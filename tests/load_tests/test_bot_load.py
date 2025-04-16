import time
from locust import HttpUser, task, between

class TelegramBotLoadTest(HttpUser):
    """
    Клас, що представляє користувача, який надсилає запити до Telegram-бота.
    """
    #wait_time = between(1, 5)  # Затримка між запитами користувача (випадкове значення від 1 до 5 секунд)
    host = "https://api.telegram.org"  # Базовий URL API Telegram

    def on_start(self):
        """
        Метод, що виконується при запуску кожного користувача.
        Тут можна отримати токен бота з конфігурації або змінної оточення.
        """
        self.bot_token = "7077081400:AAG0SnZuf6FQObHexSBqGwJx75CidxjFgn4"  # Замініть на токен вашого бота!
        if not self.bot_token:
            raise ValueError("Bot token is not set. Please configure it in the 'bot_token' variable.")
        self.chat_id = 1735938530  # Замініть на ID чату, куди надсилати запити (можна отримати динамічно, якщо потрібно)

    @task
    def send_start_command(self):
        """
        Метод, що імітує надсилання команди /start боту.
        """
        payload = {
            "chat_id": self.chat_id,
            "text": "/start"
        }
        url = f"/bot{self.bot_token}/sendMessage"  # Формуємо URL для надсилання повідомлення
        with self.client.post(url, json=payload, catch_response=True) as response: # Відправляємо POST запит
            if response.status_code != 200:
                response.failure(f"Failed to send /start command: {response.text}") # Позначаємо запит як невдалий у випадку помилки

    @task
    def send_hello_message(self):
        """
        Метод, що імітує надсилання текстового повідомлення боту
        """
        payload = {
            "chat_id": self.chat_id,
            "text": "Привіт!"
        }
        url = f"/bot{self.bot_token}/sendMessage"  # Формуємо URL для надсилання повідомлення
        with self.client.post(url, json=payload, catch_response=True) as response: # Відправляємо POST запит
            if response.status_code != 200:
                 response.failure(f"Failed to send Привіт command: {response.text}") # Позначаємо запит як невдалий у випадку помилки
