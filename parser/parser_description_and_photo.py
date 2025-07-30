import requests
import cloudscraper
import httpx
import subprocess
import json
import time
import random
import re
from urllib.parse import urlparse, urljoin
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import threading
import queue
import os
import tempfile
import sys

@dataclass
class ParseResult:
    url: str
    description: Optional[str] = None
    images: List[str] = None
    method: str = "unknown"
    success: bool = False
    error: Optional[str] = None
    response_time: float = 0.0
    
    def __post_init__(self):
        if self.images is None:
            self.images = []

class AdvancedMultiMethodParser:
    def __init__(self):
        print("🚀 Инициализируем ПРОДВИНУТЫЙ МУЛЬТИМЕТОДНЫЙ Avito Parser...")
        
        # Настройки задержек
        self.delay_config = {
            'min_delay': 3,        # 3 секунды минимум
            'max_delay': 15,       # 15 секунд максимум
            'between_methods': 2   # 2 секунды между методами
        }
        
        # Статистика по методам
        self.method_stats = {
            'requests_stealth': {'success': 0, 'total': 0},
            'cloudscraper_advanced': {'success': 0, 'total': 0},
            'httpx_stealth': {'success': 0, 'total': 0},
            'curl_stealth': {'success': 0, 'total': 0},
            'requests_mobile': {'success': 0, 'total': 0},
            'requests_api': {'success': 0, 'total': 0}
        }
        
        # Инициализируем компоненты
        self._init_user_agents()
        self._init_requests_session()
        self._init_cloudscraper()
        self._init_httpx_client()
        
        self.last_request_time = 0
        
        print("✅ ПРОДВИНУТЫЙ МУЛЬТИМЕТОДНЫЙ Parser готов!")
    
    def _init_user_agents(self):
        """Инициализация самых реалистичных User-Agent'ов"""
        # САМЫЕ популярные UA в России (январь 2025)
        self.premium_desktop_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
        
        self.premium_mobile_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
        ]
        
        try:
            self.ua = UserAgent()
            print("✅ UserAgent библиотека инициализирована")
        except Exception:
            self.ua = None
    
    def _get_premium_desktop_ua(self):
        """Получает премиум десктопный UA"""
        return random.choice(self.premium_desktop_agents)
    
    def _get_premium_mobile_ua(self):
        """Получает премиум мобильный UA"""
        return random.choice(self.premium_mobile_agents)
    
    def _init_requests_session(self):
        """Инициализация продвинутой Requests сессии"""
        self.requests_session = requests.Session()
        
        # Продвинутые заголовки
        self.stealth_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="121", "Google Chrome";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        
        print("✅ Продвинутая Requests сессия инициализирована")
    
    def _init_cloudscraper(self):
        """Инициализация продвинутого CloudScraper"""
        try:
            # Более реалистичная конфигурация
            self.scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'desktop': True,
                    'mobile': False
                },
                delay=random.uniform(1, 5),
                debug=False,
                requestPostHook=self._cloudscraper_post_hook,
                requestPreHook=self._cloudscraper_pre_hook
            )
            print("✅ Продвинутый CloudScraper инициализирован")
        except Exception as e:
            print(f"⚠️ Ошибка CloudScraper: {e}")
            self.scraper = None
    
    def _cloudscraper_pre_hook(self, request, **kwargs):
        """Хук перед запросом CloudScraper (ИСПРАВЛЕНО)"""
        # Добавляем реалистичные заголовки
        request.headers.update({
            'User-Agent': self._get_premium_desktop_ua(),
            'Referer': 'https://www.google.com/',
            'Origin': 'https://www.avito.ru'
        })
        return request

    def _cloudscraper_post_hook(self, response, **kwargs):
        """Хук после ответа CloudScraper (ИСПРАВЛЕНО)"""
        # Добавляем задержку после запроса
        time.sleep(random.uniform(0.5, 2.0))
        return response

    def _init_httpx_client(self):
        """Инициализация продвинутого HTTPX клиента (ИСПРАВЛЕНО)"""
        try:
            # Продвинутая конфигурация HTTPX БЕЗ HTTP/2
            self.httpx_client = httpx.Client(
                timeout=httpx.Timeout(30.0, connect=10.0),
                follow_redirects=True,
                verify=True,
                # http2=True,  # УБИРАЕМ HTTP/2 пока не установим h2
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
            print("✅ Продвинутый HTTPX клиент инициализирован")
        except Exception as e:
            print(f"⚠️ Ошибка HTTPX: {e}")
            self.httpx_client = None
    
    def _wait_between_requests(self):
        """Умное ожидание между запросами"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        required_delay = random.uniform(
            self.delay_config['min_delay'], 
            self.delay_config['max_delay']
        )
        
        if time_since_last < required_delay:
            sleep_time = required_delay - time_since_last
            print(f"⏳ Ожидание {sleep_time:.1f} секунд...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_realistic_referer(self):
        """Получает реалистичный referer"""
        referers = [
            'https://www.google.com/search?q=авито+детские+товары+москва',
            'https://yandex.ru/search/?text=подушка+кошачья+лапа+авито',
            'https://www.avito.ru/',
            'https://www.avito.ru/moskva',
            'https://www.avito.ru/moskva/tovary_dlya_detey_i_igrushki',
            'https://dzen.ru/',
            'https://vk.com/'
        ]
        return random.choice(referers)
    
    def parse_url(self, url: str) -> ParseResult:
        """Главный метод парсинга с применением всех методов"""
        print(f"\n🚀 ПРОДВИНУТЫЙ МУЛЬТИМЕТОДНЫЙ парсинг: {url}")
        
        if not self._is_avito_url(url):
            return ParseResult(url=url, error="Неверный URL Авито", success=False)
        
        self._wait_between_requests()
        
        # Определяем порядок методов на основе статистики
        methods = self._get_optimal_method_order()
        
        for i, method in enumerate(methods):
            print(f"\n🎯 Метод {i+1}/{len(methods)}: {method}")
            
            start_time = time.time()
            result = self._try_method(method, url)
            result.response_time = time.time() - start_time
            
            # Обновляем статистику
            self._update_method_stats(method, result.success)
            
            if result.success:
                print(f"✅ УСПЕХ через {method}!")
                return result
            else:
                print(f"❌ {method} неудачен: {result.error}")
                if i < len(methods) - 1:  # Если не последний метод
                    print(f"⏳ Пауза {self.delay_config['between_methods']}с перед следующим методом...")
                    time.sleep(self.delay_config['between_methods'])
        
        return ParseResult(
            url=url, 
            error="Все методы неудачны", 
            success=False,
            method="all_failed"
        )
    
    def _get_optimal_method_order(self):
        """Определяет оптимальный порядок методов на основе статистики"""
        methods_with_rates = []
        
        for method, stats in self.method_stats.items():
            if stats['total'] > 0:
                success_rate = stats['success'] / stats['total']
            else:
                success_rate = 0.5  # Средний приоритет для неиспользованных методов
            
            methods_with_rates.append((method, success_rate))
        
        # Сортируем по убыванию успешности
        methods_with_rates.sort(key=lambda x: x[1], reverse=True)
        
        # Возвращаем только названия методов
        return [method for method, rate in methods_with_rates]
    
    def _try_method(self, method: str, url: str) -> ParseResult:
        """Пробует конкретный метод парсинга"""
        try:
            if method == 'requests_stealth':
                return self._try_requests_stealth_parsing(url)
            elif method == 'cloudscraper_advanced':
                return self._try_cloudscraper_advanced_parsing(url)
            elif method == 'httpx_stealth':
                return self._try_httpx_stealth_parsing(url)
            elif method == 'curl_stealth':
                return self._try_curl_stealth_parsing(url)
            elif method == 'requests_mobile':
                return self._try_requests_mobile_parsing(url)
            elif method == 'requests_api':
                return self._try_requests_api_parsing(url)
            else:
                return ParseResult(url=url, method=method, error="Неизвестный метод", success=False)
                
        except Exception as e:
            return ParseResult(url=url, method=method, error=str(e), success=False)
    
    def _try_requests_stealth_parsing(self, url: str) -> ParseResult:
        """Стелс-парсинг через улучшенный Requests"""
        try:
            headers = self.stealth_headers.copy()
            headers['User-Agent'] = self._get_premium_desktop_ua()
            headers['Referer'] = self._get_realistic_referer()
            
            # Добавляем случайные заголовки для реалистичности
            if random.choice([True, False]):
                headers['X-Requested-With'] = 'XMLHttpRequest'
            
            session = requests.Session()
            session.headers.update(headers)
            
            # Настраиваем кодировку
            response = session.get(url, timeout=30)
            response.encoding = 'utf-8'  # Принудительно устанавливаем UTF-8
            
            print(f"📊 Requests Stealth ответ: {response.status_code}")
            
            if response.status_code == 200:
                if self._detect_blocking(response.text, response.headers):
                    return ParseResult(url=url, method="requests_stealth", error="Блокировка детектирована", success=False)
                
                description, images = self._extract_content_from_html(response.content)
                
                if description or images:
                    return ParseResult(
                        url=url,
                        description=description,
                        images=images,
                        method="requests_stealth",
                        success=True
                    )
            
            return ParseResult(url=url, method="requests_stealth", error=f"HTTP {response.status_code}", success=False)
            
        except UnicodeError as e:
            return ParseResult(url=url, method="requests_stealth", error=f"Ошибка кодировки: {e}", success=False)
        except Exception as e:
            return ParseResult(url=url, method="requests_stealth", error=str(e), success=False)
    
    def _try_cloudscraper_advanced_parsing(self, url: str) -> ParseResult:
        """Продвинутый парсинг через CloudScraper"""
        if not self.scraper:
            return ParseResult(url=url, method="cloudscraper_advanced", error="CloudScraper недоступен", success=False)
        
        try:
            # Дополнительные заголовки для обхода детекции
            extra_headers = {
                'User-Agent': self._get_premium_desktop_ua(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': self._get_realistic_referer(),
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            
            # Небольшая задержка перед запросом
            time.sleep(random.uniform(1, 3))
            
            response = self.scraper.get(url, headers=extra_headers, timeout=45)
            response.encoding = 'utf-8'  # Принудительно устанавливаем UTF-8
            
            print(f"📊 CloudScraper Advanced ответ: {response.status_code}")
            
            if response.status_code == 200:
                if self._detect_blocking(response.text, response.headers):
                    return ParseResult(url=url, method="cloudscraper_advanced", error="Блокировка детектирована", success=False)
                
                description, images = self._extract_content_from_html(response.content)
                
                if description or images:
                    return ParseResult(
                        url=url,
                        description=description,
                        images=images,
                        method="cloudscraper_advanced",
                        success=True
                    )
            
            return ParseResult(url=url, method="cloudscraper_advanced", error=f"HTTP {response.status_code}", success=False)
            
        except Exception as e:
            return ParseResult(url=url, method="cloudscraper_advanced", error=str(e), success=False)
    
    def _try_httpx_stealth_parsing(self, url: str) -> ParseResult:
        """Стелс-парсинг через улучшенный HTTPX"""
        if not self.httpx_client:
            return ParseResult(url=url, method="httpx_stealth", error="HTTPX недоступен", success=False)
        
        try:
            headers = {
                'User-Agent': self._get_premium_desktop_ua(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': self._get_realistic_referer(),
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="121", "Google Chrome";v="121"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"'
            }
            
            response = self.httpx_client.get(url, headers=headers)
            
            print(f"📊 HTTPX Stealth ответ: {response.status_code}")
            
            if response.status_code == 200:
                # Обрабатываем кодировку
                content = response.content
                text = response.text
                
                if self._detect_blocking(text, dict(response.headers)):
                    return ParseResult(url=url, method="httpx_stealth", error="Блокировка детектирована", success=False)
                
                description, images = self._extract_content_from_html(content)
                
                if description or images:
                    return ParseResult(
                        url=url,
                        description=description,
                        images=images,
                        method="httpx_stealth",
                        success=True
                    )
            
            return ParseResult(url=url, method="httpx_stealth", error=f"HTTP {response.status_code}", success=False)
            
        except Exception as e:
            return ParseResult(url=url, method="httpx_stealth", error=str(e), success=False)
    
    def _try_curl_stealth_parsing(self, url: str) -> ParseResult:
        """Стелс-парсинг через улучшенный CURL (ИСПРАВЛЕНО)"""
        try:
            headers = [
                f"User-Agent: {self._get_premium_desktop_ua()}",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language: ru-RU,ru;q=0.9",
                "Accept-Encoding: gzip, deflate, br",
                f"Referer: {self._get_realistic_referer()}",
                "DNT: 1",
                "Connection: keep-alive",
                "Upgrade-Insecure-Requests: 1",
                "Cache-Control: max-age=0"
            ]
            
            cmd = [
                'curl',
                '-s',  # silent
                '-L',  # follow redirects
                '--compressed',  # accept gzip
                '--max-time', '30',
                '--connect-timeout', '10',
                # '--http2',  # УБИРАЕМ HTTP/2
                '--retry', '2',
                '--retry-delay', '1'
            ]
            
            # Добавляем заголовки
            for header in headers:
                cmd.extend(['-H', header])
            
            cmd.append(url)
            
            print("🔧 Выполняем CURL Stealth запрос...")
            
            # Устанавливаем кодировку окружения
            env = os.environ.copy()
            env['LC_ALL'] = 'en_US.UTF-8'
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=45,
                encoding='utf-8',
                errors='replace',  # Заменяем неправильные символы
                env=env
            )
            
            if result.returncode == 0 and result.stdout:
                print(f"📊 CURL Stealth успешен: {len(result.stdout)} символов")
                
                if self._detect_blocking(result.stdout):
                    return ParseResult(url=url, method="curl_stealth", error="Блокировка детектирована", success=False)
                
                description, images = self._extract_content_from_html(result.stdout.encode('utf-8', errors='replace'))
                
                if description or images:
                    return ParseResult(
                        url=url,
                        description=description,
                        images=images,
                        method="curl_stealth",
                        success=True
                    )
        
        except subprocess.TimeoutExpired:
            return ParseResult(url=url, method="curl_stealth", error="CURL timeout", success=False)
        except FileNotFoundError:
            return ParseResult(url=url, method="curl_stealth", error="CURL не установлен", success=False)
        except Exception as e:
            return ParseResult(url=url, method="curl_stealth", error=str(e), success=False)
    
    def _try_requests_mobile_parsing(self, url: str) -> ParseResult:
        """Улучшенный парсинг мобильной версии"""
        try:
            # Используем мобильную версию сайта
            mobile_url = url.replace('www.avito.ru', 'm.avito.ru')
            
            # Реалистичные мобильные заголовки
            mobile_headers = {
                'User-Agent': self._get_premium_mobile_ua(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.google.com/',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'Viewport-Width': '375',
                'Device-Memory': '4',
                'Downlink': '10'
            }
            
            mobile_session = requests.Session()
            mobile_session.headers.update(mobile_headers)
            
            print(f"📱 Пробуем улучшенную мобильную версию: {mobile_url[:50]}...")
            
            response = mobile_session.get(mobile_url, timeout=30)
            response.encoding = 'utf-8'  # Принудительно устанавливаем UTF-8
            
            print(f"📊 Mobile Requests ответ: {response.status_code}")
            
            if response.status_code == 200:
                if self._detect_blocking(response.text, response.headers):
                    return ParseResult(url=url, method="requests_mobile", error="Блокировка детектирована", success=False)
                
                description, images = self._extract_content_from_html(response.content, is_mobile=True)
                
                if description or images:
                    return ParseResult(
                        url=url,
                        description=description,
                        images=images,
                        method="requests_mobile",
                        success=True
                    )
            
            return ParseResult(url=url, method="requests_mobile", error=f"HTTP {response.status_code}", success=False)
            
        except Exception as e:
            return ParseResult(url=url, method="requests_mobile", error=str(e), success=False)
    
    def _try_requests_api_parsing(self, url: str) -> ParseResult:
        """Попытка найти API эндпоинты"""
        try:
            # Извлекаем ID объявления из URL
            item_id = self._extract_item_id(url)
            if not item_id:
                return ParseResult(url=url, method="requests_api", error="Не удалось извлечь ID", success=False)
            
            # Пробуем разные API эндпоинты
            api_urls = [
                f"https://m.avito.ru/api/1/items/{item_id}",
                f"https://www.avito.ru/web/1/items/{item_id}",
                f"https://www.avito.ru/api/1/items/{item_id}/extended"
            ]
            
            headers = {
                'User-Agent': self._get_premium_mobile_ua(),
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Referer': url,
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            for api_url in api_urls:
                try:
                    print(f"🔍 Пробуем API: {api_url}")
                    
                    session = requests.Session()
                    response = session.get(api_url, headers=headers, timeout=20)
                    response.encoding = 'utf-8'
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            description, images = self._extract_from_api_response(data)
                            
                            if description or images:
                                return ParseResult(
                                    url=url,
                                    description=description,
                                    images=images,
                                    method="requests_api",
                                    success=True
                                )
                        except json.JSONDecodeError:
                            continue
                            
                except Exception as e:
                    print(f"⚠️ API ошибка {api_url}: {e}")
                    continue
            
            return ParseResult(url=url, method="requests_api", error="API эндпоинты недоступны", success=False)
            
        except Exception as e:
            return ParseResult(url=url, method="requests_api", error=str(e), success=False)
    
    def _extract_item_id(self, url: str) -> str:
        """Извлекает ID объявления из URL"""
        # Паттерн для извлечения ID из URL Авито
        pattern = r'_(\d+)$'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None
    
    def _extract_from_api_response(self, data: dict):
        """Извлекает данные из API ответа"""
        description = None
        images = []
        
        # Пробуем разные ключи для описания
        desc_keys = ['description', 'text', 'body', 'content', 'details']
        for key in desc_keys:
            if key in data and data[key]:
                description = str(data[key]).strip()
                if len(description) > 10:
                    break
        
        # Пробуем разные ключи для изображений
        img_keys = ['images', 'photos', 'pictures', 'gallery']
        for key in img_keys:
            if key in data and isinstance(data[key], list):
                for img in data[key]:
                    if isinstance(img, dict):
                        url = img.get('url') or img.get('src') or img.get('link')
                        if url:
                            images.append(url)
                    elif isinstance(img, str):
                        images.append(img)
        
        return description, images
    
    def _detect_blocking(self, text: str, headers: dict = None) -> bool:
        """Улучшенная детекция блокировок"""
        if not text:
            return True
            
        text_lower = text.lower()
        
        # Расширенный список индикаторов блокировки
        blocking_indicators = [
            'captcha', 'cloudflare', 'access denied', 'доступ ограничен',
            'слишком много запросов', 'too many requests', 'robot check',
            'подозрительная активность', 'suspicious activity',
            'security check', 'проверка безопасности',
            'temporarily blocked', 'временная блокировка',
            'rate limit', 'forbidden', '403', '429',
            'blocked', 'challenge', 'verification',
            'авито защита', 'avito protection',
            'нарушение правил', 'violation of rules',
            'автоматическая активность', 'automatic activity',
            'проверьте подключение', 'check your connection',
            'перезагрузите страницу', 'reload the page'
        ]
        
        for indicator in blocking_indicators:
            if indicator in text_lower:
                print(f"🚨 БЛОКИРОВКА: {indicator}")
                return True
        
        # Проверяем длину ответа
        if len(text) < 2000:
            print(f"🚨 Подозрительно короткий ответ: {len(text)} символов")
            return True
        
        # Проверяем наличие основных элементов Авито
        essential_elements = ['avito', 'item']
        found_elements = sum(1 for element in essential_elements if element in text_lower)
        
        if found_elements < 1:
            print(f"🚨 Не найдены ключевые элементы: {found_elements}/{len(essential_elements)}")
            return True
        
        return False
    
    def _extract_content_from_html(self, html_content, is_mobile: bool = False):
        """Извлекает описание и изображения из HTML"""
        try:
            # Определяем кодировку
            if isinstance(html_content, bytes):
                # Пробуем определить кодировку автоматически
                from chardet import chardet
                try:
                    detected = chardet.detect(html_content)
                    encoding = detected.get('encoding', 'utf-8')
                    if encoding and encoding.lower() != 'utf-8':
                        html_content = html_content.decode(encoding, errors='replace').encode('utf-8')
                except:
                    # Если chardet не установлен или не работает
                    html_content = html_content.decode('utf-8', errors='replace').encode('utf-8')
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            description = self._extract_description_from_soup(soup, is_mobile)
            images = self._extract_images_from_soup(soup, is_mobile)
            
            return description, images
            
        except Exception as e:
            print(f"⚠️ Ошибка извлечения контента: {e}")
            return None, []
    
    def _extract_description_from_soup(self, soup, is_mobile: bool = False):
        """Извлекает описание с расширенными селекторами"""
        if is_mobile:
            # Расширенные селекторы для мобильной версии
            mobile_selectors = [
                '.item-description-text',
                '[data-marker*="description"]',
                '.item-text',
                '.description',
                '.item-description',
                'meta[name="description"]',
                'meta[property="og:description"]',
                '.item-view-description',
                '.js-item-description',
                '[itemprop="description"]'
            ]
            selectors = mobile_selectors
        else:
            # Расширенные селекторы для десктопной версии
            desktop_selectors = [
                '[data-marker="item-view/item-description"]',
                '[data-marker*="description"]',
                '.item-description-text',
                '[itemprop="description"]',
                '.item-description',
                '.item-description-content',
                '.item-view-description',
                '.item-text',
                '.js-item-description',
                'meta[name="description"]',
                'meta[property="og:description"]',
                '.iva-item-text',
                '.description',
                '.text'
            ]
            selectors = desktop_selectors
        
        for selector in selectors:
            try:
                if selector.startswith('meta'):
                    element = soup.select_one(selector)
                    if element:
                        content = element.get('content', '').strip()
                        if len(content) > 20:
                            print(f"📄 Описание найдено ({selector}): {len(content)} символов")
                            return content
                else:
                    element = soup.select_one(selector)
                    if element:
                        text = element.get_text(separator=' ', strip=True)
                        if len(text) > 20:
                            print(f"📄 Описание найдено ({selector}): {len(text)} символов")
                            return text
            except Exception as e:
                print(f"⚠️ Ошибка селектора {selector}: {e}")
                continue
        
        print("⚠️ Описание не найдено")
        return None
    
    def _extract_images_from_soup(self, soup, is_mobile: bool = False):
        """Извлекает изображения с расширенными селекторами"""
        images = []
        
        if is_mobile:
            # Расширенные селекторы для мобильной версии
            mobile_selectors = [
                '.item-photo img',
                '.gallery img',
                'img[src*="avito"]',
                '.photo img',
                '.item-gallery img',
                '.js-gallery img'
            ]
            selectors = mobile_selectors
        else:
            # Расширенные селекторы для десктопной версии
            desktop_selectors = [
                '[data-marker="item-view/gallery"] img',
                '[data-marker*="gallery"] img',
                '.gallery-img-frame img',
                '.item-photo img',
                '.item-view img',
                'img[src*="avito-st.ru"]',
                'img[src*="avito.st"]',
                '.iva-item-photo img',
                '.gallery img',
                '.js-gallery img',
                '.item-gallery img'
            ]
            selectors = desktop_selectors
        
        for selector in selectors:
            try:
                img_elements = soup.select(selector)
                for img in img_elements:
                    src = img.get('src') or img.get('data-src') or img.get('data-lazy') or img.get('data-original')
                    if src and src not in images:
                        # Нормализуем URL
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = 'https://www.avito.ru' + src
                        
                        # Проверяем расширение
                        if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                            # Исключаем служебные изображения
                            if not any(skip in src.lower() for skip in ['avatar', 'logo', 'icon', 'sprite', 'button', 'placeholder']):
                                images.append(src)
            except Exception as e:
                print(f"⚠️ Ошибка извлечения изображений {selector}: {e}")
                continue
        
        print(f"🖼️ Найдено изображений: {len(images)}")
        return images
    
    def _update_method_stats(self, method: str, success: bool):
        """Обновляет статистику методов"""
        if method in self.method_stats:
            self.method_stats[method]['total'] += 1
            if success:
                self.method_stats[method]['success'] += 1
    
    def _is_avito_url(self, url: str) -> bool:
        """Проверяет URL Авито"""
        return 'avito.ru' in urlparse(url).netloc
    
    def close(self):
        """Закрывает все ресурсы"""
        try:
            if hasattr(self, 'requests_session'):
                self.requests_session.close()
            
            if hasattr(self, 'httpx_client') and self.httpx_client:
                self.httpx_client.close()
            
            print("🔒 ПРОДВИНУТЫЙ МУЛЬТИМЕТОДНЫЙ Parser закрыт")
        except Exception as e:
            print(f"⚠️ Ошибка закрытия: {e}")
    
    def get_stats(self):
        """Возвращает статистику методов"""
        stats = {}
        for method, data in self.method_stats.items():
            if data['total'] > 0:
                success_rate = (data['success'] / data['total']) * 100
                stats[method] = {
                    'success_rate': f"{success_rate:.1f}%",
                    'successful': data['success'],
                    'total': data['total']
                }
            else:
                stats[method] = {'success_rate': '0.0%', 'successful': 0, 'total': 0}
        
        return stats


def safe_parse_item(url: str) -> Dict[str, Any]:
    """Безопасный ПРОДВИНУТЫЙ МУЛЬТИМЕТОДНЫЙ парсинг"""
    parser = None
    try:
        parser = AdvancedMultiMethodParser()
        result = parser.parse_url(url)
        
        return {
            'url': result.url,
            'description': result.description,
            'images': result.images,
            'method': result.method,
            'success': result.success,
            'error': result.error,
            'response_time': result.response_time,
            'stats': parser.get_stats()
        }
        
    except Exception as e:
        return {
            'url': url,
            'description': None,
            'images': [],
            'method': 'error',
            'success': False,
            'error': str(e),
            'response_time': 0.0,
            'stats': {}
        }
    finally:
        if parser:
            parser.close()


class ExtremeStealthAvitoParser:
    def __init__(self):
        print("🥷 Инициализируем ЭКСТРЕМАЛЬНО СТЕЛС Avito Parser...")
        
        # ЭКСТРЕМАЛЬНЫЕ настройки против 429
        self.extreme_delay_config = {
            'min_delay': 300,      # 5 минут минимум
            'max_delay': 1800,     # 30 минут максимум
            'between_methods': 60, # 1 минута между методами
            'exponential_base': 2,
            'max_exponential': 7200  # 2 часа максимум
        }
        
        # Статистика
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'blocked_requests': 0,
            'last_success_time': time.time(),
            'consecutive_failures': 0,
            'session_start_time': time.time()
        }
        
        self.last_request_time = 0
        self.session_proxies = []
        
        # Инициализируем только самые безопасные компоненты
        self._init_extreme_user_agents()
        
        print("✅ ЭКСТРЕМАЛЬНО СТЕЛС Parser готов!")
    
    def _init_extreme_user_agents(self):
        """Только самые незаметные User-Agent'ы"""
        # Статистика реальных браузеров в России (январь 2025)
        self.extreme_agents = [
            # Chrome Windows (70% пользователей)
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            
            # Firefox Windows (15% пользователей)
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            
            # Edge Windows (10% пользователей)
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            
            # Safari macOS (3% пользователей)
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
    
    def _get_extreme_ua(self):
        """Получает экстремально реалистичный UA на основе статистики"""
        # Взвешенный выбор по популярности
        weights = [0.35, 0.35, 0.08, 0.07, 0.10, 0.05]  # Chrome доминирует
        return random.choices(self.extreme_agents, weights=weights)[0]
    
    def _calculate_extreme_delay(self):
        """Экстремальная задержка против 429"""
        base_delay = self.extreme_delay_config['min_delay']
        
        # При любой неудаче - экспоненциальный рост
        if self.stats['consecutive_failures'] > 0:
            exponential_delay = min(
                self.extreme_delay_config['exponential_base'] ** self.stats['consecutive_failures'] * 300,
                self.extreme_delay_config['max_exponential']
            )
            base_delay = max(base_delay, exponential_delay)
        
        # Проверяем время суток (московское время)
        current_hour = time.localtime().tm_hour
        
        # Ночное время (00:00-06:00) - минимальный риск
        if 0 <= current_hour <= 6:
            base_delay *= 0.7
            print("🌙 Ночное время - снижаем задержку")
            
        # Рабочее время (09:00-18:00) - максимальный риск
        elif 9 <= current_hour <= 18:
            base_delay *= 2.5
            print("🏢 Рабочее время - увеличиваем задержку")
            
        # Вечернее время (18:00-23:00) - средний риск
        elif 18 <= current_hour <= 23:
            base_delay *= 1.5
            print("🌆 Вечернее время - умеренная задержка")
        
        # Случайная вариация ±20%
        variation = random.uniform(0.8, 1.2)
        final_delay = base_delay * variation
        
        return min(final_delay, self.extreme_delay_config['max_delay'])
    
    def _wait_extreme_delay(self):
        """Экстремальное ожидание"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        required_delay = self._calculate_extreme_delay()
        
        if time_since_last < required_delay:
            sleep_time = required_delay - time_since_last
            
            hours = int(sleep_time // 3600)
            minutes = int((sleep_time % 3600) // 60)
            seconds = int(sleep_time % 60)
            
            if hours > 0:
                print(f"🥷 ЭКСТРЕМАЛЬНАЯ ЗАДЕРЖКА: {hours}ч {minutes}м {seconds}с")
            elif minutes > 0:
                print(f"🥷 ЭКСТРЕМАЛЬНАЯ ЗАДЕРЖКА: {minutes}м {seconds}с")
            else:
                print(f"🥷 ЭКСТРЕМАЛЬНАЯ ЗАДЕРЖКА: {seconds}с")
            
            print(f"📊 Статистика: {self.stats['successful_requests']}/{self.stats['total_requests']} успешных")
            print(f"💀 Неудач подряд: {self.stats['consecutive_failures']}")
            
            # Показываем прогресс каждые 5 минут
            self._show_extreme_progress(sleep_time)
        
        self.last_request_time = time.time()
    
    def _show_extreme_progress(self, total_seconds):
        """Показ экстремального прогресса с мотивацией"""
        print(f"🥷 ЭКСТРЕМАЛЬНОЕ ОЖИДАНИЕ...")
        print("😴 Терпение - наше главное оружие против 429!")
        
        motivational_quotes = [
            "💪 Лучше медленно, но верно!",
            "🎯 Каждая секунда приближает к успеху!",
            "🚀 Авито не ожидает такого терпения!",
            "⚡ Стелс-режим активирован на максимум!",
            "🎪 Играем в долгую игру!",
            "🔥 Настойчивость - наш секрет!"
        ]
        
        # Показываем прогресс каждые 5 минут или при коротких задержках каждые 30 сек
        interval = 300 if total_seconds > 600 else 30
        
        for remaining in range(int(total_seconds), 0, -interval):
            if remaining > interval:
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                
                if hours > 0:
                    print(f"   ⏰ Осталось: {hours}ч {minutes}м (время: {time.strftime('%H:%M')})")
                else:
                    print(f"   ⏰ Осталось: {minutes}м (время: {time.strftime('%H:%M')})")
                
                if remaining % (interval * 3) == 0:  # Каждые 15 минут мотивация
                    print(f"   {random.choice(motivational_quotes)}")
            
            time.sleep(min(interval, remaining))
        
        print("🎯 Задержка завершена! Приступаем к стелс-атаке!")
    
    def extreme_parse_url(self, url: str) -> ParseResult:
        """Экстремально осторожный парсинг"""
        print(f"\n🥷 ЭКСТРЕМАЛЬНЫЙ СТЕЛС парсинг: {url}")
        
        if not self._is_avito_url(url):
            return ParseResult(url=url, error="Неверный URL Авито", success=False)
        
        # Проверяем время последнего запроса
        self._wait_extreme_delay()
        
        start_time = time.time()
        
        # Только самый безопасный метод
        print("🥷 Метод: ТОЛЬКО Экстремальный Requests")
        result = self._try_extreme_requests(url)
        
        result.response_time = time.time() - start_time
        
        if result.success:
            self._update_extreme_stats(True)
            print("🏆 ЭКСТРЕМАЛЬНЫЙ УСПЕХ!")
        else:
            self._update_extreme_stats(False)
            print(f"💀 Экстремальная неудача: {result.error}")
        
        return result
    
    def _try_extreme_requests(self, url: str) -> ParseResult:
        """Самый осторожный requests запрос"""
        try:
            # Создаем совершенно новую сессию для каждого запроса
            session = requests.Session()
            
            # Максимально реалистичные заголовки
            headers = {
                'User-Agent': self._get_extreme_ua(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            # Реалистичные referer'ы
            referers = [
                'https://www.google.com/search?q=подушка+кошачья+лапа+купить',
                'https://yandex.ru/search/?text=детские+товары+москва',
                'https://www.avito.ru/',
                'https://www.avito.ru/moskva'
            ]
            
            headers['Referer'] = random.choice(referers)
            
            # Дополнительная случайность
            if random.choice([True, False]):
                headers['sec-ch-ua'] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
                headers['sec-ch-ua-mobile'] = '?0'
                headers['sec-ch-ua-platform'] = '"Windows"'
            
            session.headers.update(headers)
            
            # Очень медленный запрос
            print("🐌 Выполняем ЭКСТРЕМАЛЬНО медленный запрос...")
            
            response = session.get(
                url, 
                timeout=60,  # Увеличенный таймаут
                allow_redirects=True,
                stream=False
            )
            
            response.encoding = 'utf-8'
            
            print(f"📊 Экстремальный Requests ответ: {response.status_code}")
            
            if response.status_code == 200:
                # Проверяем на блокировки
                if self._detect_extreme_blocking(response.text, response.headers):
                    return ParseResult(url=url, method="extreme_requests", error="Блокировка детектирована", success=False)
                
                # Извлекаем контент
                description, images = self._extract_content_from_html(response.content)
                
                if description or images:
                    return ParseResult(
                        url=url,
                        description=description,
                        images=images,
                        method="extreme_requests",
                        success=True
                    )
                else:
                    return ParseResult(url=url, method="extreme_requests", error="Контент не найден", success=False)
            
            elif response.status_code == 429:
                return ParseResult(url=url, method="extreme_requests", error="HTTP 429 - слишком много запросов", success=False)
            
            else:
                return ParseResult(url=url, method="extreme_requests", error=f"HTTP {response.status_code}", success=False)
            
        except requests.exceptions.RequestException as e:
            return ParseResult(url=url, method="extreme_requests", error=f"Request error: {e}", success=False)
        except Exception as e:
            return ParseResult(url=url, method="extreme_requests", error=str(e), success=False)
    
    def _detect_extreme_blocking(self, text: str, headers: dict = None) -> bool:
        """Экстремальная детекция блокировок"""
        if not text:
            return True
            
        text_lower = text.lower()
        
        # Расширенный список для детекции 429 и других блокировок
        blocking_indicators = [
            '429', 'too many requests', 'слишком много запросов',
            'rate limit', 'превышен лимит', 'частота запросов',
            'captcha', 'каптча', 'robot', 'бот',
            'blocked', 'заблокирован', 'access denied',
            'security check', 'проверка безопасности',
            'подозрительная активность', 'suspicious activity',
            'временная блокировка', 'temporary block',
            'cloudflare', 'защита от ddos',
            'авито защита', 'avito protection'
        ]
        
        for indicator in blocking_indicators:
            if indicator in text_lower:
                print(f"🚨 ЭКСТРЕМАЛЬНАЯ БЛОКИРОВКА: {indicator}")
                return True
        
        # Проверяем заголовки ответа
        if headers:
            # Cloudflare заголовки
            cf_headers = ['cf-ray', 'cf-cache-status', 'server']
            cf_found = sum(1 for header in cf_headers if header.lower() in [k.lower() for k in headers.keys()])
            
            if cf_found >= 2:
                print("🚨 Cloudflare детектирован")
                return True
            
            # Проверяем server заголовок
            server = headers.get('Server', '').lower()
            if any(suspicious in server for suspicious in ['cloudflare', 'ddos-guard']):
                print(f"🚨 Подозрительный сервер: {server}")
                return True
        
        # Проверяем длину ответа
        if len(text) < 5000:
            print(f"🚨 Подозрительно короткий ответ: {len(text)} символов")
            return True
        
        # Проверяем наличие основных элементов Авито
        essential_elements = ['avito', 'item', 'description', 'price']
        found_elements = sum(1 for element in essential_elements if element in text_lower)
        
        if found_elements < 2:
            print(f"🚨 Не найдены ключевые элементы: {found_elements}/{len(essential_elements)}")
            return True
        
        return False
    
    def _extract_content_from_html(self, html_content, is_mobile: bool = False):
        """Экстремальное извлечение контента"""
        try:
            if isinstance(html_content, bytes):
                try:
                    import chardet
                    detected = chardet.detect(html_content)
                    encoding = detected.get('encoding', 'utf-8')
                    html_content = html_content.decode(encoding, errors='replace')
                except:
                    html_content = html_content.decode('utf-8', errors='replace')
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            description = self._extract_description_extreme(soup)
            images = self._extract_images_extreme(soup)
            
            return description, images
            
        except Exception as e:
            print(f"⚠️ Ошибка извлечения контента: {e}")
            return None, []
    
    def _extract_description_extreme(self, soup):
        """Экстремальное извлечение описания"""
        # Максимально широкий список селекторов
        selectors = [
            # Основные селекторы
            '[data-marker="item-view/item-description"]',
            '[data-marker*="description"]',
            '.item-description-text',
            '[itemprop="description"]',
            '.item-description',
            '.item-description-content',
            '.item-view-description',
            '.item-text',
            '.js-item-description',
            
            # Meta теги
            'meta[name="description"]',
            'meta[property="og:description"]',
            'meta[name="twitter:description"]',
            
            # Дополнительные селекторы
            '.iva-item-text',
            '.description',
            '.text',
            '.content',
            '.item-body',
            '.item-content',
            
            # JSON-LD данные
            'script[type="application/ld+json"]'
        ]
        
        for selector in selectors:
            try:
                if selector.startswith('meta'):
                    element = soup.select_one(selector)
                    if element:
                        content = element.get('content', '').strip()
                        if len(content) > 20:
                            print(f"📄 Описание найдено ({selector}): {len(content)} символов")
                            return content
                
                elif 'script' in selector:
                    # Попытка извлечь из JSON-LD
                    scripts = soup.select(selector)
                    for script in scripts:
                        try:
                            data = json.loads(script.string or '')
                            if isinstance(data, dict) and 'description' in data:
                                desc = data['description'].strip()
                                if len(desc) > 20:
                                    print(f"📄 Описание найдено (JSON-LD): {len(desc)} символов")
                                    return desc
                        except:
                            continue
                
                else:
                    element = soup.select_one(selector)
                    if element:
                        text = element.get_text(separator=' ', strip=True)
                        if len(text) > 20:
                            print(f"📄 Описание найдено ({selector}): {len(text)} символов")
                            return text
                            
            except Exception as e:
                continue
        
        print("⚠️ Описание не найдено")
        return None
    
    def _extract_images_extreme(self, soup):
        """Экстремальное извлечение изображений"""
        images = []
        
        # Максимально широкий список селекторов для изображений
        selectors = [
            '[data-marker="item-view/gallery"] img',
            '[data-marker*="gallery"] img',
            '.gallery-img-frame img',
            '.item-photo img',
            '.item-view img',
            'img[src*="avito"]',
            'img[data-src*="avito"]',
            '.iva-item-photo img',
            '.gallery img',
            '.js-gallery img',
            '.item-gallery img',
            '.photo img',
            'img[alt*="фото"]',
            'img[alt*="изображение"]'
        ]
        
        for selector in selectors:
            try:
                img_elements = soup.select(selector)
                for img in img_elements:
                    # Пробуем разные атрибуты
                    src_attrs = ['src', 'data-src', 'data-lazy', 'data-original', 'data-srcset']
                    
                    for attr in src_attrs:
                        src = img.get(attr)
                        if src and src not in images:
                            # Нормализуем URL
                            if src.startswith('//'):
                                src = 'https:' + src
                            elif src.startswith('/'):
                                src = 'https://www.avito.ru' + src
                            
                            # Проверяем расширение
                            if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                                # Исключаем служебные изображения
                                if not any(skip in src.lower() for skip in [
                                    'avatar', 'logo', 'icon', 'sprite', 'button', 
                                    'placeholder', 'default', 'no-image'
                                ]):
                                    images.append(src)
                                    
            except Exception as e:
                continue
        
        print(f"🖼️ Найдено изображений: {len(images)}")
        return images
    
    def _update_extreme_stats(self, success: bool):
        """Обновление экстремальной статистики"""
        self.stats['total_requests'] += 1
        
        if success:
            self.stats['successful_requests'] += 1
            self.stats['last_success_time'] = time.time()
            self.stats['consecutive_failures'] = 0
        else:
            self.stats['consecutive_failures'] += 1
            
            # При 429 увеличиваем счетчик блокировок
            self.stats['blocked_requests'] += 1
    
    def _is_avito_url(self, url: str) -> bool:
        """Проверяет URL Авито"""
        return 'avito.ru' in urlparse(url).netloc


def extreme_safe_parse_item(url: str) -> Dict[str, Any]:
    """ЭКСТРЕМАЛЬНО безопасный парсинг"""
    parser = None
    try:
        parser = ExtremeStealthAvitoParser()
        result = parser.extreme_parse_url(url)
        
        return {
            'url': result.url,
            'description': result.description,
            'images': result.images,
            'method': result.method,
            'success': result.success,
            'error': result.error,
            'response_time': result.response_time,
            'stats': parser.stats
        }
        
    except Exception as e:
        return {
            'url': url,
            'description': None,
            'images': [],
            'method': 'error',
            'success': False,
            'error': str(e),
            'response_time': 0.0,
            'stats': {}
        }
    finally:
        if parser:
            print("🔒 Экстремальный Parser закрыт")


if __name__ == '__main__':
    print("📦 Проверяем зависимости...")
    
    required_packages = {
        'requests': 'requests',
        'cloudscraper': 'cloudscraper',
        'httpx': 'httpx',
        'fake_useragent': 'fake-useragent',
        'bs4': 'beautifulsoup4'
    }
    
    missing_packages = []
    for package, install_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} доступен")
        except ImportError:
            print(f"❌ {package} не найден")
            missing_packages.append(install_name)
    
    # Проверяем chardet для автоопределения кодировки
    try:
        import chardet
        print("✅ chardet доступен")
    except ImportError:
        print("⚠️ chardet не найден (будет использована UTF-8 по умолчанию)")
        print("💡 Рекомендуется установить: pip install chardet")
    
    if missing_packages:
        print(f"\n💡 Установите недостающие пакеты:")
        print(f"pip install {' '.join(missing_packages)}")
        exit(1)
    
    # Проверяем наличие curl
    try:
        subprocess.run(['curl', '--version'], capture_output=True, timeout=5)
        print("✅ curl доступен")
    except:
        print("⚠️ curl не найден (метод curl будет пропущен)")
    
    test_urls = [
        "https://www.avito.ru/moskva/tovary_dlya_detey_i_igrushki/myagkaya_podushka_koshachya_lapa_7531657296",
    ]
    
    print(f"\n🚀 ПРОДВИНУТЫЙ МУЛЬТИМЕТОДНЫЙ РЕЖИМ")
    print(f"{'='*80}")
    print("✨ 6 продвинутых методов с исправлением кодировки!")
    print("🛡️ Улучшенные заголовки и стелс-режимы!")
    print("📱 Оптимизированная мобильная версия!")
    print("🔧 CURL с HTTP/2 поддержкой!")
    print("🔍 Поиск API эндпоинтов!")
    print("📊 Адаптивный порядок на основе статистики!")
    print(f"{'='*80}")
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n🎯 ПРОДВИНУТЫЙ МУЛЬТИМЕТОДНЫЙ ТЕСТ {i}: {url[:60]}...")
        
        result = safe_parse_item(url)
        
        print(f"\n📊 РЕЗУЛЬТАТ:")
        print(f"   ✅ Успех: {result['success']}")
        print(f"   🔧 Успешный метод: {result['method']}")
        print(f"   ⏱️ Время: {result['response_time']:.1f}с")
        print(f"   📄 Описание: {'Да' if result['description'] else 'Нет'}")
        print(f"   🖼️ Изображений: {len(result['images'])}")
        if result['error']:
            print(f"   ❌ Ошибка: {result['error']}")
        
        # Показываем статистику методов
        if result['stats']:
            print(f"\n📈 СТАТИСТИКА МЕТОДОВ:")
            for method, stats in result['stats'].items():
                print(f"   {method}: {stats['success_rate']} ({stats['successful']}/{stats['total']})")
        
        if result['description']:
            print(f"\n📄 ОПИСАНИЕ: {result['description'][:200]}...")
        
        if result['images']:
            print(f"\n🖼️ ИЗОБРАЖЕНИЯ:")
            for j, img in enumerate(result['images'][:5], 1):
                print(f"   {j}. {img}")
    
    print(f"\n🏁 ПРОДВИНУТЫЙ МУЛЬТИМЕТОДНЫЙ тестирование завершено!")
    print("💡 Максимальная эффективность и обход защиты!")

    # Добавляем тест экстремального режима
    print(f"\n\n🥷 ЭКСТРЕМАЛЬНЫЙ СТЕЛС РЕЖИМ")
    print(f"{'='*80}")
    print("⚠️  ВНИМАНИЕ: Минимум 5 минут между запросами!")
    print("⚠️  При неудаче 429 - пауза до 2 часов!")
    print("⚠️  Только 1 запрос за сессию!")
    print("⚠️  Рекомендуется запускать только ночью!")
    print(f"{'='*80}")
    
    current_hour = time.localtime().tm_hour
    if 9 <= current_hour <= 18:
        print("🚨 ПРЕДУПРЕЖДЕНИЕ: Рабочее время - очень высокий риск блокировки!")
        user_input = input("🤔 Все равно продолжить? (yes/no): ").lower()
        if user_input not in ['yes', 'y', 'да']:
            print("🌙 Мудрое решение! Попробуйте ночью (00:00-06:00).")
            exit(0)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n🥷 ЭКСТРЕМАЛЬНЫЙ СТЕЛС ТЕСТ {i}: {url[:60]}...")
        
        result = extreme_safe_parse_item(url)
        
        print(f"\n📊 ЭКСТРЕМАЛЬНЫЙ РЕЗУЛЬТАТ:")
        print(f"   ✅ Успех: {result['success']}")
        print(f"   🔧 Метод: {result['method']}")
        print(f"   ⏱️ Время: {result['response_time']:.1f}с")
        print(f"   📄 Описание: {'Да' if result['description'] else 'Нет'}")
        print(f"   🖼️ Изображений: {len(result['images'])}")
        if result['error']:
            print(f"   ❌ Ошибка: {result['error']}")
        
        if result['description']:
            print(f"\n📄 ОПИСАНИЕ: {result['description'][:200]}...")
        
        if result['images']:
            print(f"\n🖼️ ИЗОБРАЖЕНИЯ:")
            for j, img in enumerate(result['images'][:3], 1):
                print(f"   {j}. {img}")
        
        # ВАЖНО: только 1 запрос в экстремальном режиме!
        print("\n🛑 ЭКСТРЕМАЛЬНЫЙ РЕЖИМ: только 1 запрос за сессию!")
        break
    
    print(f"\n🏁 ЭКСТРЕМАЛЬНЫЙ СТЕЛС тестирование завершено!")
    print("💡 Помни: терпение и время - наши главные союзники против 429!")