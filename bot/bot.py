from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TELEGRAM_TOKEN
from keyboard import start
from handlers import handle_button_click


# Функция обработки нажатий кнопок
async def button(update: Update, context: CallbackContext):
    """
    Обрабатывает нажатия кнопок в чате и передает управление функции `handle_button_click`.
    """
    await handle_button_click(update, context)


def main():
    """
    Основная функция для запуска бота.
    Создает бота, добавляет обработчики команд и кнопок, и запускает его.
    """
    # Создание бота с токеном
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик нажатий на кнопки
    application.add_handler(CallbackQueryHandler(handle_button_click))

    # Запуск бота
    application.run_polling()


# Запуск основной функции при запуске скрипта
if __name__ == '__main__':
    main()
