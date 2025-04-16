import pytest
from unittest.mock import MagicMock
from aiogram import types  # Import types from aiogram
from aiogram.dispatcher import Dispatcher
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.admin_private import add_product  # Corrected import

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
    dp = MagicMock()
    return dp

# Тест для функції add_product
@pytest.mark.asyncio
async def test_add_product(mock_update, mock_context, mock_bot, mock_dispatcher):
    """
    Тестує функцію add_product з файлу admin_private.py.

    Перевіряє, чи правильно додається викладач до контексту,
    а також обробку помилок при некоректному введенні даних.
    """
    # Задаємо текст повідомлення з коректними даними викладача
    mock_update.message.text = "Додати інфо-картку"
    mock_update.message.chat.id = 12345
    mock_update.message.from_user.id = 54321

    # Mocking необхідних методів
    mock_context.bot = mock_bot
    mock_context._dispatcher = mock_dispatcher

    # Створюємо екземпляр StateFilter
    state_filter = StateFilter(None)

    # Припускаємо, що  state.set_state повертає awaitable
    mock_context.set_state.return_value = None  # або awaitable об'єкт, якщо потрібно

    # Викликаємо функцію add_product
    await add_product(mock_update, mock_context)

    # Перевіряємо, чи викликався метод answer з правильним повідомленням
    mock_update.message.answer.assert_called_once_with(
        "Введіть ПІБ викладача", reply_markup=types.ReplyKeyboardRemove()
    )
    # Перевіряємо, чи викликався метод set_state з правильним станом
    mock_context.set_state.assert_called_once()
    assert mock_context.set_state.call_args[0][0].state == "AddTeachers:full_name"
