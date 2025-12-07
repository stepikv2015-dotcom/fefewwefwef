import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен вашего бота
BOT_TOKEN = "8111120762:AAHJfiSl1h16nbBvxf4hiaLlyR4HUgHChIk"

# Ссылки на изображения (замените на свои с Imgur или другого хостинга)
WELCOME_IMAGE = "https://i.postimg.cc/s25xqmLK/izobrazenie-2025-12-07-220905491.png"
ABOUT_IMAGE = "https://i.postimg.cc/qRbT5CpZ/izobrazenie-2025-12-07-221050897.png"
BUY_IMAGE = "https://i.postimg.cc/FKG5YJdP/izobrazenie-2025-12-07-221133329.png"
PAYMENT_IMAGE = "https://i.postimg.cc/FKG5YJdP/izobrazenie-2025-12-07-221133329.png"

# Реквизиты для оплаты (замените на свои)
PAYMENT_DETAILS = """
💳 Реквизиты для оплаты:

📱 **QIWI**: +7XXXXXXXXXX
💳 **СБП**: 2202XXXXXXXXXXXX
🪙 **USDT TRC-20**: TXXXXXXXXXXXXXXXXXXX

💰 **Сумма**: 499 рублей
📝 **Комментарий к платежу**: Укажите ваш ID: {user_id}
"""

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== КЛАВИАТУРЫ ==========

# Главное меню
def get_main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="💰 Купить приват", callback_data="buy_private"))
    keyboard.add(InlineKeyboardButton(text="👤 Обо мне", callback_data="about"))
    keyboard.adjust(1)
    return keyboard.as_markup()

# Клавиатура "Назад" (возврат в главное меню)
def get_back_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    return keyboard.as_markup()

# Клавиатура для раздела покупки
def get_buy_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🛒 Купить", callback_data="confirm_buy"))
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    keyboard.adjust(1)
    return keyboard.as_markup()

# Клавиатура для оплаты
def get_payment_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid"))
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_buy"))
    keyboard.adjust(1)
    return keyboard.as_markup()

# ========== ОБРАБОТЧИКИ КОМАНД ==========

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = "Привет дрочер"

    await message.answer_photo(
        photo=WELCOME_IMAGE,
        caption=welcome_text,
        reply_markup=get_main_menu()
    )

# ========== ОБРАБОТЧИКИ CALLBACK-ЗАПРОСОВ ==========

@dp.callback_query(lambda c: c.data == "about")
async def about_callback(callback: types.CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo=ABOUT_IMAGE,
        caption="Привет",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "buy_private")
async def buy_private_callback(callback: types.CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo=BUY_IMAGE,
        caption="Покупка фотокарточек красивых девушек",
        reply_markup=get_buy_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "confirm_buy")
async def confirm_buy_callback(callback: types.CallbackQuery):
    await callback.message.delete()

    payment_text = PAYMENT_DETAILS.format(user_id=callback.from_user.id)

    await callback.message.answer_photo(
        photo=PAYMENT_IMAGE,
        caption=payment_text,
        reply_markup=get_payment_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "paid")
async def paid_callback(callback: types.CallbackQuery):
    await callback.message.delete()

    await callback.message.answer(
        text="✅ Спасибо за оплату!\n\n"
             "⏳ Ожидайте подтверждение оплаты в течение 10-15 минут.\n"
             "Как только оплата будет подтверждена, вы получите доступ к материалам.",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_callback(callback: types.CallbackQuery):
    await callback.message.delete()

    welcome_text = "Привет дрочер"
    await callback.message.answer_photo(
        photo=WELCOME_IMAGE,
        caption=welcome_text,
        reply_markup=get_main_menu()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_buy")
async def back_to_buy_callback(callback: types.CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo=BUY_IMAGE,
        caption="Покупка фотокарточек красивых девушек",
        reply_markup=get_buy_keyboard()
    )
    await callback.answer()

# ========== ЗАПУСК БОТА ==========

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
