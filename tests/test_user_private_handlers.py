import pytest
from unittest.mock import MagicMock, AsyncMock
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.context import FSMContext
from handlers.user_private import start_cmd
from kbds.reply import get_keyboard  # Import get_keyboard

# Фікстури для мокання об'єктів
@pytest.fixture
def mock_update():
    """Фікстура для створення мок-об'єкта Update."""
    update = MagicMock(spec=types.Update)
    update.message = MagicMock(spec=types.Message)
    update.message.chat = MagicMock(spec=types.Chat)
    update.message.from_user = MagicMock(spec=types.User)
    return update

@pytest.fixture
def mock_context():
    """Фікстура для створення мок-об'єкта CallbackContext."""
    context = MagicMock(spec=FSMContext)
    context.chat_data = {}
    return context

@pytest.fixture
def mock_bot():
    """Фікстура для створення мок-об'єкта Bot."""
    bot = MagicMock()
    return bot

@pytest.fixture
def mock_dispatcher():
    """Фікстура для створення мок-об'єкта Dispatcher."""
    dp = Dispatcher()
    return dp

# Тестування команди /start
@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context, mock_bot, mock_dispatcher):
    """
    Тестує обробник команди /start у файлі user_private.py.

    Перевіряє, чи повертає функція правильне привітання.
    """
    mock_update.message.text = "/start"
    mock_update.message.chat.id = 12345

    # Мокуємо bot та dispatcher для context
    mock_context.bot = mock_bot
    mock_context._dispatcher = mock_dispatcher

    # Налаштовуємо mock_update.message.answer для повернення корутини
    mock_update.message.answer = AsyncMock()  # Use AsyncMock here

    # Викликаємо обробник
    await start_cmd(mock_update.message)

    # Перевіряємо, чи викликався метод answer з правильним текстом
    mock_update.message.answer.assert_called_once_with(
        "Привіт я бот, який допомогає студентам знайти важливу інформацію про викладачів",
        reply_markup=get_keyboard(
            "Пошук",
            "Меню",
            "Про проект",
            placeholder="Оберіть дію",
            sizes=(1, 1, 1)),
    )
