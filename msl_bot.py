import inspect
import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import sys

admin = 214304884
with open('../MSLB_tools/token.txt') as token_file:
    token = token_file.read().strip()
bot = telebot.TeleBot(token, parse_mode=None)


def db_request(request_body):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(request_body)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


# Сгенерировать случайное число от a до b включительно
def rand_gen(a, b):
    return int(random.random() * 10000) % (b - a + 1) + a


# Достать аргументы из команды
def extract_args(command):
    string = ''
    for word in command.split()[1:]:
        string += word + ' '
    return string.strip()


def user_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('/help'))
    return markup


def check_user(message):
    conn = sqlite3.connect('../MSLB_tools/db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f'select nickname from Players where player_id={message.from_user.id}')
    result = cursor.fetchall()
    conn.close()
    if not result:
        return False, message.from_user.username
    else:
        return True, result[0][0]


def add_user(user_id, nickname):
    conn = sqlite3.connect('../MSLB_tools/db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f'insert into Players values ({user_id}, "{nickname}")')
    conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
def command_start(message):
    exists, nickname = check_user(message)
    if exists:
        text = inspect.cleandoc(f"""
            Привет, {nickname}, я тебя помню.
            Давай продолжим!
        """) if message.from_user.language_code == 'ru' else inspect.cleandoc(f"""
            Hi, {nickname}, I remember you.
            Let's continue!
        """)
    else:
        nickname += f"#{rand_gen(1000, 9999)}"
        text = inspect.cleandoc(f"""
            Привет, {message.from_user.username}!
            Я надеюсь тебе нравятся RPG.
            Предлагаю ник {nickname}.
        """) if message.from_user.language_code == 'ru' else inspect.cleandoc(f"""
            Hi, {message.from_user.username}!
            I hope you like RPG.
            I suggest nick {nickname}.
        """)
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=user_buttons())


@bot.message_handler(commands=['id'])
def command_id(message):
    bot.send_message(message.chat.id, message.from_user.id)


@bot.message_handler(commands=['sql'])
def command_sql(message):
    if message.chat.id == admin:
        request = extract_args(message.text)
        result = db_request(request)
        bot.send_message(message.chat.id, str(result))
    else:
        bot.send_message(message.chat.id, 'Only for admin!')


bot.infinity_polling()
