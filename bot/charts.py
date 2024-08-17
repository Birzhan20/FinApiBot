import gspread
import matplotlib.pyplot as plt
import io
from config import GOOGLE_SHEET_ID
from oauth2client.service_account import ServiceAccountCredentials

# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials/finbot-432715-697506698f0d.json",
    scope
)
client = gspread.authorize(creds)


def get_company_sheet_map():
    """
    Получает маппинг между идентификаторами компаний и названиями листов в Google Sheets.

    Returns:
        dict: Словарь с маппингом вида {'company_1': 'Sheet Name 1', ...}
    """
    # Открываем документ Google Sheets по ключу
    sheet = client.open_by_key(GOOGLE_SHEET_ID)

    # Получаем список всех листов
    worksheets = sheet.worksheets()

    # Создаем маппинг компании и названия листа
    company_sheet_map = {}
    for index, worksheet in enumerate(worksheets, start=1):
        sheet_name = worksheet.title
        company_sheet_map[f'company_{index}'] = sheet_name

    return company_sheet_map


def create_chart(column, sheet_name):
    """
    Создает график на основе данных из Google Sheets.

    Args:
        column (str): Название столбца для отображения на графике.
        sheet_name (str): Имя листа в Google Sheets.

    Returns:
        io.BytesIO: Объект BytesIO с сохраненным графиком в формате PNG.

    Raises:
        ValueError: Если указанный столбец не найден в данных Google Sheets.
    """
    # Получение нужного листа по имени
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)

    # Получение данных из Google Sheets
    data = sheet.get_all_records()

    # Очистка названий столбцов и удаление пробелов и символов после них
    columns = {col.split()[0]: col for col in data[0].keys()} if data else {}
    print("Доступные столбцы:", columns)

    # Очистка пробелов в названии столбца
    column = column.strip()

    # Проверка наличия столбца в данных
    if column not in columns:
        raise ValueError(f"Столбец '{column}' не найден в данных Google Sheets.")

    # Извлечение данных для графика
    months = [row['Месяц'] for row in data]
    values = [row[columns[column]] for row in data]

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(months, values, marker='o')
    plt.title(f'График по столбцу {column} ({sheet_name})')
    plt.xlabel('Месяц')
    plt.ylabel(column)
    plt.xticks(rotation=45)

    # Сохранение графика в объект BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf
