from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# З відео

def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,),):

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:

            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)






# Клавіатура основний функціонал
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пошук"),
        ],
        [
            KeyboardButton(text="Меню"),
        ],
        [
            KeyboardButton(text="Про проект")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Оберіть дію'
)
# Клавіатура для пошуку
search_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
          KeyboardButton(text="За кафедрою")
        ],
        [
          KeyboardButton(text="За прізвищем")

        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Оберіть спосіб пошуку викладача'
)
# Видалення клавіатури
del_kbd = ReplyKeyboardRemove()

# Інший клас для клавіатур.

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text="Пошук"),
    KeyboardButton(text="Меню"),
    KeyboardButton(text="Про проект")
)
start_kb2.adjust(2,1,1)

# додавання додаткових пунктів клави.

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(text="Додати відгук"))


