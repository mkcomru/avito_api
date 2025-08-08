import asyncio
import sqlite3
from datetime import datetime
import time
from app.avito.get_all_ads import get_all_user_ads
from app.parser.parser_description_and_photo import AvitoPageParser
from app.database.database import DatabaseManager
from app.telegram.bot import TelegramBotManager

class AvitoMonitor:
    def __init__(self):
        print("🔧 Инициализируем компоненты...")
        
        try:
            self.db = DatabaseManager()
            print("✅ База данных инициализирована")
        except Exception as e:
            print(f"❌ Ошибка инициализации БД: {e}")
            raise
            
        try:
            self.telegram = TelegramBotManager()
            print("✅ Telegram бот инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации Telegram: {e}")
            raise
            
        try:
            self.parser = AvitoPageParser()
            print("✅ Парсер инициализирован")
        except Exception as e:
            print(f"❌ Ошибка инициализации парсера: {e}")
            raise
            
        print("🔧 Monitor инициализирован успешно")
    
    async def run_monitoring_cycle(self):
        """
        Запускает один полный цикл мониторинга
        Это основная функция, которая координирует всю работу
        """
        print(f"\n🔄 Начинаем цикл мониторинга: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. Получаем текущие объявления с API Авито
            print("📡 Получаем данные с API Авито...")
            current_ads = self._get_current_ads()
            if not current_ads:
                print("❌ Не удалось получить данные с API, пропускаем цикл")
                return
            
            print(f"📊 Получено {len(current_ads)} объявлений с API")
            
            # 2. Получаем сохраненные объявления из БД
            print("💾 Загружаем данные из базы...")
            stored_items = self._get_stored_items()
            print(f"💾 В базе данных: {len(stored_items)} объявлений")
            
            # 3. Сравниваем и выявляем изменения
            print("🔍 Анализируем изменения...")
            changes = self._compare_ads(current_ads, stored_items)
            
            # 4. Обрабатываем изменения
            if any(changes.values()):
                print("⚡ Обрабатываем изменения...")
                await self._process_changes(changes, current_ads, stored_items)
            else:
                print("😴 Изменений не обнаружено")
            
            print("✅ Цикл мониторинга завершен успешно")
            
        except Exception as e:
            print(f"❌ Ошибка в цикле мониторинга: {e}")
            import traceback
            traceback.print_exc()
    
    def _get_current_ads(self):
        """Получает текущие объявления с API Авито"""
        try:
            print("🌐 Отправляем запрос к API Авито...")
            ads = get_all_user_ads(status="active,removed,old,blocked,rejected")
            
            if ads is None:
                print("❌ API вернул None")
                return None
            elif len(ads) == 0:
                print("⚠️ API вернул пустой список")
                return []
            else:
                print(f"✅ API вернул {len(ads)} объявлений")
                return ads
                
        except Exception as e:
            print(f"❌ Исключение при получении данных с API: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_stored_items(self):
        """Получает все объявления из базы данных"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM items")
                items = [dict(row) for row in cursor.fetchall()]
                return items
        except Exception as e:
            print(f"❌ Ошибка получения данных из БД: {e}")
            return []
    
    def _compare_ads(self, current_ads, stored_items):
        """
        Сравнивает текущие объявления с сохраненными и выявляет изменения
        
        Returns:
            dict: Словарь с типами изменений
        """
        # Создаем множества ID для сравнения
        current_ids = {ad['id'] for ad in current_ads}
        stored_ids = {item['id'] for item in stored_items}
        
        # Создаем словари для быстрого поиска
        current_ads_dict = {ad['id']: ad for ad in current_ads}
        stored_items_dict = {item['id']: item for item in stored_items}
        
        # Выявляем изменения
        new_ids = current_ids - stored_ids
        removed_ids = stored_ids - current_ids
        common_ids = current_ids & stored_ids
        
        # Проверяем изменения статусов
        status_changed = []
        for item_id in common_ids:
            stored_item = stored_items_dict[item_id]
            current_item = current_ads_dict[item_id]
            
            if stored_item['status'] != current_item['status']:
                status_changed.append({
                    'id': item_id,
                    'old_status': stored_item['status'],
                    'new_status': current_item['status'],
                    'stored_item': stored_item,
                    'current_item': current_item
                })
        
        changes = {
            'new_items': [current_ads_dict[item_id] for item_id in new_ids],
            'removed_items': [stored_items_dict[item_id] for item_id in removed_ids],
            'status_changed': status_changed
        }
        
        # Логируем найденные изменения
        print(f"🔍 Результаты анализа:")
        print(f"   Новых объявлений: {len(changes['new_items'])}")
        print(f"   Удаленных из API: {len(changes['removed_items'])}")
        print(f"   Изменений статуса: {len(changes['status_changed'])}")
        
        if changes['new_items']:
            for item in changes['new_items']:
                print(f"   🆕 Новое: {item['title'][:50]}... (ID: {item['id']})")
        
        return changes
    
    async def _process_changes(self, changes, current_ads, stored_items):
        """Обрабатывает все выявленные изменения"""
        
        # 1. Обрабатываем новые объявления
        for new_item in changes['new_items']:
            await self._handle_new_item(new_item)
            # Добавляем задержку между обработкой объявлений
            await asyncio.sleep(2)
        
        # 2. Обрабатываем изменения статусов
        for status_change in changes['status_changed']:
            await self._handle_status_change(status_change)
            await asyncio.sleep(1)
        
        # 3. Обрабатываем удаленные объявления
        for removed_item in changes['removed_items']:
            await self._handle_removed_item(removed_item)
            await asyncio.sleep(1)
    
    async def _handle_new_item(self, item_data):
        """Обрабатывает новое объявление"""
        try:
            print(f"🆕 Обрабатываем новое объявление: {item_data['title'][:50]}...")
            
            # Получаем дополнительную информацию (описание и фото)
            description, images = await self._get_item_details(item_data)
            
            telegram_result = None
            
            # Отправляем в Telegram только активные объявления
            if item_data['status'] == 'active':
                print(f"📤 Отправляем в Telegram...")
                telegram_result = await self.telegram.send_new_item(
                    item_data, description, images
                )
            else:
                print(f"⏸️ Объявление не активно ({item_data['status']}), не отправляем в Telegram")
            
            # Сохраняем в базу данных
            self._save_item_to_db(item_data, telegram_result)
            
            print(f"✅ Новое объявление обработано: ID {item_data['id']}")
            
        except Exception as e:
            print(f"❌ Ошибка обработки нового объявления {item_data.get('id', 'unknown')}: {e}")
            import traceback
            traceback.print_exc()
    
    async def _handle_status_change(self, status_change):
        """Обрабатывает изменение статуса объявления"""
        try:
            item_id = status_change['id']
            old_status = status_change['old_status']
            new_status = status_change['new_status']
            stored_item = status_change['stored_item']
            current_item = status_change['current_item']
            
            print(f"📝 Изменение статуса ID {item_id}: {old_status} → {new_status}")
            
            # Обновляем в Telegram если есть message_id
            if stored_item.get('telegram_message_id'):
                has_photo = stored_item.get('has_photo', False)
                success = await self.telegram.edit_item_status(
                    stored_item['telegram_message_id'],
                    current_item,
                    new_status,
                    has_photo
                )
                
                if success:
                    print(f"✅ Статус обновлен в Telegram")
                else:
                    print(f"❌ Ошибка обновления в Telegram")
            
            # Обновляем в базе данных
            self._update_item_status_in_db(item_id, new_status)
            
        except Exception as e:
            print(f"❌ Ошибка обработки изменения статуса: {e}")
    
    async def _handle_removed_item(self, stored_item):
        """Обрабатывает объявление, удаленное из API"""
        try:
            item_id = stored_item['id']
            print(f"🗑️ Объявление удалено из API: ID {item_id}")
            
            # Обновляем в Telegram если есть message_id
            if stored_item.get('telegram_message_id'):
                # Создаем минимальные данные для обновления
                item_data = {
                    'id': item_id,
                    'title': 'Объявление недоступно',
                    'price': None,
                    'url': None
                }
                
                has_photo = stored_item.get('has_photo', False)
                success = await self.telegram.edit_item_status(
                    stored_item['telegram_message_id'],
                    item_data,
                    'removed_from_api',
                    has_photo
                )
                
                if success:
                    print(f"✅ Статус 'недоступно' установлен в Telegram")
            
            # Помечаем в БД как удаленное
            self._update_item_status_in_db(item_id, 'removed_from_api')
            
        except Exception as e:
            print(f"❌ Ошибка обработки удаленного объявления: {e}")
    
    async def _get_item_details(self, item_data):
        """Получает дополнительную информацию об объявлении (описание и фото)"""
        description = None
        images = None
        
        try:
            if item_data.get('url'):
                print(f"🔍 Парсим страницу: {item_data['url']}")
                page_data = self.parser.parse_item_page(item_data['url'])
                
                if page_data:
                    description = page_data.get('description')
                    images = page_data.get('images', [])
                    print(f"📄 Получено описание: {len(description) if description else 0} символов")
                    print(f"🖼️ Получено изображений: {len(images)}")
                else:
                    print(f"❌ Не удалось распарсить страницу")
                
                # Задержка между запросами к Авито
                time.sleep(3)
                
        except Exception as e:
            print(f"❌ Ошибка парсинга страницы: {e}")
        
        return description, images
    
    def _save_item_to_db(self, item_data, telegram_result):
        """Сохраняет новое объявление в базу данных"""
        try:
            telegram_message_id = None
            has_photo = False
            is_posted = False
            
            if telegram_result:
                telegram_message_id = telegram_result['message_id']
                has_photo = telegram_result['has_photo']
                is_posted = True
            
            with sqlite3.connect(self.db.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO items 
                    (id, status, telegram_message_id, is_posted_to_telegram, has_photo, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    item_data['id'],
                    item_data['status'],
                    telegram_message_id,
                    is_posted,
                    has_photo,
                    datetime.now(),
                    datetime.now()
                ))
                
            print(f"💾 Сохранено в БД: ID {item_data['id']}")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения в БД: {e}")
    
    def _update_item_status_in_db(self, item_id, new_status):
        """Обновляет статус объявления в базе данных"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                conn.execute("""
                    UPDATE items 
                    SET status = ?, updated_at = ?
                    WHERE id = ?
                """, (new_status, datetime.now(), item_id))
                
            print(f"💾 Статус обновлен в БД: ID {item_id} → {new_status}")
            
        except Exception as e:
            print(f"❌ Ошибка обновления статуса в БД: {e}")
    
    def get_monitoring_stats(self):
        """Возвращает статистику мониторинга"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                # Общее количество объявлений
                cursor = conn.execute("SELECT COUNT(*) FROM items")
                total_items = cursor.fetchone()[0]
                
                # По статусам
                cursor = conn.execute("""
                    SELECT status, COUNT(*) 
                    FROM items 
                    GROUP BY status
                """)
                status_counts = dict(cursor.fetchall())
                
                # Отправленные в Telegram
                cursor = conn.execute("""
                    SELECT COUNT(*) 
                    FROM items 
                    WHERE is_posted_to_telegram = 1
                """)
                posted_count = cursor.fetchone()[0]
                
                return {
                    'total_items': total_items,
                    'status_counts': status_counts,
                    'posted_to_telegram': posted_count
                }
        except Exception as e:
            print(f"❌ Ошибка получения статистики: {e}")
            return None


# Тестирование
async def test_monitor():
    """Тестирует основную логику мониторинга"""
    print("🧪 Тестируем Monitor...")
    
    try:
        monitor = AvitoMonitor()
        
        # Показываем текущую статистику
        stats = monitor.get_monitoring_stats()
        if stats:
            print(f"📊 Текущая статистика:")
            print(f"   Всего объявлений в БД: {stats['total_items']}")
            print(f"   Отправлено в Telegram: {stats['posted_to_telegram']}")
            print(f"   По статусам: {stats['status_counts']}")
        
        # Запускаем один цикл мониторинга
        await monitor.run_monitoring_cycle()
        
        # Показываем обновленную статистику
        print(f"\n📊 Статистика после цикла:")
        stats = monitor.get_monitoring_stats()
        if stats:
            print(f"   Всего объявлений в БД: {stats['total_items']}")
            print(f"   Отправлено в Telegram: {stats['posted_to_telegram']}")
            print(f"   По статусам: {stats['status_counts']}")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_monitor())