import numpy as np
import requests
import telebot
from colorthief import ColorThief

import config
import functions
from parser import parser

bot = telebot.TeleBot(config.tg_token)
parser = parser()


@bot.message_handler(commands=['start', 'help'])
def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_random = telebot.types.KeyboardButton('Random aesthetic')
    button_create = telebot.types.KeyboardButton('Create my color aes')
    button_return = telebot.types.KeyboardButton('Return')
    markup.add(button_random, button_create, button_return)

    sms = bot.send_message(message.chat.id, "Choose:", reply_markup=markup)
    bot.register_next_step_handler(sms, process_select_step)


def process_select_step(r):
    try:
        if (r.text == 'Random aesthetic'):
            random_fun(r)
        elif (r.text == 'Create my color aes'):
            sms = bot.send_message(r.chat.id, 'Send me image of your color!')
            bot.register_next_step_handler(sms, create_fun)
        elif (r.text == 'Return'):
            markup = telebot.types.ReplyKeyboardRemove(selective=False)
            bot.send_message(r.chat.id, "See you later!)\n", reply_markup=markup)

        elif (r.text == "/start" or r.text == "/help"):
            bot.send_message(r.chat.id,
                             "Hello! I am your personal assistant I know how to make an aesthetic chart based on the most common color of the picture you send me!")
            menu(r)
        else:
            bot.send_message(r.chat.id, "Sorry, I dont understand\n")
            menu(r)
    except Exception as e:
        bot.reply_to(r, "Sorry, something went wrong...")


def create_fun(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    r = requests.get('https://xkcd.com/color/rgb/')
    table = functions.make_table(r)
    color_thief = ColorThief('image.jpg')
    most_common_col = color_thief.get_color(quality=1)
    functions.closest_color(most_common_col)
    col = table[table['rgb_code'] == functions.closest_color(most_common_col)].name.values
    res = col[0]
    col_url = f'https://www.pinterest.ru/search/pins/?rs=ac&len=2&q={res}%20aesthetic&eq={res}%20aes&etslf=4115&term_meta[]={res}%7Cautocomplete%7C0&term_meta[]=aesthetic%7Cautocomplete%7C0'
    functions.driver_fun(col_url)
    bot.send_message(message.chat.id, res)
    parser.run(bot, message)
    next_step_msg = bot.send_message(message.chat.id, "What's next?")
    bot.register_next_step_handler(next_step_msg, process_select_step)


def random_fun(message):
    r = requests.get('https://xkcd.com/color/rgb/')
    table = functions.make_table(r)
    res = np.random.choice(table.name)
    col_url = f'https://www.pinterest.ru/search/pins/?rs=ac&len=2&q={res}%20aesthetic&eq={res}%20aes&etslf=4115&term_meta[]={res}%7Cautocomplete%7C0&term_meta[]=aesthetic%7Cautocomplete%7C0'
    functions.driver_fun(col_url)
    bot.send_message(message.chat.id, res)
    parser.run(bot, message)
    next_step_msg = bot.send_message(message.chat.id, "What's next?")
    bot.register_next_step_handler(next_step_msg, process_select_step)


if __name__ == '__main__':
    bot.polling(none_stop=True)
