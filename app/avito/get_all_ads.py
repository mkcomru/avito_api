import requests
from app.config import AVITO_BASE_URL
from .get_access_token import get_access_token


def get_user_ads(status="active", per_page=100, page=1, updated_from=None, category=None):
    """
    Получает список объявлений пользователя из API Авито.

    Args:
        status (str, optional): Статусы объявлений (например, "active", "removed").
                                По умолчанию "active".
                                Можно передать несколько через запятую: "active,old".
        per_page (int, optional): Количество записей на странице (1-99). По умолчанию 100.
        page (int, optional): Номер страницы (начиная с 1). По умолчанию 1.
        updated_from (str, optional): Фильтр по дате обновления (YYYY-MM-DD).
        category (int, optional): Идентификатор категории.

    Returns:
        dict: Ответ API Авито в формате JSON, содержащий meta и resources,
            или None в случае ошибки.
    """
    access_token = get_access_token()
    if not access_token:
        print("Не удалось получить access token")
        return None

    url = f"{AVITO_BASE_URL}/core/v1/items"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "status": status,
        "per_page": per_page,
        "page": page
    }

    if updated_from:
        params["updatedAtFrom"] = updated_from
    if category:
        params["category"] = category

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        filtered_data = []
        for item in data.get("resources", []):
            filtered_item = {
                "id": item.get("id"),
                "title": item.get("title"),
                "status": item.get("status"),
                "price": item.get("price"),
                "url": item.get("url")
            }
            filtered_data.append(filtered_item)

        return {
            "meta": data.get("meta", {}),
            "resources": filtered_data
        }

    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка при запросе списка объявлений: {e}")
        print(f"Статус код: {response.status_code}")
        try:
            error_detail = response.json()
            print(f"Детали ошибки: {error_detail}")
        except:
            print(f"Тело ответа: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при запросе списка объявлений: {e}")
        return None
    except ValueError as e:  
        print(f"Ошибка декодирования JSON ответа: {e}")
        print(f"Тело ответа: {response.text}")
        return None


def get_all_user_ads(status="active", updated_from=None, category=None):
    """
    Получает ВСЕ объявления пользователя из API Авито через пагинацию.

    Args:
        status (str, optional): Статусы объявлений (например, "active", "removed").
                                По умолчанию "active".
                                Можно передать несколько через запятую: "active,old".
        updated_from (str, optional): Фильтр по дате обновления (YYYY-MM-DD).
        category (int, optional): Идентификатор категории.

    Returns:
        list: Список всех объявлений пользователя,
            или None в случае ошибки.
    """
    all_ads = []
    page = 1
    per_page = 100  # Максимальное количество на странице
    
    while True:
        page_data = get_user_ads(
            status=status,
            per_page=per_page,
            page=page,
            updated_from=updated_from,
            category=category
        )

        if not page_data:
            print("Ошибка при получении данных")
            return None
            
        resources = page_data.get("resources", [])
        
        if not resources:
            # Если на странице нет объявлений, значит достигли конца
            break
            
        all_ads.extend(resources)
        
        # Если получили меньше объявлений, чем запрашивали, значит это последняя страница
        if len(resources) < per_page:
            break
            
        page += 1
    
    print(f"Всего получено {len(all_ads)} объявлений")
    return all_ads


if __name__ == "__main__":
    ads = get_all_user_ads(status="active")
    print(ads)  # Выводим полученные объявления для проверки

