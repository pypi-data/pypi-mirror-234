# async_pushover_client

Проект представляет собой набор синхронных и асинхронных методов для работы с [API PushOver ](https://pushover.net/api)

## Установка

```bash
pip install async_pushover_client
```

## Использование


Создайте _.env_ файл, и поместите туда переменные
```
PUSHOVER_DEVICE_ID=ВАШ ИД устройства, если его нет зарегистрируется автоматически
PUSHOVER_EMAIL_USERNAME=email аккаунта
PUSHOVER_PASSWORD=пароль аккаунта
```
Или создайте файл _auth_data.json_ и положите его в корень проекта.
```json
{"email": "example@example.com", 
  "password": "password", 
  "secret": "secret", "device_id": "device_id"}
```
После первого успешного запуска worker файл создастся автоматически, вы так же можете вызвать метод
```python
from async_pushover_client.main import OpenAPI
from async_pushover_client.settings import DEVICE_ID, PASSWORD, EMAIL_USERNAME

api = OpenAPI(email=EMAIL_USERNAME,
              password=PASSWORD,
              device_id=DEVICE_ID)
api.launch_preparation() 
# ИЛИ его асинхронное представление a_launch_preparation()

```
Для того, что бы запустить асинхронный worker достаточно переопределить метод _receiver_messages_, или метод
_on_message_, если вы хотите работать с сырыми данными.

```python
from async_pushover_client.worker import WSClientPushOver
from async_websocket_client.apps import AsyncWebSocketApp


class MyTestCase(WSClientPushOver):
    async def receiver_messages(self, message: dict):
        print(self.messages)
        print(message)


client = AsyncWebSocketApp('wss://client.pushover.net/push', MyTestCase())
client.asyncio_run()
```

Метод получает _message_, у которого есть все данные представляемые API PushOver.
Далее примените фантазию, и решите что вы сделаете c _message_, который будет хранить в себе одно сообщение,
или _self.messages_, хранящий в себе не полученные сообщения на момент, пока worker не работал.

Вы так же можете поработать с методами получения и удаления сообщений, без использования WebSocket.
Для этого достаточно импортировать класс _**OpenAPI**_

```python
from async_pushover_client.main import OpenAPI
from async_pushover_client.settings import DEVICE_ID, PASSWORD, EMAIL_USERNAME

api = OpenAPI(email=EMAIL_USERNAME,
              password=PASSWORD,
              device_id=DEVICE_ID)
messages = api.receiving_notifications()
print(messages)

```