import os
import random
import time
import re
from selenium.webdriver.common.by import By
from seleniumbase import SB
from loguru import logger


class AvitoItemParser:
    """
    Адаптированный парсер на основе parser_avito для извлечения описания и фото
    Оптимизирован для работы без прокси
    """
    
    def __init__(self, debug_mode=False):
        """
        Инициализация парсера
        
        Args:
            debug_mode (bool): Показывать браузер для отладки
        """
        self.debug_mode = debug_mode
        self.user_agents = self._load_user_agents()
        
        # Селекторы из parser_avito/locator.py
        self.selectors = {
            # Для страницы объявления
            'description': "[data-marker='item-view/item-description']",
            'images': "img[itemprop='image']",
            'image_gallery': ".gallery-img-frame img",
            'additional_images': ".gallery-extended img",
            'price': "[itemprop='price']",
            'title': "[itemprop='name']",
            'geo': "div[class*='style-item-address']",
            'seller_name': "[data-marker='seller-info/label']",
            'date_public': "[data-marker='item-view/item-date']",
            'total_views': "[data-marker='item-view/total-views']",
            'seller_link': "[data-marker='seller-link/link']"
        }
        
        # Задержки для имитации человеческого поведения (без прокси нужно быть осторожнее)
        self.delays = {
            'page_load': (3, 6),
            'between_actions': (2, 4),
            'after_error': (10, 15)
        }
    
    def _load_user_agents(self):
        """Загружает user agents из parser_avito или использует fallback"""
        try:
            ua_path = os.path.join('parser_avito', 'user_agent_pc.txt')
            if os.path.exists(ua_path):
                with open(ua_path, 'r', encoding='utf-8') as f:
                    agents = [line.strip() for line in f.readlines() if line.strip()]
                if agents:
                    logger.debug(f"Загружено {len(agents)} user agents из файла")
                    return agents
        except Exception as e:
            logger.debug(f"Не удалось загрузить user agents: {e}")
        
        # Fallback user agents для стабильной работы
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    
    def parse_item_page(self, url):
        """
        Парсит страницу объявления Авито и извлекает описание и изображения
        
        Args:
            url (str): URL страницы объявления
            
        Returns:
            dict: {'description': str, 'images': list, 'additional_info': dict} или None
        """
        if not url:
            logger.error("URL не предоставлен")
            return None
        
        logger.info(f"Парсим страницу: {url}")
        
        # Увеличиваем задержки для работы без прокси
        retry_count = 0
        max_retries = 2
        
        while retry_count < max_retries:
            try:
                # Настройки браузера адаптированные из parser_avito/parser_cls.py
                with SB(uc=True,  # Обход детекции
                        headed=self.debug_mode,
                        headless2=not self.debug_mode,
                        page_load_strategy="eager",  # Быстрая загрузка
                        block_images=False,  # НЕ блокируем изображения
                        agent=random.choice(self.user_agents),
                        sjw=False,  # Отключаем быструю скорость для стабильности без прокси
                        ) as driver:
                    
                    # Переходим на страницу
                    driver.get(url)
                    
                    # Проверяем на блокировку как в оригинальном парсере
                    page_title = driver.get_title()
                    if "Доступ ограничен" in page_title or "Access denied" in page_title:
                        logger.error("Доступ ограничен - возможна блокировка IP")
                        
                        if retry_count < max_retries - 1:
                            retry_count += 1
                            delay = random.uniform(*self.delays['after_error'])
                            logger.info(f"Попытка {retry_count + 1}/{max_retries} через {delay:.1f} секунд")
                            time.sleep(delay)
                            continue
                        else:
                            return None
                    
                    # Ждем загрузки основного контента
                    try:
                        driver.wait_for_element(self.selectors['description'], timeout=10)
                    except Exception:
                        logger.warning("Описание не найдено в течение 10 секунд")
                    
                    # Имитируем человеческое поведение - прокручиваем страницу
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
                        time.sleep(random.uniform(1, 2))
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                        time.sleep(random.uniform(1, 2))
                        driver.execute_script("window.scrollTo(0, 0);")
                    except Exception:
                        pass
                    
                    # Извлекаем данные
                    result = self._extract_data(driver)
                    
                    # Задержка для имитации человеческого поведения
                    time.sleep(random.uniform(*self.delays['between_actions']))
                    
                    return result
                    
            except Exception as e:
                logger.error(f"Ошибка при парсинге (попытка {retry_count + 1}): {e}")
                
                if retry_count < max_retries - 1:
                    retry_count += 1
                    delay = random.uniform(*self.delays['after_error'])
                    logger.info(f"Повторная попытка через {delay:.1f} секунд")
                    time.sleep(delay)
                    continue
                else:
                    return None
        
        return None
    
    def _extract_data(self, driver):
        """Извлекает данные со страницы используя Selenium driver"""
        result = {
            'description': None,
            'images': [],
            'additional_info': {}
        }
        
        try:
            # Извлекаем описание
            try:
                description_elements = driver.find_elements(self.selectors['description'], by="css selector")
                if description_elements:
                    description = description_elements[0].text.strip()
                    if description:
                        result['description'] = description
                        logger.success(f"Найдено описание: {len(description)} символов")
                    else:
                        logger.warning("Описание пустое")
                else:
                    logger.warning("Элемент описания не найден")
            except Exception as e:
                logger.error(f"Ошибка при извлечении описания: {e}")
            
            # Извлекаем изображения
            images = []
            try:
                # Ищем изображения по всем возможным селекторам
                img_selectors = [
                    self.selectors['images'],
                    self.selectors['image_gallery'],
                    self.selectors['additional_images'],
                    ".gallery-img-frame img",
                    ".gallery-extended img",
                    "[data-marker='image-frame/image-wrapper'] img",
                    ".image-frame img"
                ]
                
                for selector in img_selectors:
                    try:
                        img_elements = driver.find_elements(selector, by="css selector")
                        for img in img_elements:
                            # Проверяем разные атрибуты для получения URL изображения
                            src = (img.get_attribute('src') or 
                                  img.get_attribute('data-src') or 
                                  img.get_attribute('data-lazy-src') or
                                  img.get_attribute('data-original'))
                            
                            if src and src.startswith('http') and src not in images:
                                # Улучшаем качество изображений с avito.st
                                if 'avito.st' in src:
                                    # Заменяем размер на максимальный
                                    src = re.sub(r'_\d+x\d+', '_1280x960', src)
                                
                                images.append(src)
                    except Exception as e:
                        logger.debug(f"Ошибка с селектором {selector}: {e}")
                        continue
                
                # Убираем дубликаты и ограничиваем количество
                result['images'] = list(dict.fromkeys(images))[:15]  # Убираем дубли и берем первые 15
                logger.success(f"Найдено изображений: {len(result['images'])}")
                
            except Exception as e:
                logger.error(f"Ошибка при извлечении изображений: {e}")
            
            # Дополнительная информация (опционально, может пригодиться)
            try:
                # Цена
                try:
                    price_elements = driver.find_elements(self.selectors['price'], by="css selector")
                    if price_elements:
                        result['additional_info']['price'] = price_elements[0].get_attribute('content')
                except Exception:
                    pass
                
                # Название
                try:
                    title_elements = driver.find_elements(self.selectors['title'], by="css selector")
                    if title_elements:
                        result['additional_info']['title'] = title_elements[0].text.strip()
                except Exception:
                    pass
                
                # Геолокация
                try:
                    geo_elements = driver.find_elements(self.selectors['geo'], by="css selector")
                    if geo_elements:
                        result['additional_info']['location'] = geo_elements[0].text.strip()
                except Exception:
                    pass
                
                # Продавец
                try:
                    seller_elements = driver.find_elements(self.selectors['seller_name'], by="css selector")
                    if seller_elements:
                        result['additional_info']['seller'] = seller_elements[0].text.strip()
                except Exception:
                    pass
                
                # Дата публикации
                try:
                    date_elements = driver.find_elements(self.selectors['date_public'], by="css selector")
                    if date_elements:
                        date_text = date_elements[0].text.strip()
                        if "· " in date_text:
                            date_text = date_text.replace("· ", '')
                        result['additional_info']['date_published'] = date_text
                except Exception:
                    pass
                
                # Просмотры
                try:
                    views_elements = driver.find_elements(self.selectors['total_views'], by="css selector")
                    if views_elements:
                        views_text = views_elements[0].text.strip()
                        # Извлекаем число из строки типа "123 просмотра"
                        views_match = re.search(r'\d+', views_text)
                        if views_match:
                            result['additional_info']['views'] = int(views_match.group())
                except Exception:
                    pass
                
            except Exception as e:
                logger.debug(f"Ошибка при извлечении дополнительной информации: {e}")
        
        except Exception as e:
            logger.error(f"Общая ошибка при извлечении данных: {e}")
        
        return result


# Глобальный экземпляр парсера (singleton)
_parser_instance = None

def get_parser_instance(debug_mode=False):
    """Получить экземпляр парсера (singleton pattern)"""
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = AvitoItemParser(debug_mode=debug_mode)
    return _parser_instance

def parse_avito_item_page(url, debug_mode=False):
    """
    Основная функция для парсинга страницы объявления Авито
    
    Args:
        url (str): URL страницы объявления
        debug_mode (bool): Режим отладки
        
    Returns:
        dict: {'description': str, 'images': list, 'additional_info': dict} или None
    """
    parser = get_parser_instance(debug_mode=debug_mode)
    return parser.parse_item_page(url)


# Функция для интеграции в вашу систему
def get_listing_details(listing_url, debug=False):
    """
    Функция для интеграции в вашу систему уведомлений
    
    Args:
        listing_url (str): URL объявления
        debug (bool): Режим отладки
        
    Returns:
        dict: Данные объявления или None при ошибке
    """
    try:
        logger.info(f"Получаем детали объявления: {listing_url}")
        
        # Парсим страницу
        parsed_data = parse_avito_item_page(listing_url, debug_mode=debug)
        
        if parsed_data:
            logger.success("Данные успешно получены")
            return {
                'description': parsed_data.get('description'),
                'images': parsed_data.get('images', []),
                'price': parsed_data.get('additional_info', {}).get('price'),
                'title': parsed_data.get('additional_info', {}).get('title'),
                'location': parsed_data.get('additional_info', {}).get('location'),
                'seller': parsed_data.get('additional_info', {}).get('seller'),
                'date_published': parsed_data.get('additional_info', {}).get('date_published'),
                'views': parsed_data.get('additional_info', {}).get('views')
            }
        else:
            logger.error("Не удалось получить данные объявления")
            return None
            
    except Exception as e:
        logger.error(f"Ошибка при получении деталей объявления: {e}")
        return None


# Функция для тестирования
def test_parser():
    """Тестирует парсер"""
    logger.info("🧪 Тестируем адаптированный парсер без прокси...")
    
    # Тестовая ссылка (замените на реальную)
    test_url = "https://www.avito.ru/moskva/odezhda_obuv_aksessuary/sportivnye_solntsezaschitnye_ochki_bliz_7403930411"
    
    result = get_listing_details(test_url, debug=True)
    
    if result:
        logger.success("✅ Парсинг выполнен успешно!")
        logger.info(f"📄 Описание: {'Найдено' if result['description'] else 'Не найдено'}")
        if result['description']:
            logger.info(f"   Длина: {len(result['description'])} символов")
            logger.info(f"   Превью: {result['description'][:100]}...")
        
        logger.info(f"🖼️ Изображений: {len(result['images'])}")
        for i, img_url in enumerate(result['images'][:3], 1):
            logger.info(f"   {i}. {img_url}")
            
        if result.get('price'):
            logger.info(f"💰 Цена: {result['price']}")
        if result.get('location'):
            logger.info(f"📍 Местоположение: {result['location']}")
        if result.get('seller'):
            logger.info(f"👤 Продавец: {result['seller']}")
    else:
        logger.error("❌ Ошибка парсинга")


if __name__ == "__main__":
    test_parser()