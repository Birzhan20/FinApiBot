from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    """
    Отправляет пользователю сообщение с кнопками для выбора компании.

    Использует `InlineKeyboardButton` для создания кнопок с данными callback,
    которые позволяют пользователю выбрать компанию.

    Args:
        update (Update): Объект обновления от Telegram.
        context (CallbackContext): Контекст обработки запроса.
    """
    # Создание клавиатуры с кнопками для выбора компании
    keyboard = [
        [InlineKeyboardButton("Onyx Corp.", callback_data='company_1')],
        [InlineKeyboardButton("Parlamentarioum LTD.", callback_data='company_2')],
        [InlineKeyboardButton("Michelangello LLP.", callback_data='company_3')],
        [InlineKeyboardButton("Almaty Cube LTD.", callback_data='company_4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка сообщения с клавиатурой пользователю
    await update.message.reply_text('Выберите компанию:', reply_markup=reply_markup)
