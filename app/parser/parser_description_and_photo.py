import os
import random
import time
import re
from selenium.webdriver.common.by import By
from seleniumbase import SB
from loguru import logger
import sys

# Добавляем корневую директорию в путь
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.config import PROXY_SERVER, PROXY_ENABLED


class AvitoPageParser:
    """
    Адаптированный парсер страниц Авито для получения только фото и описания
    Основан на проверенном parser_cls.py
    """
    
    def __init__(self, proxy=None, debug_mode=False):
        """
        Инициализация парсера
        
        Args:
            proxy (str): Прокси в формате username:password@server:port или None для использования из config
            debug_mode (bool): Показывать браузер для отладки
        """
        # Используем прокси из config если не передан явно
        if proxy is None and PROXY_ENABLED:
            self.proxy = PROXY_SERVER
        else:
            self.proxy = proxy
            
        self.debug_mode = debug_mode
        self.user_agents = self._load_user_agents()
        
        # Селекторы точно как в оригинальном parser_cls
        self.selectors = {
            'description_full': "[data-marker='item-view/item-description']",
            'images': [
                "img[itemprop='image']",
                ".gallery-img-frame img",
                ".gallery-extended img", 
                "[data-marker='image-frame/image-wrapper'] img",
                ".image-frame img",
                "img[data-marker*='image']"
            ]
        }
        
        logger.info(f"🔧 Парсер инициализирован. Прокси: {'Включен' if self.proxy else 'Отключен'}")
    
    def _load_user_agents(self):
        """Загружает user agents как в оригинальном парсере"""
        try:
            # Пытаемся использовать тот же файл что и в parser_cls
            ua_files = [
                "user_agent_pc.txt",
                "app/parser_avito/user_agent_pc.txt",
                "parser_avito/user_agent_pc.txt"
            ]
            
            for ua_file in ua_files:
                if os.path.exists(ua_file):
                    with open(ua_file, 'r', encoding='utf-8') as f:
                        agents = [line.strip() for line in f.readlines() if line.strip()]
                    if agents:
                        logger.debug(f"Загружено {len(agents)} user agents из {ua_file}")
                        return agents
        except Exception as e:
            logger.debug(f"Не удалось загрузить user agents: {e}")
        
        # Fallback user agents как в оригинале
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    
    def ip_block_handler(self):
        """Обработка блокировки IP как в оригинальном парсере"""
        logger.warning("⛔ Обнаружена блокировка IP")
        if self.proxy:
            logger.info("🔄 Пауза из-за блокировки, прокси активен")
            time.sleep(random.uniform(30, 60))
        else:
            logger.info("🔄 Блок IP. Прокси нет, увеличенная пауза")
            time.sleep(random.uniform(300, 350))
    
    def parse_item_page(self, url):
        """
        Парсит страницу объявления и возвращает только фото и описание
        
        Args:
            url (str): URL страницы объявления
            
        Returns:
            dict: {'description': str, 'images': list} или None
        """
        if not url:
            logger.error("URL не предоставлен")
            return None
        
        logger.info(f"🔍 Парсим страницу: {url}")
        
        max_retries = 2
        
        for attempt in range(max_retries + 1):
            try:
                # Настройки браузера точно как в оригинальном parser_cls
                with SB(uc=True,  # Обход детекции
                        headed=True if self.debug_mode else False,
                        headless2=True if not self.debug_mode else False,
                        page_load_strategy="eager",
                        block_images=False,  # НЕ блокируем изображения - они нам нужны
                        agent=random.choice(self.user_agents),
                        proxy=self.proxy if self.proxy else None,
                        sjw=False,  # Стабильность важнее скорости для парсинга фото
                        ) as driver:
                    
                    # Переходим на страницу
                    driver.get(url)
                    
                    # Проверяем на блокировку точно как в оригинале
                    if "Доступ ограничен" in driver.get_title():
                        logger.warning(f"⛔ Доступ ограничен (попытка {attempt + 1})")
                        if attempt < max_retries:
                            self.ip_block_handler()
                            continue
                        else:
                            return None
                    
                    # Ждем загрузки контента как в оригинальном парсере
                    try:
                        # Используем тот же селектор что и в parser_cls для проверки загрузки
                        driver.wait_for_element("[data-marker='item-view/total-views']", timeout=10)
                    except Exception:
                        # Дополнительная проверка на блокировку
                        if "Доступ ограничен" in driver.get_title():
                            logger.warning("⛔ Блокировка обнаружена при ожидании загрузки")
                            if attempt < max_retries:
                                self.ip_block_handler()
                                continue
                            else:
                                return None
                        logger.debug("Не дождался полной загрузки страницы")
                    
                    # Прокручиваем страницу для загрузки всех изображений
                    # Имитируем человеческое поведение как в оригинале
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
                        time.sleep(random.uniform(1, 2))
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                        time.sleep(random.uniform(1, 2))
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(random.uniform(1, 2))
                        driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(random.uniform(1, 2))
                    except Exception:
                        pass
                    
                    # Извлекаем данные
                    result = self._extract_page_data(driver)
                    
                    # Задержка перед закрытием браузера как в оригинале
                    time.sleep(random.uniform(2, 4))
                    
                    return result
                    
            except Exception as e:
                logger.error(f"❌ Ошибка парсинга (попытка {attempt + 1}): {e}")
                if attempt < max_retries:
                    delay = random.uniform(10, 15)
                    logger.info(f"⏳ Пауза {delay:.1f} секунд перед повторной попыткой")
                    time.sleep(delay)
                    continue
                else:
                    logger.error("❌ Все попытки исчерпаны")
                    return None
        
        return None
    
    def _extract_page_data(self, driver):
        """Извлекает только описание и изображения"""
        result = {
            'description': None,
            'images': []
        }
        
        # Извлекаем полное описание
        try:
            description_elements = driver.find_elements(self.selectors['description_full'], by="css selector")
            if description_elements:
                description = description_elements[0].text.strip()
                if description:
                    result['description'] = description
                    logger.success(f"📄 Описание найдено: {len(description)} символов")
                else:
                    logger.warning("📄 Описание пустое")
            else:
                logger.warning("📄 Элемент описания не найден")
        except Exception as e:
            logger.error(f"❌ Ошибка извлечения описания: {e}")
        
        # Извлекаем все изображения
        images = []
        try:
            for selector in self.selectors['images']:
                try:
                    img_elements = driver.find_elements(selector, by="css selector")
                    for img in img_elements:
                        # Проверяем разные атрибуты изображений
                        src = (img.get_attribute('src') or 
                              img.get_attribute('data-src') or 
                              img.get_attribute('data-lazy-src') or
                              img.get_attribute('data-original'))
                        
                        if src and src.startswith('http') and src not in images:
                            # Улучшаем качество изображений avito.st как в оригинале
                            if 'avito.st' in src:
                                src = re.sub(r'_\d+x\d+', '_1280x960', src)
                            images.append(src)
                except Exception as e:
                    logger.debug(f"Ошибка с селектором {selector}: {e}")
                    continue
            
            # Убираем дубликаты и ограничиваем количество
            result['images'] = list(dict.fromkeys(images))[:15]  # Максимум 15 фото
            logger.success(f"🖼️ Найдено изображений: {len(result['images'])}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка извлечения изображений: {e}")
        
        return result


# Единственный экземпляр парсера для всего приложения (как в оригинале)
_parser_instance = None

def get_parser():
    """Получить единственный экземпляр парсера"""
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = AvitoPageParser(debug_mode=False)
    return _parser_instance


def parse_avito_photos_and_description(url, proxy=None, debug=False):
    """
    Простая функция для парсинга фото и описания
    
    Args:
        url (str): URL страницы объявления
        proxy (str): Прокси в формате username:password@server:port
        debug (bool): Показывать браузер
        
    Returns:
        dict: {'description': str, 'images': list} или None
    """
    try:
        parser = AvitoPageParser(proxy=proxy, debug_mode=debug)
        return parser.parse_item_page(url)
    except Exception as e:
        logger.error(f"❌ Ошибка парсинга: {e}")
        return None


def test_parser():
    """Тестирует парсер с вашими настройками"""
    logger.info("🧪 Тестируем адаптированный парсер...")
    
    # Ваш прокси из конфига
    proxy = PROXY_SERVER if PROXY_ENABLED else None
    
    # Тестовые URL
    test_urls = [
        "https://www.avito.ru/amurskaya_oblast_blagoveschensk/predlozheniya_uslug/fotozona_v_arendu_na_gender_pati_7549350435",
        "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_32_m_35_et._2011149284"
    ]
    
    for i, test_url in enumerate(test_urls, 1):
        logger.info(f"\n📄 Тест {i}: {test_url}")
        logger.info(f"🔧 Используемый прокси: {proxy}")
        
        # Создаем парсер
        parser = AvitoPageParser(proxy=proxy, debug_mode=True)  # True для просмотра браузера
        
        # Парсим
        result = parser.parse_item_page(test_url)
        
        if result:
            logger.success("✅ Парсинг успешен!")
            
            if result['description']:
                logger.info(f"📄 Описание ({len(result['description'])} символов):")
                logger.info(f"   {result['description'][:200]}...")
            else:
                logger.warning("📄 Описание не найдено")
            
            if result['images']:
                logger.info(f"🖼️ Найдено {len(result['images'])} изображений:")
                for j, img_url in enumerate(result['images'][:3], 1):
                    logger.info(f"   {j}. {img_url}")
            else:
                logger.warning("🖼️ Изображения не найдены")
                
        else:
            logger.error("❌ Парсинг неудачен")
        
        # Пауза между тестами
        if i < len(test_urls):
            logger.info("⏳ Пауза 10 секунд между тестами...")
            time.sleep(10)


if __name__ == "__main__":
    test_parser()