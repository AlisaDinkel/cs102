import json
import re
from datetime import datetime, timedelta

import gspread  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
import telebot  # type: ignore

bot = telebot.TeleBot("6005297572:AAE8T_01diWdDd0TlWHfCsVUHZ3ye_JgbaA")


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    if divider != date[2]:
        return False
    new_date = "/".join(date.split(divider))
    try:
        converted_date = convert_date(new_date)
    except ValueError:
        return False
    if -1 <= (converted_date - datetime.today()).days < 365 and converted_date.date() >= datetime.today().date():
        return True
    return False


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    return datetime.strptime(date, "%d/%m/%y")


def connect_table(message):
    """Подключаемся к Google-таблице"""
    if message.text == "Меню":
        start(message)
    url = message.text
    if not is_valid_url(url):
        bot.send_message(message.chat.id, "Ссылка некорректна, попробуйте еще раз")
        start(message)
    sheet_id = url.split("/")[url.split("/").index("d") + 1]
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")
    start(message)


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    df = pd.DataFrame(worksheet.get_all_records())
    return worksheet, tables[max(tables)]["url"], df


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        table_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        table_markup.row("Меню")
        info = bot.send_message(message.chat.id, "Пришлите ссылку на таблицу", reply_markup=table_markup)
        bot.register_next_step_handler(info, connect_table)
    elif message.text == "Редактировать предметы":
        subject_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        subject_markup.row("Добавить новый предмет")
        subject_markup.row("Редактировать информацию о предмете")
        subject_markup.row("Удалить предмет")
        subject_markup.row("Удалить все предметы")
        subject_markup.row("Меню")
        info = bot.send_message(message.chat.id, "Выберите действие", reply_markup=subject_markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Редактировать дедлайн":
        deadline_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        deadline_markup.row("Добавить дедлайн")
        deadline_markup.row("Изменить дедлайн")
        deadline_markup.row("Удалить дедлайн")
        deadline_markup.row("Меню")
        info = bot.send_message(message.chat.id, "Выберите действие", reply_markup=deadline_markup)
        bot.register_next_step_handler(info, choose_deadline_action)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        today = datetime.today()
        week = today + timedelta(days=7)
        worksheet = access_current_sheet()[0]
        mes = f""
        for i in range(2, len(worksheet.col_values(1)) + 1):
            for ind, data in enumerate(worksheet.row_values(i)[2:], 3):
                if is_valid_date(data):
                    if today <= convert_date(data) <= week:
                        mes += f"Предмет: {worksheet.cell(i, 1).value}    дедлайн №{worksheet.cell(1, ind).value}: {data}\n"
        if mes == "":
            mes += "На этой неделе дедлайнов нет!"
        bot.send_message(message.chat.id, mes)
        menu(message)

    else:
        bot.send_message(message.chat.id, "Попробуйте еще раз")
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Добавить новый предмет":
        info = bot.send_message(message.chat.id, "Введите название предмета")
        bot.register_next_step_handler(info, add_new_subject)

    elif message.text == "Редактировать информацию о предмете":
        subject_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        worksheet = access_current_sheet()[0]
        subject = len(worksheet.col_values(1)) + 1
        for i in range(2, subject):
            subject_markup.row(worksheet.cell(i, 1).value)
        subject_markup.row("Меню")
        info = bot.send_message(
            message.chat.id, "Нажмите на название предмета, который хотите изменить.", reply_markup=subject_markup
        )
        bot.register_next_step_handler(info, update_subject)

    elif message.text == "Удалить предмет":
        df = access_current_sheet()[2]
        if len(df) == 0:
            bot.send_message(message.chat.id, "Список предметов пуст")
            menu(message)
        else:
            subject_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            worksheet = access_current_sheet()[0]
            subject = len(worksheet.col_values(1)) + 1
            for i in range(2, subject):
                subject_markup.row(worksheet.cell(i, 1).value)
            subject_markup.row("Меню")
            info = bot.send_message(message.chat.id, "Выберите название предмета", reply_markup=subject_markup)
            bot.register_next_step_handler(info, delete_subject)

    elif message.text == "Удалить все предметы":
        subject_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        subject_markup.row("Да")
        subject_markup.row("Нет")
        subject_markup.row("Меню")
        info = bot.send_message(
            message.chat.id, "Вы уверены, что хотите удалить все предметы?", reply_markup=subject_markup
        )
        bot.register_next_step_handler(info, choose_removal_option)

    elif message.text == "Меню":
        menu(message)

    else:
        bot.send_message(message.chat.id, "Попробуйте еще раз")
        menu(message)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    if message.text == "Добавить дедлайн" or message.text == "Изменить дедлайн":
        deadline_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        worksheet = access_current_sheet()[0]
        deadlines = len(worksheet.col_values(1)) + 1
        for i in range(2, deadlines):
            deadline_markup.row(worksheet.cell(i, 1).value)
        deadline_markup.row("Меню")
        info = bot.send_message(
            message.chat.id,
            "Выберите предмет",
            reply_markup=deadline_markup,
        )
        bot.register_next_step_handler(info, choose_subject)

    elif message.text == "Удалить дедлайн":
        info = bot.send_message(message.chat.id, "Введите через запятую название предмета и номер работы (от 1 до 5)")
        bot.register_next_step_handler(info, delete_deadline, message.text)

    elif message.text == "Меню":
        menu(message)

    else:
        bot.send_message(message.chat.id, "Попробуйте еще раз")
        menu(message)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да":
        clear_subject_list(message)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Удаление отменено")
        menu(message)
    elif message.text == "Меню":
        menu(message)
    else:
        bot.send_message(message.chat.id, "Попробуйте еще раз")
        menu(message)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    worksheet, _, df = access_current_sheet()
    prev_sub = message.text
    if worksheet.find(prev_sub) is None:
        bot.send_message(message.chat.id, "Предмет не найден")
        menu(message)
    elif prev_sub == "Меню":
        menu(message)
    info = bot.send_message(
        message.chat.id, "Введите через запятую номер работы (от 1 до 5) и новый дедлайн (dd/mm/yy)"
    )
    bot.register_next_step_handler(info, update_subject_deadline, prev_sub)


def update_subject_deadline(message, prev_sub):
    """Обновляем дедлайн"""
    worksheet, _, df = access_current_sheet()
    try:
        n, date = [el.strip() for el in message.text.split(",")]
        if not 1 <= int(n) <= 5:
            bot.send_message(message.chat.id, "Номер работы должен быть от 1 до 5")
            menu(message)
        if is_valid_date(date, date[2]):
            updated_subject_row = worksheet.find(prev_sub).row
            date = convert_date("/".join(date.split(date[2])))
            worksheet.update_cell(updated_subject_row, int(n) + 2, date.strftime("%d/%m/%y"))
            bot.send_message(message.chat.id, "Обновление прошло успешно")
            menu(message)
        else:
            bot.send_message(
                message.chat.id,
                "Некорректная дата, попробуйте еще раз",
            )
            bot.register_next_step_handler(prev_sub, choose_subject)
    except ValueError:
        bot.send_message(message.chat.id, "Вводите данные через запятую")
        menu(message)


def delete_deadline(message, return_msg):
    worksheet, _, df = access_current_sheet()
    try:
        sub, n = [el.strip() for el in message.text.split(",")]
        if worksheet.find(sub) is None:
            bot.send_message(message.chat.id, "Предмет не найден, попробуйте еще раз")
            menu(message)
        if not 1 <= int(n) <= 5:
            bot.send_message(message.chat.id, "Номер работы должен быть от 1 до 5")
            menu(message)
        worksheet.update_cell(worksheet.find(sub).row, int(n) + 2, "")
        bot.send_message(message.chat.id, "Дедлайн удален")
        menu(message)
    except ValueError:
        bot.send_message(message.chat.id, "Вводите данные через запятую")
        bot.register_next_step_handler(return_msg, choose_deadline_action)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    worksheet, _, df = access_current_sheet()
    if worksheet.find(message.text) is not None:
        bot.send_message(message.chat.id, f"Предмет {message.text} уже существует")
        menu(message)
    else:
        worksheet.append_row([message.text])
        info = bot.send_message(message.chat.id, "Введите URL предмета")
        bot.register_next_step_handler(info, add_new_subject_url, message.text)


def add_new_subject_url(message, subject):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    if is_valid_url(message.text):
        worksheet, _, df = access_current_sheet()
        index_row = df.shape[0] + 1
        worksheet.update_cell(index_row, 2, message.text)

        bot.send_message(message.chat.id, "Предмет добавлен")
        menu(message)

    else:
        bot.send_message(message.chat.id, "Ссылка некорректна, попробуйте еще раз")
        bot.register_next_step_handler(subject, add_new_subject)


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    worksheet, _, df = access_current_sheet()
    prev_sub = message.text
    cell = worksheet.find(prev_sub)
    if prev_sub == "Меню":
        menu(message)
    if worksheet.find(prev_sub) is None:
        info = bot.send_message(message.chat.id, "Такого предмета не существует. Повторите попытку")
        bot.register_next_step_handler(info, update_subject)
    info = bot.send_message(message.chat.id, "Введите новое название предмета и url через запятую")
    bot.register_next_step_handler(info, update_subject_url, cell.row, prev_sub)


def update_subject_url(message, new_row, old_sub):
    worksheet, _, df = access_current_sheet()
    try:
        new_sub, new_url = [el.strip() for el in message.text.split(",")]
        if is_valid_url(new_url):
            worksheet.update_cell(new_row, 1, new_sub)
            worksheet.update_cell(new_row, 2, new_url)
            bot.send_message(message.chat.id, "Обновление прошло успешно")
            menu(message)
        else:
            bot.send_message(message.chat.id, "Ссылка некорректна")
            bot.register_next_step_handler(old_sub, update_subject)
    except ValueError:
        bot.send_message(message.chat.id, "Вводите новые данные через пробел")
        bot.register_next_step_handler(old_sub, update_subject)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    worksheet, url, df = access_current_sheet()
    del_cell = worksheet.find(message.text)
    if del_cell:
        worksheet.delete_rows(del_cell.row)
        bot.send_message(message.chat.id, "Предмет удален из таблицы")
        menu(message)
    elif message.text == "Меню":
        menu(message)
    else:
        info = bot.send_message(message.chat.id, "Такого предмета не существует. Повторите попытку")
        bot.register_next_step_handler(info, delete_subject)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    worksheet = access_current_sheet()[0]
    worksheet.delete_rows(2, 30)
    bot.send_message(message.chat.id, "Все предметы удалены")
    menu(message)


def is_table_connected():
    """Проверяет, подключена ли таблица"""
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        return bool(tables)  # Возвращаем True, если таблица подключена, иначе False
    except FileNotFoundError:
        return False  # Если файл tables.json не найден, считаем, что таблица не подключена


@bot.message_handler(commands=["menu"])
def menu(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Редактировать дедлайн")
    start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


@bot.message_handler(commands=["start"])
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if is_table_connected():
        bot.send_message(message.chat.id, "Таблица подключена!")
        start_markup.row("Посмотреть дедлайны на этой неделе")
        start_markup.row("Редактировать дедлайн")
        start_markup.row("Редактировать предметы")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_action)
    else:
        start_markup.row("Подключить Google-таблицу")
        info = bot.send_message(
            message.chat.id, "Чтобы начать нажмите 'Подключить Google-таблицу'", reply_markup=start_markup
        )
        bot.register_next_step_handler(info, choose_action)


bot.infinity_polling()
