import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="avito_monitor.db"):
        """
        Инициализация менеджера базы данных
        
        Args:
            db_path (str): Путь к файлу базы данных
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        Создает базу данных и таблицу, если они не существуют
        Безопасно вызывать много раз - не пересоздает существующие таблицы
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        status TEXT NOT NULL,
                        telegram_message_id INTEGER,
                        is_posted_to_telegram BOOLEAN DEFAULT 0,
                        has_photo BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Создаем индексы для быстрого поиска
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_status 
                    ON items(status)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_posted 
                    ON items(is_posted_to_telegram)
                """)
                
                conn.commit()
                print(f"✅ База данных инициализирована: {self.db_path}")
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка при создании базы данных: {e}")
            raise
    
    def database_exists(self):
        """Проверяет, существует ли файл базы данных"""
        return os.path.exists(self.db_path)
    
    def get_database_info(self):
        """Возвращает информацию о базе данных"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM items")
                total_items = cursor.fetchone()[0]
                
                cursor = conn.execute("""
                    SELECT status, COUNT(*) 
                    FROM items 
                    GROUP BY status
                """)
                status_counts = dict(cursor.fetchall())
                
                cursor = conn.execute("""
                    SELECT COUNT(*) 
                    FROM items 
                    WHERE is_posted_to_telegram = 1
                """)
                posted_count = cursor.fetchone()[0]
                
                return {
                    'total_items': total_items,
                    'status_counts': status_counts,
                    'posted_to_telegram': posted_count,
                    'db_path': self.db_path,
                    'db_size_mb': round(os.path.getsize(self.db_path) / 1024 / 1024, 2) if self.database_exists() else 0
                }
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка при получении информации о БД: {e}")
            return None
    
    def clear_database(self):
        """
        ОСТОРОЖНО! Удаляет все данные из таблицы
        Используйте только для тестирования или сброса
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM items")
                conn.commit()
                print("🗑️ Все данные удалены из базы данных")
        except sqlite3.Error as e:
            print(f"❌ Ошибка при очистке БД: {e}")
    
    def backup_database(self, backup_path=None):
        """Создает резервную копию базы данных"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_avito_monitor_{timestamp}.db"
        
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ Резервная копия создана: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Ошибка при создании резервной копии: {e}")
            return None

