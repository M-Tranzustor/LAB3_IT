from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_teacher, orm_get_teachers, orm_delete_teacher, orm_get_teacher, \
    orm_update_teacher
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.inline import get_callback_btns
from kbds.reply import start_kb2, get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Додати інфо-картку",
    "Переглянути всі інфо-картки викладачів",
    placeholder="Виберіть дію",
    sizes=(1, 1),
)
class AddTeachers(StatesGroup):
    full_name = State()
    description = State()
    image = State()

    teacher_for_change = None

    texts = {
        'AddTeachers:full_name': 'Введіть повторно Прізвище Імя Побатькові викладача',
        'AddTeachers:description': 'Введіть повторно інформацію про викладача',
        'AddTeachers:image': 'Завантажте фото викладача повторно'
    }

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Що ви хочете зробити?", reply_markup=ADMIN_KB)

##  ПЕрегляд карток і їх редагування
@admin_router.message(F.text == "Переглянути всі інфо-картки викладачів")
async def starring_at_product(message: types.Message, session: AsyncSession):
    await message.answer("ОК, список інфо-карточок викладачів")
    for teacher in await orm_get_teachers(session):
        await message.answer_photo(
            teacher.image,
            caption=f"<strong>{teacher.name}\
            </strong>\n{teacher.description}\n",
            reply_markup=get_callback_btns(btns={
                'Видалити': f'delete_{teacher.id}',
                'Редагувати': f'change_{teacher.id}'})
        )

## РЕакція на кнопки ВИДАЛИТИ
@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_teacher(session, int(product_id))
    ### Для телеграма команда
    await callback.answer("Інфо-картка видалена",True)
    await callback.message.answer("Інфо-картка видалена!")


#для call back query РЕДАГУВАННЯ
@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_teacher_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]

    teacher_for_change = await orm_get_teacher(session, int(product_id))

    AddTeachers.teacher_for_change = teacher_for_change

    await callback.answer()
    await callback.message.answer(
        "Введіть ПІБ викладача", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddTeachers.full_name)

# @admin_router.message(F.text == "Редагувати інфо-картку")
# async def change_product(message: types.Message):
#     await message.answer("ОК, список інфо-карточок викладачів")
#
#
# @admin_router.message(F.text == "Видалити інфо-картку")
# async def delete_product(message: types.Message):
#     await message.answer("Виберіть інфо-картку(и) для видалення")


#Код знизу для машини станів (FSM)



@admin_router.message(StateFilter(None), F.text == "Додати інфо-картку")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введіть ПІБ викладача", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddTeachers.full_name)


@admin_router.message(StateFilter('*'),Command("скасувати"))
@admin_router.message(StateFilter('*'),F.text.casefold() == "скасувати")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return
    if AddTeachers.teacher_for_change:
        AddTeachers.teacher_for_change = None

    await state.clear()
    await message.answer("Дія скасована", reply_markup=ADMIN_KB)



@admin_router.message(StateFilter('*'),Command("назад"))
@admin_router.message(StateFilter('*'),F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddTeachers.full_name:
        await message.answer("Введіть повторно Прізвище Ім'я Побатькові викладача, або напишіть 'Скасувати'")
        return

    previous = None
    for step in AddTeachers.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"ок, ви повернулися до попереднього кроку \n {AddTeachers.texts[previous.state]}")
        previous = step

#  В  в  і  д    П  І  Б
@admin_router.message(AddTeachers.full_name, or_f(F.text, F.text == '.'))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(full_name=AddTeachers.teacher_for_change.name)

    else:
        if len(message.text) >=100:
             await message.answer("Ви помилилися, ПІБ викладача не повинно бути таким довгим")
             return

        await state.update_data(full_name=message.text)
    await message.answer("Введіть інформацію про викладача")
    await state.set_state(AddTeachers.description)


@admin_router.message(AddTeachers.full_name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Ви припустилися помилки при введенні даних, введіть ПІБ викладача повторно")


#В  в  і  д     О   П  И  С  У      В   И  К  Л  А  Д  А  Ч  А.
@admin_router.message(AddTeachers.description, or_f(F.text, F.text == '.'))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(description=AddTeachers.teacher_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Завантажте фото викладача")
    await state.set_state(AddTeachers.image)



@admin_router.message(AddTeachers.description)
async def add_description(message: types.Message, state: FSMContext):
    await message.answer("Ви припустилися помилки при введенні даних, введіть інформацію про викладача повторно")


'''''''''
@admin_router.message(F.text)
async def add_price(message: types.Message, state: FSMContext):
    await message.answer("Завантажте фото викладача")
'''''''''
# З  А  В  А  Н  Т  А  Ж  Е  Н  Н  Я     Ф  О  Т  О     В  И  К  Л  А  Д  А  Ч  А
@admin_router.message(AddTeachers.image, or_f(F.photo, F.text == '.'))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):

    if message.text and message.text == '.':
        await state.update_data(image=AddTeachers.teacher_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddTeachers.teacher_for_change:
            await orm_update_teacher(session, AddTeachers.teacher_for_change.id, data)
        else:
            await orm_add_teacher(session, data) # В нього product
        await message.answer("Інфо-картка додана", reply_markup=ADMIN_KB)
        await state.clear()
    # Додавання в бд

    except Exception as e:
        await message.answer(
            f"Помилка: \n{str(e)}\nЗверніться до програміста, знову він щось начудив", reply_markup= ADMIN_KB)
        await state.clear()

    AddTeachers.teacher_for_change = None








#@admin_router.message(AddTeachers.image)
#async def add_image(message: types.Message, state: FSMContext):
 #   await message.answer("Ви припустилися помилки при введенні даних, завантажте фото викладача повторно")


 # наші дані вивід в чат.



####Збереження даних в базі даних.
    ##await message.answer(str(data))
