import asyncio
from string import punctuation

from aiogram import F, Bot, types, Router

from aiogram.filters import Command
from filters.chat_types import ChatTypeFilter
#from common.restricted_words import restricted_words

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group","supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))
restricted_words = {'підор','залупа','даун','сука','єбав','шлюха','соси','йди нахуй','маму єбав'}
# Функція для забору id адмінів групи.

@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    #подивитися дані  і властивості отриманих обєктів
    #print(admins_list)
    # код нижче- це генератор списку x = [i for i in range(10)]
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    print(admins_list)



# Фільтр нецензурних слів.
def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        # Повідомлення для порушника
        await message.answer(f"{message.from_user.first_name}, дотримуйтеся порядку в чаті!)")
        #
        await message.delete()
        ## Команда для бану цього користувача
        await message.chat.ban(message.from_user.id)
