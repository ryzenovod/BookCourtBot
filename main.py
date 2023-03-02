"""
import telebot
bot = telebot.TeleBot('6013625056:AAEliH3fEFwOiVxlJjdy5DaSm9NSGao43g4')
@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler()
def get_user_message(message):
    if message.text == "привет":
        bot.send_message(message.chat.id, "салам")
bot.polling(none_stop=True)
"""

import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import sys
import pathlib
from pathlib import Path

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'C:\\Users\\ryzenovod\\pythonProject\\mydatabase'

# connect to the database
conn = sqlite3.connect('C:\\Users\\ryzenovod\\pythonProject\\mydatabase', check_same_thread=False)

cursor = conn.cursor()


# define the search function
def search(update, context):
    query = update.message.text
    sql = "SELECT * FROM books WHERE title LIKE '%{}%' OR author LIKE '%{}%'".format(query, query)
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        message = "Sorry, I couldn't find any books matching your search query."
    else:
        message = "Here are the books I found:\n\n"
        for result in results:
            message += "* {} by {}\n".format(result[1], result[2])
            message += "Link: {}\n\n".format(result[3])
    update.message.reply_text(message, parse_mode='Markdown')


# set up the Telegram bot
updater = Updater('6013625056:AAFx2QgneeRDR5XlfBo-2uR7n0xl04QzdP0', use_context=True)
dispatcher = updater.dispatcher

# add the message handler
dispatcher.add_handler(MessageHandler(Filters.text, search))

# start the bot
updater.start_polling()
