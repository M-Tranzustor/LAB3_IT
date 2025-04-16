# tests/test_admin_private.py

import pytest
from unittest.mock import MagicMock, AsyncMock # Додав AsyncMock про всяк випадок
from aiogram import types
# Видали цей рядок:
# from aiogram.dispatcher import Dispatcher
from aiogram.filters import StateFilter # Це коректний імпорт для v3
from aiogram.fsm.context import FSMContext # Це коректний імпорт для v3

# Важливо: Перевір шлях імпорту до твого admin_private!
# Якщо він у папці handlers:
from handlers.admin_private import add_product, AddTeachers # Імпортуємо також клас стану

# --- Змінимо фікстури та тест для більшої відповідності aiogram v3 ---

@pytest.fixture
def mock_message(mocker): # Перейменуємо і спростимо
    """Фікстура для створення мок-об'єкта Message."""
    message = mocker.MagicMock(spec=types.Message)
    message.chat = mocker.MagicMock(spec=types.Chat)
    message.from_user = mocker.MagicMock(spec=types.User)
    # Імітуємо метод answer як асинхронний
    message.answer = AsyncMock()
    return message

@pytest.fixture
def mock_state(mocker): # Перейменуємо
    """Фікстура для створення мок-об'єкта FSMContext."""
    state = mocker.MagicMock(spec=FSMContext)
    # Імітуємо set_state як асинхронний
    state.set_state = AsyncMock()
    # Якщо твій код використовує update_data або get_data, їх теж треба зробити AsyncMock
    # state.update_data = AsyncMock(return_value={})
    # state.get_data = AsyncMock(return_value={})
    return state

# Фікстури mock_bot та mock_dispatcher не потрібні для цього тесту,
# бо add_product приймає лише message і state

# --- Виправлений тест ---

@pytest.mark.asyncio
# ↓↓↓ Використовуємо оновлені фікстури ↓↓↓
async def test_add_product_starts_correctly(mock_message, mock_state):
    """
    Тестує початковий виклик функції add_product.
    Перевіряє правильність відповіді та встановлення стану.
    """
    # Arrange
    # Задаємо текст повідомлення (хоча для add_product він не використовується,
    # бо це обробник команди або конкретного тексту, наприклад "Додати інфо-картку")
    mock_message.text = "Додати інфо-картку" # Або текст твоєї команди/фільтра
    mock_message.chat.id = 12345
    mock_message.from_user.id = 54321

    # Act
    # ↓↓↓ Викликаємо функцію з правильними аргументами ↓↓↓
    await add_product(mock_message, mock_state)

    # Assert
    # ↓↓↓ Перевіряємо виклик mock_message.answer ↓↓↓
    mock_message.answer.assert_called_once_with(
        "Введіть ПІБ викладача", reply_markup=types.ReplyKeyboardRemove()
    )
    # ↓↓↓ Перевіряємо виклик mock_state.set_state ↓↓↓
    mock_state.set_state.assert_called_once_with(AddTeachers.full_name)