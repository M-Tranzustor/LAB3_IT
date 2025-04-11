import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.strategy import FSMStrategy

#Імпорт TOKEN з файлу
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession


#from middlewares.db import CounterMiddleware

from handlers import user_private
from database.engine import create_db, drop_db, session_maker


from handlers.admin_private import admin_router
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router

# Користувацікі команди.

from common.bot_cmds_list import private

## Обмеження на повідомлення які може отримувати бот від ТГ
#ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'),parse_mode=ParseMode.HTML)
# Список адмінів чату.
bot.my_admins_list = []

dp = Dispatcher(fsm_strategy = FSMStrategy.USER_IN_CHAT)
# БД підключення


## Підключаємо адмін роутер до диспетчера.
dp.include_router(admin_router)
## Підключаємо приватний роутер до диспетчера.
dp.include_router(user_private_router)
## Підключаємо груповий роутер до диспетчера.
dp.include_router(user_group_router)



'''''''''''
# функція яка реагує на старт і відправляє повідомлення про початок роботи бота.
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('оберіть інститут( це була команда старт)')


# ЕХО для бота.
@dp.message()
async def echo(message: types.Message):

  ## інший варіант відповіді. ## await bot.send_message(message.from_user.id,'Відповідь')
    await message.answer(message.text)

  ## Відповідь на повідомлення користувача з іменем користувача.
    await message.reply(message.text)
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
'''''''''''

# Функції для запуску та завершення роботи бота.
async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('Бот заснув')






async def main():
    # ЗАПУСК БАЗИ ДАНИХ
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    #await create_db
    # функція для видалення повідомлень, які надійшли боту коли він був не в онлайн.
    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_my_commands(commands=private,scope=types.BotCommandScopeAllPrivateChats())
## код для перепризначення меню новими кнопками.
       #await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())