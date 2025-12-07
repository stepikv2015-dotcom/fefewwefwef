import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения (обязательно на хостинге)
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден в переменных окружения!")
    exit("Ошибка: Установите переменную окружения BOT_TOKEN")

# Ссылки на изображения (замените на свои через переменные окружения или здесь)
WELCOME_IMAGE = os.getenv('WELCOME_IMAGE', 'https://i.imgur.com/ваше_изображение.jpg')
ABOUT_IMAGE = os.getenv('ABOUT_IMAGE', 'https://i.imgur.com/ваше_изображение2.jpg')
BUY_IMAGE = os.getenv('BUY_IMAGE', 'https://i.imgur.com/ваше_изображение3.jpg')
PAYMENT_IMAGE = os.getenv('PAYMENT_IMAGE', 'https://i.imgur.com/ваше_изображение4.jpg')

# Реквизиты для оплаты (настройте через переменные окружения или здесь)
PAYMENT_DETAILS = """
💳 <b>РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ:</b>

📱 <b>QIWI</b>: {qiwi_number}
💳 <b>СБП</b>: {sbp_number}
🪙 <b>USDT TRC-20</b>: {usdt_address}

💰 <b>Сумма</b>: {amount} рублей
👤 <b>Комментарий к платежу</b>: Укажите ваш ID: {user_id}
⚠️ <b>ВАЖНО</b>: Без комментария платеж не будет зачислен!
"""

# Получаем реквизиты из переменных окружения
QIWI_NUMBER = os.getenv('QIWI_NUMBER', '+7XXXXXXXXXX')
SBP_NUMBER = os.getenv('SBP_NUMBER', '2202XXXXXXXXXXXX')
USDT_ADDRESS = os.getenv('USDT_ADDRESS', 'TXXXXXXXXXXXXXXXXXXX')
PAYMENT_AMOUNT = os.getenv('PAYMENT_AMOUNT', '499')

# Инициализация бота с правильными настройками
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
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
        "💎 При возникновении проблем с оплатой - напишите в поддержку"
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
                f"💰 <b>Цена:</b> {PAYMENT_AMOUNT} руб.",
        reply_markup=get_buy_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "confirm_buy")
async def confirm_buy_callback(callback: types.CallbackQuery):
    """Кнопка 'Купить'"""
    await callback.message.delete()
    
    payment_text = PAYMENT_DETAILS.format(
        qiwi_number=QIWI_NUMBER,
        sbp_number=SBP_NUMBER,
        usdt_address=USDT_ADDRESS,
        amount=PAYMENT_AMOUNT,
        user_id=callback.from_user.id
    )
    
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
        "💬 <b>По всем вопросам:</b> Свяжитесь с поддержкой"
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
                f"💰 <b>Цена:</b> {PAYMENT_AMOUNT} руб.",
        reply_markup=get_buy_keyboard()
    )
    await callback.answer()

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
