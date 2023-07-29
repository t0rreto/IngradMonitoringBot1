import re

import requests

tagAssociation = [
    {'slug': "flinitiative", 'name': 'ФилатовЛуг'},
    {'slug': "Kytyzovgrad2chat", 'name': 'КутузовГрад2'},
    {'slug': "kutuzovgrad", 'name': 'КутузовГрад'},
    {'slug': "novoe_medvedkovo", 'name': 'НовоеМедведково'},
    {'slug': "preobrajenie", 'name': 'Преображение'},
    {'slug': "preobrazhenie", 'name': 'Преображение'},
    {'slug': "LSP_Talks", 'name': 'Лесопарковый'},
    {'slug': "mikhaylova31", 'name': 'Михайлова31'},
    {'slug': "silverpark_dmz", 'name': 'СеребряныйПарк'},
    {'slug': "LSP_3K", 'name': 'Лесопарковый'},
    {'slug': "LSP_Auto", 'name': 'Лесопарковый'},
    {'slug': "JKLesoparkoviy", 'name': 'Лесопарковый'},
    {'slug': "odingrad", 'name': 'Одинград'},
    {'slug': "odingrad_lesnoy", 'name': 'Одинград'},
    {'slug': "odingrad_semeyniy", 'name': 'Одинград'},
    {'slug': "vesna_aprelevka", 'name': 'Vesna'},
    {'slug': "parking_fl", 'name': 'ФилатовЛуг'},
    {'slug': "flinitiative", 'name': 'ФилатовЛуг'},
    {'slug': "semeini1korpus", 'name': 'Одинград'},
    {'slug': "odingrad_boltalka", 'name': 'Одинград'},
    {'slug': "preobrazhenie_talks", 'name': 'Преображение'},
    {'slug': "preo_oss", 'name': 'Преображение'},
    {'slug': "odingrad_centr", 'name': 'Одинград'},
    {'slug': "novoe_medvedkovo", 'name': 'НовоеМедведково'},
    {'slug': "top_hills", 'name': "ЖК_TOPHILLS"}]


tagWithKeyWordsAssociation = []

def tagingChat(slug, chatTitle):
    name = ""
    for tag in tagAssociation:
        if slug == tag['slug'] or slug == tag['slug']:
            name = tag['name']
    if name == "":
        name = chatTitle
    return name


def taggingManyData(text, chatTitle):
    findedTags = []
    for tag in tagWithKeyWordsAssociation:
        try:
            (minStrI, maxStrI, resEnd) = getClosestString(text.lower(), tag['keywords'])
        except Exception:
            continue
        if len(resEnd) > 0:
            findedTags.append(tag['name'])
    if len(findedTags) == 0:
        findedTags.append(chatTitle)
    return findedTags


def replyBotMessage(message, entities, slug_from_url):
    len1 = len(message)
    tag: str = tagingChat(slug_from_url, message.split("\n")[0].replace(" ", "_"))
    message = f"#{tag}\n" + "\n".join(message.split("\n")[1:])
    len2 = len(message)
    minus = 0
    if len1 > len2:
        minus -= (len1 - len2)
    elif len2 > len1:
        minus = len2 - len1
    if entities:
        for ent in entities:
            ent.offset += minus

    return message, entities


def replyBotMessageKeyWordsByManyData(message, entities, url):
    mergeText = message
    if url:
        urlText = requests.get(url).text
        mergeText += " " + urlText

    generalTag: str = re.sub("[\W]", "_", message.split("\n")[0])
    tags = taggingManyData(mergeText, generalTag)
    tagsStr = ""
    for tag in tags:
        tagsStr = tagsStr + f"#{tag} "
    tagsStr = tagsStr + "\n"
    len1 = len(message)
    message = tagsStr + "\n".join(message.split("\n")[1:])
    len2 = len(message)
    minus = 0
    if len1 > len2:
        minus -= (len1 - len2)
    elif len2 > len1:
        minus = len2 - len1
    if entities:
        for ent in entities:
            ent.offset += minus
    return message, entities


def getClosestString(str1, substr):
    res = []
    for sub in substr:
        pattern = "([\W]?[\W])" + sub + "[\s\w]{0,2}([\W\s]|$){1,1}"
        result = [(_.start(), _.end()) for _ in
                  re.finditer(pattern, str1, re.RegexFlag.IGNORECASE | re.RegexFlag.UNICODE |
                              re.RegexFlag.MULTILINE)]
        for _ in result:
            res.append(_)

    n = 80
    chunks = [(i, i + n if i + n < len(str1) else len(str1)) for i in range(0, len(str1), n)]
    res2 = []
    for start, end in chunks:
        for wS, wE in res:
            if wS in range(start, end) or wE in range(start, end):
                res2.append((start, end, wS, wE))

    class CountMax:
        def __init__(self, start, end, count):
            self.start = start
            self.end = end
            self.count = count

    count: list[CountMax] = []
    for s1, e1, s2, e2 in res2:
        finded = False
        for maxy in count:
            if s1 == maxy.start and e1 == maxy.end:
                maxy.count += 1
                finded = True
        if not finded:
            count.append(CountMax(s1, e1, 1))
    maxy: CountMax = count[0]
    for c in count:
        if maxy.count < c.count:
            maxy = c

    minStrI = maxy.start
    maxStrI = maxy.end
    resEnd = []
    for (start, end, ss, se) in res2:
        if maxy.start == start:
            resEnd.append((ss, se))

    for (ss, se) in resEnd:
        if minStrI > ss:
            minStrI = ss
        if maxStrI < se:
            maxStrI = se

    return minStrI, maxStrI, resEnd


def print_message(message):
    chat_id = message.chat.id
    chat_name = message.chat.title
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name
    text = message.text.replace('\n', ' ')
    print(f"Chat - {chat_name}, chat id: {chat_id}, sender: {sender_name}, sender_id: {sender_id}, text: {text}")