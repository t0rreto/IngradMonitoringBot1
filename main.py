import telebot

from functions import *

bot_token = '6038540603:AAGOnN0O42xOZCLGs4VIr0DkAwwCUeKPIFM'

# Создаем объект бота
bot = telebot.TeleBot(bot_token)

BRAND_YK_ID = -558338915
BRAND_SOCIAL_ID = -697398941

INGRAD_YK_ID = -1001807530118
INGRAD_SOCIAL_ID = -1001696121895

BRAND_BOT_ID = 953170029

ADMIN_ID = 559828927


@bot.message_handler(func=lambda message: message.chat.id == BRAND_YK_ID)
def forward_yk(message):
    try:
        print_message(message)
        sender_id = message.from_user.id
        if sender_id == BRAND_BOT_ID or sender_id == ADMIN_ID:
            entities = message.entities
            slug = ""
            if entities:
                slug = entities[0].url.split("/")[-2]
            message = replyBotMessage(message.text, entities, slug)
            bot.send_message(INGRAD_YK_ID, message[0], entities=message[1])
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")


@bot.message_handler(func=lambda message: message.chat.id == BRAND_SOCIAL_ID)
def forward_social(message):
    try:
        print_message(message)
        sender_id = message.from_user.id
        if sender_id == BRAND_BOT_ID or sender_id == ADMIN_ID:
            entities = message.entities
            url = ""
            if entities:
                url = entities[0].url
            message = replyBotMessageKeyWordsByManyData(message.text, entities, url)
            bot.send_message(INGRAD_SOCIAL_ID, message[0], entities=message[1])
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")


print("Bot started")
# Запускаем бота
bot.polling()

