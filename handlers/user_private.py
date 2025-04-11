from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_teacher, orm_get_teachers
from filters.chat_types import ChatTypeFilter
from kbds import reply
from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard
from handlers.admin_private import ADMIN_KB

from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)  # Italic, as_numbered_list и тд

# Розідлення фільтрів для привату і груп
user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))




# Основне меню

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привіт я бот, який допомогає студентам знайти важливу інформацію про викладачів",
        reply_markup=get_keyboard(
    "Пошук",
    "Меню",
    "Про проект",
    placeholder="Оберіть дію",
    sizes=(1, 1, 1)),
    )
# функція яка реагує на старт і відправляє повідомлення про початок роботи бота.
#@user_private_router.message(CommandStart())
#async def start_cmd(message: types.Message):
  #  await message.answer("Привіт я бот, який допомогає студентам знайти важливу інформацію про викладачів", reply_markup=reply.start_kb)


# M       E      N       U
@user_private_router.message(F.text.lower().contains('меню'))
@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for teacher in await orm_get_teachers(session):
        await message.answer_photo(
            teacher.image,
            caption=f"<strong>{teacher.name}\
            </strong>\n{teacher.description}\n"
        )
    #Відправленіня меню на команду /меню
    await message.answer("<b>Виберіть інститут потрібного викладача</b>", reply_markup=reply.del_kbd)


    ## інший варіант відповіді. ## await bot.send_message(message.from_user.id,'Відповідь')
   ## await message.answer(message.text)
  ## Відповідь на повідомлення користувача з іменем користувача.
   ## await message.reply(message.text)


# A      B       O       U        T
@user_private_router.message(F.text.lower().contains('Про проект'))
@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer("Тут ви знайдете потрібну інформацію про викладачів.")

    """"""""""
    # Відповіді бота на стандартні повідомлення( привіт, допобачення)
    text = message.text
    if text in ['Привіт','hi','Hello','Здоров','Чіназес','Прив','ку','куку','Йов']:
        await message.answer('Привіт!!!')

    elif text in ['Пака','До побачення','Допобачення','Давай','пока','Пака','Тєряйся','Усьо']:
        await message.answer('До зустрічі, кайфуй!!!')

    else:
         await message.answer(message.text)
"""""""""""""""""""""

# S    E     A     R     C       H
@user_private_router.message(F.text.lower().contains('шук'))
@user_private_router.message(Command('search'))
async def search_cmd(message: types.Message):
    await message.answer("Оберіть спосіб пошуку викладачів", reply_markup=get_keyboard(
    "За кафедрою",
    "За прізвищем",
    "Вивести всіх викладачів",

    placeholder="Оберіть спосіб пошуку викладачів",
    sizes=(1, 1, 1)),
    )

####     В  И  В  І  Д       В   С   І   Х  В   И   К   Л   А  Д  А   Ч  І   В
@user_private_router.message(F.text.lower().contains('всіх'))
@user_private_router.message(Command('Вивести всіх викладачів'))
async def all_search_cmd(message: types.Message, session: AsyncSession):
    for teacher in await orm_get_teachers(session):
        await message.answer_photo(
            teacher.image,
            caption=f"<strong>{teacher.name}\
            </strong>\n{teacher.description}\n",
        )

# М  А  Г  І  Ч  Н  І        Ф   І   Л   Ь   Т   Р   И

## Т  Е   К   С   Т
# Привітання
@user_private_router.message(F.text.lower() == 'привіт')
async def text_cmd(message: types.Message):
    await message.answer("Привіт друже)")
    
# Прощання
@user_private_router.message(F.text.lower() == 'давай')
async def text_cmd(message: types.Message):
    await message.answer("Звертайся)")

#
@user_private_router.message(F.text.lower().contains('Виклад'))
async def text_cmd(message: types.Message):
    await message.answer("Якщо ви хочете знайти інфо-картку потрібного викладача, напишіть команду /search")

## Рандом текст
@user_private_router.message(F.text)
async def text_cmd(message: types.Message):
    await message.answer("Класно вмієш писати)")


## Ф  О   Т   О
@user_private_router.message(F.photo)
async def foto_cmd(message: types.Message):
    await message.answer("Класна фотка)")