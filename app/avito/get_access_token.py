import requests
from app.config import AVITO_CLIENT_ID, AVITO_CLIENT_SECRET, AVITO_BASE_URL


def get_access_token():
    """
    Получает access token от API Авито
    Возвращает access_token или None в случае ошибки
    """
    url = f"{AVITO_BASE_URL}/token"
    
    payload = {
        'client_id': AVITO_CLIENT_ID,
        'client_secret': AVITO_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        token_data = response.json()
        return token_data['access_token']
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе токена: {e}")
        return None
    except KeyError as e:
        print(f"Ошибка в структуре ответа: {e}")
        return None
