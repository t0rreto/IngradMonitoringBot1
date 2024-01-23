import telebot
from config import *
from functions import *
from entities import *


# Создаем объект бота
bot = telebot.TeleBot(bot_token)
table_connector = TableConnector()


@bot.message_handler(func=lambda message: True)
def handler_message(message):
    try:
        if message.chat.id == BRAND_YK_ID:
            sent_message = forward_yk(message)
            save_to_table_brand(sent_message, table_connector)
        if message.chat.id == BRAND_SOCIAL_ID:
            forward_social(message)
        if message.chat.id == CLOSED_CHATS_ID:
            closed_chats_group_handler(message)

    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")


def closed_chats_group_handler(message):
    tag_association = {
        "РС": "RiverSky",
        "ФР": "Foriver",
        "ТХ": "TopHILLS",
        "КГ1": "КутузовGRADI",
        "КГ2": "КутузовGRADII",
        "СП": "СеребряныйПарк",
        "НМ": "НовоеМедведково",
        "ОС": "ОдинградСемейный",
        "ОЛ": "ОдинградЛесной",
        "ОЦ": "ОдинградЦентральный",
        "ЛП": "Лесопарковый",
        "НП": "НовоеПушкино",
        "ПР": "Преображение",
        "МХ31": "Михайлова31",
        "НЧ17": "Новочеремушкниская17",
        "ФЛ": "ФилатовЛуг"
    }
    if message.text in tag_association.keys():
        table_connector.current_source = tag_association[message.text]
        print(f"Текущий чат пересылки: {table_connector.current_source}")
        return

    save_to_table_closed(message, table_connector)


def forward_yk(message):
    entities = message.entities
    slug = ""
    if entities:
        slug = entities[0].url.split("/")[-2]
        if slug == 'vk.com':
            slug = entities[2].url.split("/")[-1]
    message = replyBotMessage(message.text, entities, slug)
    sent_message = bot.send_message(chat_id=INGRAD_YK_ID, text=message[0], entities=message[1])
    bot.send_message(chat_id=INGRAD_YK_2_ID, text=message[0], entities=message[1], reply_to_message_id=message[2])
    return sent_message


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
