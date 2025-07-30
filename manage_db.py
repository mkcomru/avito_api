from database.database import DatabaseManager
import sys

def main():
    """Утилита для управления базой данных"""
    db_manager = DatabaseManager()
    
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python manage_db.py info     - информация о БД")
        print("  python manage_db.py create   - создать БД")
        print("  python manage_db.py backup   - создать резервную копию")
        print("  python manage_db.py clear    - очистить БД (ОСТОРОЖНО!)")
        return
    
    command = sys.argv[1].lower()
    
    if command == "info":
        info = db_manager.get_database_info()
        if info:
            print("📊 Информация о базе данных:")
            print(f"   Путь: {info['db_path']}")
            print(f"   Размер: {info['db_size_mb']} MB")
            print(f"   Всего объявлений: {info['total_items']}")
            print(f"   Отправлено в Telegram: {info['posted_to_telegram']}")
            print(f"   По статусам: {info['status_counts']}")
    
    elif command == "create":
        print("🔧 Инициализация базы данных...")
        print("✅ База данных готова к работе!")
    
    elif command == "backup":
        backup_path = db_manager.backup_database()
        if backup_path:
            print(f"✅ Резервная копия: {backup_path}")
    
    elif command == "clear":
        confirm = input("⚠️  Вы уверены, что хотите удалить ВСЕ данные? (y/n): ")
        if confirm.lower() in ['y']:
            db_manager.clear_database()
        else:
            print("❌ Операция отменена")
    
    else:
        print(f"❌ Неизвестная команда: {command}")

if __name__ == "__main__":
    main()