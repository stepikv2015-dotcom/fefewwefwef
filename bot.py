import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения (хостинг) или используем напрямую
BOT_TOKEN = os.getenv('BOT_TOKEN', 'ВАШ_ТОКЕН_БОТА')

# Проверка токена
if BOT_TOKEN == 'ВАШ_ТОКЕН_БОТА':
    logger.warning("Используется тестовый токен! Замените на настоящий.")

# Ссылки на изображения (замените на свои)
WELCOME_IMAGE = os.getenv('WELCOME_IMAGE', 'https://i.postimg.cc/FKG5YJdP/izobrazenie-2025-12-07-221133329.png')
ABOUT_IMAGE = os.getenv('ABOUT_IMAGE', 'https://i.postimg.cc/qRbT5CpZ/izobrazenie-2025-12-07-221050897.png')
BUY_IMAGE = os.getenv('BUY_IMAGE', 'https://i.postimg.cc/xTb26Ch6/izobrazenie-2025-12-07-221107661.png')
PAYMENT_IMAGE = os.getenv('PAYMENT_IMAGE', 'https://i.postimg.cc/qRbT5CpZ/izobrazenie-2025-12-07-221050897.png')

# Реквизиты для оплаты (замените на свои)
PAYMENT_DETAILS = """
💳 <b>РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ:</b>

📱 <b>QIWI</b>: +7XXXXXXXXXX
💳 <b>СБП</b>: 2202XXXXXXXXXXXX
🪙 <b>USDT TRC-20</b>: TXXXXXXXXXXXXXXXXXXX

💰 <b>Сумма</b>: 499 рублей
👤 <b>Комментарий к платежу</b>: Укажите ваш ID: {user_id}
⚠️ <b>ВАЖНО</b>: Без комментария платеж не будет зачислен!
"""

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# ========== КЛАВИАТУРЫ ==========

def get_main_menu():
    """Главное меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="💰 Купить приват", callback_data="buy_private"))
    keyboard.add(InlineKeyboardButton(text="👤 Обо мне", callback_data="about"))
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_back_keyboard():
    """Кнопка Назад в главное меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    return keyboard.as_markup()

def get_buy_keyboard():
    """Клавиатура для раздела покупки"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🛒 Купить", callback_data="confirm_buy"))
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_payment_keyboard():
    """Клавиатура для оплаты"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid"))
    keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_buy"))
    keyboard.adjust(1)
    return keyboard.as_markup()

# ========== ОБРАБОТЧИКИ КОМАНД ==========

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработка команды /start"""
    welcome_text = "Привет дрочер"
    
    await message.answer_photo(
        photo=WELCOME_IMAGE,
        caption=welcome_text,
        reply_markup=get_main_menu()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработка команды /help"""
    help_text = (
        "🤖 <b>Команды бота:</b>\n\n"
        "/start - Запустить бота\n"
        "/help - Помощь\n\n"
        "💎 При возникновении проблем с оплатой - напишите @ваш_юзернейм"
    )
    await message.answer(help_text)

# ========== ОБРАБОТЧИКИ CALLBACK-ЗАПРОСОВ ==========

@dp.callback_query(lambda c: c.data == "about")
async def about_callback(callback: types.CallbackQuery):
    """Кнопка 'Обо мне'"""
    await callback.message.delete()
    
    await callback.message.answer_photo(
        photo=ABOUT_IMAGE,
        caption="Привет",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "buy_private")
async def buy_private_callback(callback: types.CallbackQuery):
    """Кнопка 'Купить приват'"""
    await callback.message.delete()
    
    await callback.message.answer_photo(
        photo=BUY_IMAGE,
        caption="🛒 <b>Покупка фотокарточек красивых девушек</b>\n\n"
                "💎 <b>В наборе:</b>\n"
                "• 50 эксклюзивных фото\n"
                "• 10 видео\n"
                "• Доступ навсегда\n\n"
                "💰 <b>Цена:</b> 499 руб.",
        reply_markup=get_buy_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "confirm_buy")
async def confirm_buy_callback(callback: types.CallbackQuery):
    """Кнопка 'Купить'"""
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
    """Кнопка 'Я оплатил'"""
    await callback.message.delete()
    
    confirmation_text = (
        "✅ <b>Спасибо за оплату!</b>\n\n"
        "⏳ <b>Ожидайте подтверждение оплаты в течение 10-15 минут.</b>\n"
        "Как только оплата будет подтверждена, вы получите доступ к материалам.\n\n"
        "📢 <b>После подтверждения оплаты:</b>\n"
        "1. Вам придет уведомление\n"
        "2. Доступ к приватному каналу будет открыт\n\n"
        "💬 По всем вопросам: @ваш_юзернейм"
    )
    
    await callback.message.answer(
        text=confirmation_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_callback(callback: types.CallbackQuery):
    """Кнопка 'Назад' в главное меню"""
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
    """Кнопка 'Назад' в раздел покупки"""
    await callback.message.delete()
    
    await callback.message.answer_photo(
        photo=BUY_IMAGE,
        caption="🛒 <b>Покупка фотокарточек красивых девушек</b>\n\n"
                "💎 <b>В наборе:</b>\n"
                "• 50 эксклюзивных фото\n"
                "• 10 видео\n"
                "• Доступ навсегда\n\n"
                "💰 <b>Цена:</b> 499 руб.",
        reply_markup=get_buy_keyboard()
    )
    await callback.answer()

# ========== ОБРАБОТКА ОШИБОК ==========

@dp.errors()
async def errors_handler(update, exception):
    """Обработка ошибок"""
    logger.error(f"Ошибка: {exception}", exc_info=True)
    return True

# ========== ЗАПУСК БОТА ==========

async def main():
    """Основная функция запуска бота"""
    logger.info("Бот запущен!")
    
    # Удаляем вебхук (если был)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем поллинг
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

