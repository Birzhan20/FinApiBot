import os
from dotenv import load_dotenv, find_dotenv

# Поиск и загрузка файла .env
env_file = find_dotenv()
if not env_file:
    exit("Файл .env не найден. Переменные окружения не загружены.")
else:
    load_dotenv(env_file)
    print(f"Файл .env найден и загружен: {env_file}")

# Получение значений переменных окружения
TELEGRAM_TOKEN = os.getenv("Bot_token")
GOOGLE_SHEET_ID = os.getenv("G_token")

# Проверка, что переменные окружения загружены
if not TELEGRAM_TOKEN or not GOOGLE_SHEET_ID:
    exit("Отсутствуют обязательные переменные окружения Bot_token или G_token.")

# Определение стандартных команд для бота
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
)
