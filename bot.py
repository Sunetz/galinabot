import config
import os
from random import choice
from time import sleep
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits
import telebot
from telebot import types
from selenium import webdriver
from imageai.Detection import ObjectDetection
import password

chromedriver_path = os.path.join("c:/", "Users", "ilyas", "Desktop", "web-projects", "utilities", "chromedriver.exe")

bot = telebot.TeleBot(config.TOKEN)

option = webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)

@bot.message_handler(commands=['start']) #add buttoms
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Подорваться на поиски', callback_data='to find')
    item2 = types.InlineKeyboardButton('Поговорить', callback_data='to talk')
    item3 = types.InlineKeyboardButton('Угадать', callback_data='to guess')
    item4 = types.InlineKeyboardButton('Нашаманить пароль', callback_data='password')
    markup.add(item, item2, item3, item4)

    bot.send_message(message.chat.id, 'Ну, допустим, здрасте!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'to find':
            msg = bot.send_message(call.message.chat.id, 'Ну, спроси, поищем')
            bot.register_next_step_handler(msg, search)

        elif call.data == 'to talk':
            sti = open('sticker.webp', 'rb')
            bot.send_sticker(call.message.chat.id, sti)
            bot.send_message(call.message.chat.id, 'Ага, щазз')
        elif call.data == 'to guess':
            bot.send_message(call.message.chat.id, 'Валяй, загадывай')
            prediction = ImageClassification()
        elif call.data == 'password':
            how_many_chars = bot.send_message(call.message.chat.id, 'Сколько букав?')
            bot.register_next_step_handler(how_many_chars, new_password)


def new_password(message):
    n = int(message.text)
    chars = ascii_letters + digits
    word = ''.join(choice(chars) for _ in range(n))
    bot.send_message(message.chat.id, 'Держи, я стралась: ' + word)


def search(message):
    bot.send_message(message.chat.id, "Зииин, есть у нас такое?")
    image_href = 'https://yandex.ru/images/search?text=' + message.text
    driver.get(image_href)
    sleep(1)
    images = driver.find_elements_by_class_name("serp-item__link")

    for i in range(len(images)):
        bot.send_message(message.chat.id, images[i].get_attribute('href'))
        if i == 2:
            break


bot.polling()