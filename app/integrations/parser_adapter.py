import asyncio
import random
import time
from loguru import logger
from ..parser.parser_description_and_photo import get_parser


class AvitoParserAdapter:
    """
    Адаптер парсера для интеграции с системой мониторинга
    Основан на проверенном parser_cls.py
    """
    
    def __init__(self):
        self.parser = get_parser()
        logger.info("🔧 Адаптер парсера инициализирован")
    
    async def get_item_details_async(self, item_url):
        """
        Асинхронно получает детали объявления
        
        Args:
            item_url (str): URL объявления
            
        Returns:
            tuple: (description, images) или (None, None)
        """
        try:
            logger.info(f"🔍 Запрашиваем детали: {item_url}")
            
            # Запускаем парсинг в отдельном потоке чтобы не блокировать асинхронность
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self.parser.parse_item_page, 
                item_url
            )
            
            if result:
                description = result.get('description')
                images = result.get('images', [])
                
                logger.success(f"✅ Детали получены: описание - {bool(description)}, фото - {len(images)}")
                return description, images
            else:
                logger.warning("⚠️ Не удалось получить детали")
                return None, None
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения деталей: {e}")
            return None, None
    
    def parse_multiple_items_sync(self, item_urls, delay_range=(5, 8)):
        """
        Синхронно парсит несколько объявлений с задержками как в оригинальном parser_cls
        
        Args:
            item_urls (list): Список URL
            delay_range (tuple): Диапазон задержек между запросами
            
        Returns:
            dict: {url: {'description': str, 'images': list}}
        """
        results = {}
        
        for i, url in enumerate(item_urls, 1):
            logger.info(f"🔍 Парсим {i}/{len(item_urls)}: {url}")
            
            try:
                result = self.parser.parse_item_page(url)
                results[url] = result if result else {'description': None, 'images': []}
                
                logger.success(f"✅ Объявление {i} обработано")
                
                # Задержка между запросами как в оригинальном парсере (кроме последнего)
                if i < len(item_urls):
                    delay = random.uniform(*delay_range)
                    logger.debug(f"⏳ Пауза {delay:.1f} секунд")
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"❌ Ошибка парсинга {url}: {e}")
                results[url] = {'description': None, 'images': []}
        
        return results


# Глобальный экземпляр адаптера
_adapter_instance = None

def get_parser_adapter():
    """Получить единственный экземпляр адаптера"""
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = AvitoParserAdapter()
    return _adapter_instance


async def get_listing_details(item_url):
    """
    Простая асинхронная функция для получения деталей объявления
    
    Args:
        item_url (str): URL объявления
        
    Returns:
        tuple: (description, images)
    """
    adapter = get_parser_adapter()
    return await adapter.get_item_details_async(item_url)


# Функции для совместимости с вашим monitor.py
def parse_item_for_details(item_url):
    """
    Синхронная функция для парсинга деталей (для обратной совместимости)
    
    Args:
        item_url (str): URL объявления
        
    Returns:
        dict: {'description': str, 'images': list} или None
    """
    parser = get_parser()
    return parser.parse_item_page(item_url)