import telebot
import gspread
import json
import pandas as pd
import re
from datetime import datetime, timedelta

bot = telebot.TeleBot('your_bot_token')


def convert_date(date: str = "01/01/00"):
    """ Конвертируем дату из строки в datetime """
    # PUT YOUR CODE HERE
    pass


def connect_table(message):
    """ Подключаемся к Google-таблице """
    url = message.text
    sheet_id =  # Нужно извлечь id страницы из ссылки на Google-таблицу
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open('tables.json', 'w') as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")


def access_current_sheet():
    """ Обращаемся к Google-таблице """
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    return worksheet, tables[max(tables)]["url"], df


def choose_action(message):
    """ Обрабатываем действия верхнего уровня """
    if message.text == "Подключить Google-таблицу":
        # PUT YOUR CODE HERE
        pass
    elif message.text == "Редактировать предметы":
        # PUT YOUR CODE HERE
        pass
    elif message.text == "Редактировать дедлайн":
        # PUT YOUR CODE HERE
        pass
    elif message.text == "Посмотреть дедлайны на этой неделе":
        # PUT YOUR CODE HERE
        pass


def choose_subject_action(message):
    """ Выбираем действие в разделе Редактировать предметы """
    # PUT YOUR CODE HERE
    pass


def choose_deadline_action(message):
    """ Выбираем действие в разделе Редактировать дедлайн """
    # PUT YOUR CODE HERE
    pass


def choose_removal_option(message):
    """ Уточняем, точно ли надо удалить все """
    # PUT YOUR CODE HERE
    pass


def choose_subject(message):
    """ Выбираем предмет, у которого надо отредактировать дедлайн """
    # PUT YOUR CODE HERE
    pass


def update_subject_deadline(message):
    """ Обновляем дедлайн """
    # PUT YOUR CODE HERE
    pass


def add_new_subject(message):
    """ Вносим новое название предмета в Google-таблицу """
    # PUT YOUR CODE HERE
    pass


def add_new_subject_url(message):
    """ Вносим новую ссылку на таблицу предмета в Google-таблицу """
    # PUT YOUR CODE HERE
    pass


def update_subject(message):
    """ Обновляем информацию о предмете в Google-таблице """
    # PUT YOUR CODE HERE
    pass


def delete_subject(message):
    """ Удаляем предмет в Google-таблице """
    # PUT YOUR CODE HERE
    pass


def clear_subject_list(message):
    """ Удаляем все из Google-таблицы """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=["start"])
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row("Подключить Google-таблицу")
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Внести новый дедлайн")
    start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


bot.infinity_polling()
