import inspect
import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import sys

admin = 214304884
with open('../MSLB_tools/token.txt') as token_file:
    token = token_file.read().strip()
    print(token)
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
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f'select * from Players where player_id={message.from_user.id}')
    result = cursor.fetchall()
    if not result:
        cursor.execute(f'insert into Players values ({message.from_user.id}, "{message.from_user.username}")')
        conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
def command_start(message):
    check_user(message)
    text = inspect.cleandoc(f"""
        Привет, {message.from_user.username}!
        Я надеюсь тебе нравятся RPG
    """) if message.from_user.language_code == 'ru' else inspect.cleandoc(f"""
        Hi, {message.from_user.username}!
        I hope you like RPG
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
