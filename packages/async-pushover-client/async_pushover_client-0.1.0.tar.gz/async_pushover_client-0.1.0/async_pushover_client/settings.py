import logging
import os
import json
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger('settings')
logger.setLevel('INFO')
if os.path.isfile('./auth_data.json'):
    logger.info(f'Finded auth_data file')
    with open('./auth_data.json') as f:
        auth_data: dict = json.load(f)
else:
    auth_data = {}
    
DEVICE_ID = auth_data.get('device_id',
                        os.getenv('PUSHOVER_DEVICE_ID'))
EMAIL_USERNAME = auth_data.get('email', 
                            os.getenv('PUSHOVER_EMAIL_USERNAME'))
PASSWORD = auth_data.get('secret',
                            os.getenv('PUSHOVER_PASSWORD'))
    

MESSAGE_URL = os.getenv('MESSAGE_URL', 'https://api.pushover.net/1/messages.json')
LOGIN_URL = os.getenv('LOGIN_URL', 'https://api.pushover.net/1/users/login.json')
DEVICE_REGISTRATION_URL = os.getenv('DEVICE_REGISTRATION_URL', 'https://api.pushover.net/1/devices.json')
CLEAR_MESSAGE_URL = os.getenv('DEVICE_REGISTRATION_URL',
                              'https://api.pushover.net/1/devices/{device_id}/update_highest_message.json')
