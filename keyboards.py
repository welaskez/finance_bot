from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import List


def current_categories_markup(current_categories: List):
    kb = InlineKeyboardBuilder()

    for category in current_categories:
        kb.button(text=category[1], callback_data=f"category_{category[1]}")
    kb = kb.adjust(3, ).as_markup()
    kb.inline_keyboard.append([InlineKeyboardButton(text='Вернуться', callback_data='categories')])

    return kb


start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Внести трату', callback_data='add_waste')],
    [InlineKeyboardButton(text='Посмотреть траты', callback_data='check_wastes')],
    [InlineKeyboardButton(text='Настройки', callback_data='settings')]
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Категории', callback_data='categories')],
    [InlineKeyboardButton(text='Вернуться', callback_data='main')]
])

categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_category'),
     InlineKeyboardButton(text='Удалить', callback_data='delete_category')],
    [InlineKeyboardButton(text='Вернуться', callback_data='settings')]
])

add_category = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться', callback_data='categories')]
])

add_currency = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться', callback_data='currencies')]
])

success_add_category = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить еще', callback_data='add_category')],
    [InlineKeyboardButton(text='Вернуться', callback_data='categories')],
    [InlineKeyboardButton(text='На главную', callback_data='main')]
])

success_delete_category = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить еще', callback_data='delete_category')],
    [InlineKeyboardButton(text='Вернуться', callback_data='categories')],
    [InlineKeyboardButton(text='На главную', callback_data='main')]
])

success_add_waste = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть траты', callback_data='check_wastes')],
    [InlineKeyboardButton(text='Вернуться', callback_data='main')]
])

check_wastes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Внести трату', callback_data='add_waste')],
    [InlineKeyboardButton(text='Статистика', callback_data='statistics')],
    [InlineKeyboardButton(text='Вернуться', callback_data='main')]
])

statistics = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Неделя', callback_data='week'),
        InlineKeyboardButton(text='Месяц', callback_data='month'),
        InlineKeyboardButton(text='3 месяца', callback_data='three_months'),
    ],
    [
        InlineKeyboardButton(text='6 месяцев', callback_data='six_months'),
        InlineKeyboardButton(text='9 месяцев', callback_data='nine_monhts'),
        InlineKeyboardButton(text='Год', callback_data='year')
    ],
    [InlineKeyboardButton(text='Вернуться', callback_data='main')]
])
