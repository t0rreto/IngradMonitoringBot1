import telebot

from functions import *

bot_token = '6038540603:AAGOnN0O42xOZCLGs4VIr0DkAwwCUeKPIFM'

# Создаем объект бота
bot = telebot.TeleBot(bot_token)

BRAND_YK_ID = -1001832139525
BRAND_SOCIAL_ID = -1001972022129

INGRAD_YK_ID = -1001807530118
INGRAD_SOCIAL_ID = -1001696121895


BRAND_BOT_ID = 953170029
ADMIN_ID = 559828927


@bot.message_handler(func=lambda message: True)
def handler_message(message):
    try:
        print_message(message)
        if message.chat.id == BRAND_YK_ID:
            forward_yk(message)
        if message.chat.id == BRAND_SOCIAL_ID:
            forward_social(message)
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")


def forward_yk(message):
    sender_id = message.from_user.id
    entities = message.entities
    slug = ""
    if entities:
        slug = entities[0].url.split("/")[-2]
    message = replyBotMessage(message.text, entities, slug)
    bot.send_message(INGRAD_YK_ID, message[0], entities=message[1])


def forward_social(message):
    sender_id = message.from_user.id
    entities = message.entities
    url = ""
    if entities:
        url = entities[0].url
    message = replyBotMessageKeyWordsByManyData(message.text, entities, url)
    bot.send_message(INGRAD_SOCIAL_ID, message[0], entities=message[1])


print("Bot started")
bot.polling()
