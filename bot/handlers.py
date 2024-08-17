from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from charts import create_chart, get_company_sheet_map

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем маппинг между компанией и именем листа
company_sheet_map = get_company_sheet_map()


async def handle_button_click(update: Update, context: CallbackContext):
    """
    Обрабатывает нажатие кнопок в сообщении Telegram, управляя выбором компании и типа отчета.

    В зависимости от нажатой кнопки, функция сохраняет выбранную компанию и предлагает пользователю выбрать
    тип отчета. После выбора типа отчета, функция создает и отправляет график с соответствующей информацией.

    Args:
        update (Update): Объект обновления от Telegram, содержащий информацию о нажатии кнопки.
        context (CallbackContext): Контекст обработки запроса, содержащий информацию о пользователе и данные.

    Проброс исключений и логирование ошибок происходят при возникновении исключений.
    """
    try:
        # Получаем объект запроса нажатия кнопки
        query = update.callback_query
        await query.answer()

        # Получаем идентификатор чата и данные нажатой кнопки
        chat_id = query.message.chat_id
        data = query.data

        if data.startswith('company_'):
            # Обработка выбора компании
            context.user_data['selected_company'] = company_sheet_map.get(data, "Unknown")

            # Обновляем сообщение с выбором типа отчета
            await query.edit_message_text(text=f"Вы выбрали {context.user_data['selected_company']}. Теперь выберите тип отчетности:")

            # Отправляем кнопки для выбора типа отчета
            keyboard = [
                [InlineKeyboardButton("Доход", callback_data='income')],
                [InlineKeyboardButton("Расход", callback_data='expense')],
                [InlineKeyboardButton("Прибыль", callback_data='profit')],
                [InlineKeyboardButton("КПН", callback_data='corporate income tax')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=chat_id, text="Выберите тип отчетности:", reply_markup=reply_markup)

        elif data in ['income', 'expense', 'profit', 'corporate income tax']:
            # Обработка выбора типа отчета
            column_map = {
                'income': 'Доход',
                'expense': 'Расход',
                'profit': 'Прибыль',
                'corporate income tax': 'КПН'
            }

            column = column_map.get(data)
            selected_company = context.user_data.get('selected_company')

            if column and selected_company:
                # Создаем график на основе выбранного отчета и компании
                buf = create_chart(column, selected_company)
                await context.bot.send_photo(chat_id=chat_id, photo=buf)
            else:
                # Отправляем сообщение об ошибке, если не удалось найти данные
                await context.bot.send_message(chat_id=chat_id, text="Неизвестный тип отчета или компания.")

    except Exception as e:
        # Логируем ошибку при возникновении исключения
        logger.error(f"Ошибка в handle_button_click: {e}")
