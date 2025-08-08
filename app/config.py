import os
from dotenv import load_dotenv


load_dotenv()

AVITO_CLIENT_ID = os.getenv('CLIENT_ID')
AVITO_CLIENT_SECRET = os.getenv('CLIENT_SECRET')

TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

AVITO_BASE_URL = os.getenv('BASE_URL')

PROXY_SERVER = os.getenv('PROXY_SERVER')
PROXY_ENABLED = True

required_vars = {
    'CLIENT_ID': AVITO_CLIENT_ID,
    'CLIENT_SECRET': AVITO_CLIENT_SECRET,
    'BOT_TOKEN': TELEGRAM_BOT_TOKEN,
    'CHAT_ID': TELEGRAM_CHAT_ID,
    'BASE_URL': AVITO_BASE_URL
}
