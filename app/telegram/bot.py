import aiohttp
import asyncio
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramBotManager:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def send_new_item(self, item_data, description=None, images=None):
        """
        Отправляет новое объявление в канал
        
        Args:
            item_data (dict): Данные объявления из API Авито {id, title, price, status, url}
            description (str, optional): Описание с парсера страницы
            images (list, optional): Список URL изображений
            
        Returns:
            dict or None: {message_id: int, has_photo: bool} или None при ошибке
        """
        try:
            message_text = self._format_new_item_message(item_data, description)
            
            if images and len(images) > 0:
                message_id = await self._send_photo_message(images[0], message_text)
                has_photo = True
            else:
                message_id = await self._send_text_message(message_text)
                has_photo = False
            
            if message_id:
                print(f"✅ Новое объявление отправлено в Telegram: ID {item_data['id']}")
                return {
                    'message_id': message_id,
                    'has_photo': has_photo
                }
            else:
                print(f"❌ Ошибка отправки объявления ID {item_data['id']}")
                return None
                
        except Exception as e:
            print(f"❌ Исключение при отправке нового объявления: {e}")
            return None
    
    async def edit_item_status(self, message_id, item_data, new_status, has_photo=False):
        """
        Редактирует статус объявления в существующем сообщении
        
        Args:
            message_id (int): ID сообщения в Telegram для редактирования
            item_data (dict): Данные объявления {id, title, price, url}
            new_status (str): Новый статус (active, removed, old, blocked, etc.)
            has_photo (bool): True если сообщение содержит фото
            
        Returns:
            bool: True если редактирование прошло успешно, False при ошибке
        """
        try:
            updated_text = self._format_updated_item_message(item_data, new_status)
            
            if has_photo:
                success = await self._edit_message_caption(message_id, updated_text)
            else:
                success = await self._edit_message_text(message_id, updated_text)
            
            if success:
                status_emoji = self._get_status_emoji(new_status)
                print(f"✅ Статус обновлен {status_emoji}: ID {item_data['id']} -> {new_status}")
                return True
            else:
                print(f"❌ Ошибка обновления статуса для ID {item_data['id']}")
                return False
                
        except Exception as e:
            print(f"❌ Исключение при обновлении статуса: {e}")
            return False
    
    def _format_new_item_message(self, item_data, description=None):
        """Форматирует сообщение для нового объявления"""
        if item_data.get('price'):
            price_text = f"{item_data['price']:,}".replace(',', ' ') + " ₽"
        else:
            price_text = "Цена не указана"
        
        message = f"""🆕 **НОВОЕ ОБЪЯВЛЕНИЕ**

📝 **{item_data['title']}**

💰 **Цена:** {price_text}
🟢 **Статус:** АКТИВНО

"""
        
        if description:
            max_desc_length = 500
            if len(description) > max_desc_length:
                short_description = description[:max_desc_length] + "..."
            else:
                short_description = description
            
            message += f"📄 **Описание:**\n{short_description}\n\n"
        
        if item_data.get('url'):
            message += f"🔗 [Перейти к объявлению]({item_data['url']})\n\n"
        
        message += f"🆔 ID: `{item_data['id']}`"
        
        return message
    
    def _format_updated_item_message(self, item_data, new_status):
        """Форматирует сообщение для обновления статуса"""
        if item_data.get('price'):
            price_text = f"{item_data['price']:,}".replace(',', ' ') + " ₽"
        else:
            price_text = "Цена не указана"
        
        status_emoji = self._get_status_emoji(new_status)
        status_text = self._get_status_text(new_status)
        
        message = f"""{status_emoji} **{status_text.upper()}**

📝 **{item_data['title']}**

💰 **Цена:** {price_text}
📊 **Статус:** {status_text}

"""
        
        if item_data.get('url'):
            message += f"🔗 [Ссылка на объявление]({item_data['url']})\n\n"
        
        message += f"🆔 ID: `{item_data['id']}`"
        
        return message
    
    def _get_status_emoji(self, status):
        """Возвращает эмодзи для статуса"""
        status_emojis = {
            'active': '🟢',
            'removed': '✅',
            'old': '✅', 
            'blocked': '⛔',
            'rejected': '❌',
            'removed_from_api': '🚫'
        }
        return status_emojis.get(status, '❓')
    
    def _get_status_text(self, status):
        """Возвращает читаемый текст для статуса"""
        status_texts = {
            'active': 'В продаже',
            'removed': 'Продано',
            'old': 'Продано',
            'blocked': 'Заблокировано',
            'rejected': 'Отклонено',
            'removed_from_api': 'Недоступно'
        }
        return status_texts.get(status, 'Неизвестный статус')
    
    async def _send_text_message(self, text):
        """Отправляет текстовое сообщение"""
        url = f"{self.base_url}/sendMessage"
        
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('ok'):
                        return result['result']['message_id']
                    else:
                        print(f"❌ Telegram API ошибка: {result}")
                        return None
                else:
                    error_text = await response.text()
                    print(f"❌ HTTP ошибка при отправке текста: {response.status} - {error_text}")
                    return None
    
    async def _send_photo_message(self, photo_url, caption):
        """Отправляет сообщение с фото"""
        url = f"{self.base_url}/sendPhoto"
        
        data = {
            'chat_id': self.chat_id,
            'photo': photo_url,
            'caption': caption,
            'parse_mode': 'Markdown'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('ok'):
                        return result['result']['message_id']
                    else:
                        print(f"❌ Telegram API ошибка при отправке фото: {result}")
                        print("🔄 Пробуем отправить как текстовое сообщение...")
                        return await self._send_text_message(caption)
                else:
                    error_text = await response.text()
                    print(f"❌ HTTP ошибка при отправке фото: {response.status} - {error_text}")
                    return await self._send_text_message(caption)
    
    async def _edit_message_text(self, message_id, new_text):
        """Редактирует текст существующего текстового сообщения"""
        url = f"{self.base_url}/editMessageText"
        
        data = {
            'chat_id': self.chat_id,
            'message_id': message_id,
            'text': new_text,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('ok'):
                        return True
                    else:
                        print(f"❌ Telegram API ошибка при редактировании текста: {result}")
                        return False
                else:
                    error_text = await response.text()
                    print(f"❌ HTTP ошибка при редактировании сообщения {message_id}: {response.status} - {error_text}")
                    return False
    
    async def _edit_message_caption(self, message_id, new_caption):
        """Редактирует подпись существующего сообщения с фото"""
        url = f"{self.base_url}/editMessageCaption"
        
        data = {
            'chat_id': self.chat_id,
            'message_id': message_id,
            'caption': new_caption,
            'parse_mode': 'Markdown'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('ok'):
                        return True
                    else:
                        print(f"❌ Telegram API ошибка при редактировании подписи: {result}")
                        return False
                else:
                    error_text = await response.text()
                    print(f"❌ HTTP ошибка при редактировании подписи {message_id}: {response.status} - {error_text}")
                    return False
    
    async def test_connection(self):
        """Тестирует подключение к боту и получает информацию о нем"""
        url = f"{self.base_url}/getMe"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('ok'):
                            bot_info = result['result']
                            print(f"✅ Бот подключен успешно:")
                            print(f"   Имя: {bot_info['first_name']}")
                            print(f"   Username: @{bot_info['username']}")
                            print(f"   ID: {bot_info['id']}")
                            return True
                        else:
                            print(f"❌ Ошибка API при тестировании: {result}")
                            return False
                    else:
                        error_text = await response.text()
                        print(f"❌ HTTP ошибка при тестировании: {response.status} - {error_text}")
                        return False
        except Exception as e:
            print(f"❌ Исключение при тестировании бота: {e}")
            return False


async def test_telegram_bot():
    """Функция для тестирования Telegram Bot Manager"""
    print("🧪 Тестируем Telegram Bot Manager...")
    
    bot = TelegramBotManager()
    
    # Тестируем подключение
    if not await bot.test_connection():
        print("❌ Не удалось подключиться к боту")
        return
    
    # Тестовые данные объявления
    test_item = {
        'id': 12345678,
        'title': 'Тестовое объявление - iPhone 12 Pro Max',
        'price': 85000,
        'status': 'active',
        'url': 'https://www.avito.ru/test'
    }
    
    test_description = "Тестовое описание товара. Продаю iPhone в отличном состоянии."
    test_images = ['https://via.placeholder.com/300x200?text=Test+Image']
    
    print("\n📤 Тестируем отправку нового объявления...")
    result = await bot.send_new_item(test_item, test_description, test_images)
    
    if result:
        message_id = result['message_id']
        has_photo = result['has_photo']
        print(f"✅ Сообщение отправлено с ID: {message_id} (с фото: {has_photo})")
        
        print("\n⏳ Ждем 3 секунды перед тестированием редактирования...")
        await asyncio.sleep(3)
        
        print("📝 Тестируем редактирование статуса...")
        success = await bot.edit_item_status(message_id, test_item, 'removed', has_photo)
        
        if success:
            print("✅ Статус успешно изменен")
        else:
            print("❌ Ошибка при изменении статуса")
    else:
        print("❌ Ошибка при отправке сообщения")


if __name__ == "__main__":
    asyncio.run(test_telegram_bot())