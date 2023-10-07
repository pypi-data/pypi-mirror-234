import json
import requests
from .settings import *
from .exceptions import AuthenticationError, MessagesError
from typing import Union
import aiohttp
import logging
import aiofiles
import asyncio


class OpenAPI:
    def __init__(self, email: str, password: str,
                 device_id=None):
        self.email: str = email
        self.password: str = password
        self.secret: Union[str, None] = None
        self.device_id: Union[str, None] = device_id

    def login(self):
        response = requests.post(LOGIN_URL, data=self.__dict__)
        if response.status_code == 200:
            auth_data = response.json()
            self.secret = auth_data.get('secret')
        else:
            raise AuthenticationError()

    async def a_login(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(LOGIN_URL, data=self.__dict__) as response:
                if response.status == 200:
                    auth_data: dict = await response.json()
                    self.secret = auth_data.get('secret')
                else:
                    raise AuthenticationError()

    def device_registration(self, name, os='O'):
        response = requests.post(DEVICE_REGISTRATION_URL,
                                 data=dict(secret=self.secret,
                                           name=name,
                                           os=os))
        if response.status_code == 200:
            data = response.json()
            self.device_id = data.get('id')
        else:
            raise AuthenticationError(message=response.text)

    async def a_device_registration(self, name, os='O'):
        async with aiohttp.ClientSession() as session:
            async with session.post(DEVICE_REGISTRATION_URL,
                                    data=dict(secret=self.secret,
                                              name=name,
                                              os=os)) as response:
                if response.status == 200:
                    data: dict = await response.json()
                    self.device_id = data.get('id')
                else:
                    raise AuthenticationError(message=await response.text())

    def get_messages(self):
        response = requests.get(MESSAGE_URL,
                                params=dict(secret=self.secret,
                                            device_id=self.device_id))
        if response.status_code == 200:
            data = response.json()
            return data.get('messages')
        else:
            raise MessagesError(message=response.text)

    async def a_get_messages(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(MESSAGE_URL,
                                   params=dict(secret=self.secret,
                                               device_id=self.device_id)) as response:
                if response.status == 200:
                    data: dict = await response.json()
                    return data.get('messages')
                else:
                    raise MessagesError(message=await response.text())

    def clear_messages(self, message_id):
        url = f"https://api.pushover.net/1/devices/{self.device_id}/update_highest_message.json"
        response = requests.post(url, data=dict(secret=self.secret,
                                                message=message_id))
        if response.status_code == 200:
            return response.json()
        else:
            raise MessagesError(message=response.text)

    async def a_clear_message_by_id(self, message_id: int):
        url = CLEAR_MESSAGE_URL.format(device_id=self.device_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   params=dict(secret=self.secret,
                                               message_id=message_id)) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise MessagesError(message=await response.text())

    async def a_clear_messages(self, messages_id: list):
        await asyncio.gather(*map(self.a_clear_message_by_id, messages_id))

    def launch_preparation(self, name_device: str = None, make_auth_file: bool = True) -> dict:
        self.login()
        if not self.device_id:
            logger.info('Try register device by name')
            if not name_device:
                logger.warning('hmmm... name_device is not indicated')
                name_device = 'worker'
                logger.warning(f'set name {name_device}')
            self.device_registration(name=name_device)
            logger.info(f'you`re device id is {self.device_id}')
        if make_auth_file:
            with open('auth_data.json', 'w') as f:
                f.write(json.dumps(self.__dict__))
        messages = self.get_messages()
        for message in messages:
            self.clear_messages(message.get('id'))
        return messages

    def receiving_notifications(self) -> dict:
        messages = self.get_messages()
        for message in messages:
            self.clear_messages(message.get('id'))
        return messages

    @staticmethod
    async def a_get_list_id_from_dict(messages: dict) -> list:
        return [message.get('id') for message in messages]

    async def a_launch_preparation(self, name_device: str = None, make_auth_file: bool = True) -> dict:
        await self.a_login()
        if not self.device_id:
            if not name_device:
                name_device = 'worker'
            await self.a_device_registration(name=name_device)
        if make_auth_file:
            async with aiofiles.open('auth_data.json', mode='w') as f:
                await f.write(json.dumps(self.__dict__()))
        messages = await self.a_get_messages()
        ids = await OpenAPI.a_get_list_id_from_dict(messages)
        await self.a_clear_messages(ids)
        return messages

    async def a_receiving_notifications(self) -> dict:
        messages = await self.a_get_messages()
        ids = await OpenAPI.a_get_list_id_from_dict(messages)
        await self.a_clear_messages(ids)
        return messages
