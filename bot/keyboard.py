from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import logging
from charts import get_company_sheet_map

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
    # Получение маппинга компаний и листов
    company_sheet_map = get_company_sheet_map()

    # Создание клавиатуры с кнопками для выбора компании
    keyboard = [
        [InlineKeyboardButton(company_name, callback_data=company_id)]
        for company_id, company_name in company_sheet_map.items()
    ]

    # Создание разметки для кнопок
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка сообщения с клавиатурой пользователю
    await update.message.reply_text('Выберите компанию:', reply_markup=reply_markup)

