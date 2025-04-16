import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.user_private import all_search_cmd

# Фікстура для створення мок-об'єкта message
@pytest.fixture
def mock_message():
    message = MagicMock(spec=types.Message)
    message.answer_photo = AsyncMock()  # Мокаємо метод answer_photo
    return message

# Фікстура для створення мок-об'єкта сесії SQLAlchemy
@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session

# Фікстура для створення мок-об'єкта викладача
@pytest.fixture
def mock_teacher():
    """
    Фікстура, що повертає мок-об'єкт викладача з тестовими даними.
    """
    teacher = MagicMock()
    teacher.name = "Іван Іваненко"
    teacher.description = "Доцент кафедри"
    teacher.image = b"binary_image_data"  # Мокова бінарні дані зображення
    return teacher

# Мокаємо функцію orm_get_teachers
@patch("handlers.user_private.orm_get_teachers")  # Виправлено імпорт для patch
async def test_all_search_cmd_with_teachers(mock_orm_get_teachers, mock_message, mock_session, mock_teacher):
    """
    Тестує функцію all_search_cmd при наявності викладачів у базі даних.

    Перевіряє, чи викликається метод answer_photo для кожного викладача
    з правильними аргументами.
    """
    # Налаштовуємо mock_orm_get_teachers так, щоб вона повертала список мокових викладачів
    mock_orm_get_teachers.return_value = [mock_teacher, mock_teacher]  # Повертаємо список з двома викладачами

    # Викликаємо функцію, яку тестуємо
    await all_search_cmd(mock_message, mock_session)

    # Перевіряємо, чи викликався метод answer_photo двічі (для кожного викладача)
    assert mock_message.answer_photo.call_count == 2

    # Перевіряємо, чи правильні аргументи передавалися в перший виклик answer_photo
    mock_message.answer_photo.assert_any_call(
        mock_teacher.image,  # Перевіряємо передане зображення
        caption="<strong>Іван Іваненко            </strong>\nДоцент кафедри\n",  # Перевіряємо підпис
    )

    # Перевіряємо, чи правильні аргументи передавалися в другий виклик answer_photo
    mock_message.answer_photo.assert_any_call(
        mock_teacher.image,  # Знову перевіряємо передане зображення
        caption="<strong>Іван Іваненко            </strong>\nДоцент кафедри\n",  # Перевіряємо підпис
    )

@patch("handlers.user_private.orm_get_teachers")  # Виправлено імпорт для patch
async def test_all_search_cmd_no_teachers(mock_orm_get_teachers, mock_message, mock_session):
    """
    Тестує функцію all_search_cmd, коли в базі даних немає викладачів.

    Перевіряє, чи не викликається метод answer_photo.
    """
    # Налаштовуємо mock_orm_get_teachers так, щоб вона повертала порожній список
    mock_orm_get_teachers.return_value = []

    # Викликаємо функцію, яку тестуємо
    await all_search_cmd(mock_message, mock_session)

    # Перевіряємо, чи не викликався метод answer_photo взагалі
    mock_message.answer_photo.assert_not_called()
