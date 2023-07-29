import telebot

from functions import *

bot_token = '6038540603:AAGOnN0O42xOZCLGs4VIr0DkAwwCUeKPIFM'

# Создаем объект бота
bot = telebot.TeleBot(bot_token)

YK_BRAND_ID = -558338915
SOCIAL_BRAND_ID = -697398941

YK_INGRAD_ID = -1001807530118
SOCIAL_INGRAD_ID = -1001696121895

BRAND_BOT_ID = 953170029

# MY_ID = 559828927


@bot.message_handler()
def forward_message(message):
    try:
        sender_id = message.from_user.id
        if sender_id == BRAND_BOT_ID:
            entities = message.entities
            slug = ""
            if entities:
                slug = entities[0].url.split("/")[-2]
            message = replyBotMessage(message.text, entities, slug)
            bot.send_message(YK_INGRAD_ID, message[0], entities=message[1])
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")


@bot.message_handler(func=lambda message: message.chat.id == SOCIAL_BRAND_ID)
def forward_message(message):
    try:
        sender_id = message.from_user.id
        if sender_id == BRAND_BOT_ID:
            entities = message.entities
            url = ""
            if entities:
                url = entities[0].url
            message = replyBotMessageKeyWordsByManyData(message.text, entities, url)
            bot.send_message(SOCIAL_INGRAD_ID, message[0], entities=message[1])
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")

# Запускаем бота
bot.polling()
