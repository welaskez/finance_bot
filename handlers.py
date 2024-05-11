from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from datetime import datetime

from database import Database
from messages import get_today_wastes_msg
import keyboards as kb

router = Router()


class UserState(StatesGroup):
    waste = State()
    category = State()
    operation = State()


@router.callback_query(F.data == 'main')
@router.message(CommandStart())
async def start_cmd(message: Message | CallbackQuery):
    if isinstance(message, CallbackQuery):
        await message.message.edit_text(
            text=f'Привет {message.from_user.full_name}!\nЭто бот для учета финансов.',
            reply_markup=kb.start
        )
    else:
        await message.answer(
            text=f'Привет {message.from_user.full_name}!\nЭто бот для учета финансов.',
            reply_markup=kb.start
        )


@router.callback_query(F.data == 'add_waste')
async def add_waste_cmd(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.operation)
    db = Database()
    current_categories = db.get_categories()
    await callback.message.edit_text(
        text='Выбери категорию: ',
        reply_markup=kb.current_categories_markup(current_categories)
    )
    await state.update_data(operation='add_waste')


@router.callback_query(F.data == 'check_wastes')
async def check_wastes_cmd(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'Твои траты за сегодня:\n{get_today_wastes_msg()}',
        reply_markup=kb.check_wastes
    )


@router.callback_query(F.data == 'settings')
async def settings_cmd(callback: CallbackQuery):
    await callback.message.edit_text('Настройки: ', reply_markup=kb.settings)


@router.callback_query(F.data == 'categories')
async def categories_cmd(callback: CallbackQuery):
    await callback.message.edit_text('Категории: ', reply_markup=kb.categories)


@router.callback_query(F.data == 'add_category')
async def add_category_cmd(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.category)
    await callback.message.edit_text('Напиши название категории: ', reply_markup=kb.add_category)
    await state.update_data(message_id=callback.message.message_id)


@router.message(UserState.category)
async def handle_add_category(message: Message, state: FSMContext, bot: Bot):
    db = Database()

    await message.delete()

    await state.update_data(category=message.text)
    data = await state.get_data()
    await state.clear()

    db.add_category(data['category'])
    await bot.edit_message_text(
        text=f'Ты успешно добавил категорию {data["category"]}',
        chat_id=message.from_user.id,
        message_id=data['message_id'],
        reply_markup=kb.success_add_category
    )


@router.callback_query(F.data == 'delete_category')
async def delete_category_cmd(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.operation)

    db = Database()
    current_categories = db.get_categories()
    await callback.message.edit_text(
        text='Выбери категорию из списка: ',
        reply_markup=kb.current_categories_markup(current_categories)
    )
    await state.update_data(operation='delete_category')


@router.callback_query(lambda callback: callback.data.startswith('category_'), UserState.operation)
async def handle_delete_category(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    db = Database()
    state_data = await state.get_data()
    await state.clear()
    if state_data['operation'] == 'delete_category':
        db.delete_category(data[1])
        await callback.message.edit_text(
            text=f'Категория {data[1]} успешно удалена!',
            reply_markup=kb.success_delete_category
        )
    elif state_data['operation'] == 'add_waste':
        await state.set_state(UserState.waste)
        await callback.message.edit_text('Напиши сумму:')
        await state.update_data(message_id=callback.message.message_id, category=data[1])


@router.message(UserState.waste)
async def handle_add_waste(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(waste=message.text)
    await message.delete()

    db = Database()

    data = await state.get_data()
    await state.clear()

    db.add_waste(data['category'], int(data['waste']), str(datetime.now().strftime('%Y-%m-%d')))
    await bot.edit_message_text(
        text=f'Трата успешно добавлена!',
        chat_id=message.from_user.id,
        message_id=data['message_id'],
        reply_markup=kb.success_add_waste
    )


@router.callback_query(F.data == 'statistics')
async def statistics_cmd(callback: CallbackQuery):
    await callback.message.edit_text('Выбери период: ', reply_markup=kb.statistics)
