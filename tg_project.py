# Бот рассылает какое-то сообщение, пользователям из двух групп. 
# Бот управляется из админки. 
# Пользователь, когда первый раз пишет боту - должен пройти регистрацию. Он введет свою группу и имя. 
# Администратор, пишет сообщение "Отпрвить группе А: Текст" - Текст доходит до всех пользователей группы А

import telebot
import json
from modules.news import NewsProcessor
from modules.course import CourseProcessor
from modules.weather import WeaherProcessor
from modules.wiki import WikiProcessor

with open("tgtoken.txt", "r", encoding="UTF-8") as f:
    token = f.read()  
    
try:
    # ----- Считать данные из json файла
    with open("users.json", "r", encoding="UTF-8") as json_file:
        users = json.load(json_file)
except:
    with open("users.json", "w", encoding="UTF-8"):
        users = []
        

# ----- Сохранить данные в json файл
def save():
    with open("users.json", "w", encoding="UTF-8") as json_file:
        json.dump(users, json_file)


try:
    # ----- Считать данные из json файла
    with open("admin_id.txt", "r", encoding="UTF-8") as f:
        admin_id = int(f.read())
except:
    with open("admin_id.txt", "w", encoding="UTF-8"):
        admin_id = 0
        

bot = telebot.TeleBot(token)

# пользователи хранятся в списке со словарями. 
"""users = [
    {
        name: "Иван"
        user_id: 1234,
        group: "A"
    },
    {
        name: "Катя",
        user_id: 5123,
        group: "B",
    },
    ...
]
"""


# функция, проверяющая есть ли в списке пользователей пользователь с заданным user_id
def check_user_id(user_id):  
    # если нашли пользователя - вернуть True.  Иначе - False
    for user in users:
        if user["user_id"] == user_id:
            return True
    
    return False


# 1 Регистрация в боте. 
@bot.message_handler(commands=["start"])
def start(message):
    if check_user_id(message.chat.id):
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы.')
    else: # пользователя с этим id нет в списке
        bot.send_message(message.chat.id, 'Я на связи. Давайте зарегистрируемся. Введите своё имя.') # здесь мы узнали user_id нового пользователя
        users.append({
            "name": None,
            "user_id": message.chat.id,
            "group": None
        })
        # Сохранить информацию о пользователях во внешний файл
        save()


@bot.message_handler(content_types=["photo", "text"]) # будут обрабатываться сообщения, подходящие по типу из список
def add_name(message):
    # получили сообщение от пользователя с номером user_id. теперь мы должны проверить, есть ли у этого пользователя имя
    for user in users:
        if user["user_id"] == message.chat.id:
            if user["name"] == None:
                user["name"] = message.text
                bot.send_message(message.chat.id, f"Приятно позанакомиться, {user['name']}. Укажите вашу группу - A или B")
                save()
            else:
                add_group(message)
    

def add_group(message):
    # получили сообщение  от пользователя с user_id и именем. должны проверить есть ли у него имя, и что у него с группой
    # если группы нет, записать группу из его сообщения
    for user in users:
        if user["user_id"] == message.chat.id:
            if user["name"] != None and user["group"] == None:
                if message.text == "A" or message.text == "B":
                    user["group"] = message.text # сохраняем только в том случае, если введённая пользователем группа одобрена
                    bot.send_message(message.chat.id, f"{user['name']} вы добавлены в группу {user['group']}")
                    save()
                else:
                    bot.send_message(message.chat.id, f"Введённой группы нет в списке известных нам групп")
                    
            elif user["group"] != None:
                handle(message)


def send_message_to_group(message, group):
    for user in users:
        if user["group"] == group:
            bot.send_message(user["user_id"], message)


def send_photo_to_group(photo, group, text=None):
    for user in users:
        if user["group"] == group:
            bot.send_photo(user["user_id"], photo)
            
            if text != None:
                bot.send_message(user["user_id"], text)


def handle_photo(message):
    group = "A"
    if message.caption != None:
        group = message.caption[0]
        text = message.caption[1:]
    else:
        text = None

    photo = message.photo[-1].file_id
    file = bot.get_file(photo)
    
    download_file = bot.download_file(file.file_path)
    send_photo_to_group(download_file, group, text)


def handle_text(message):
    group = message.text.split(" ")[0]
    text = "".join(message.text.split(" ")[1:]) # объединить список в строку
    send_message_to_group(text, group)


def handle_document(message):
    # попробуйте сделать самостоятельно    
    pass


def user_handle(message):
    features = {
        "weather": WeaherProcessor,
        "wiki": WikiProcessor,
        "course": CourseProcessor,
        "news": NewsProcessor,
    }
    """weather: <город> - получить погоду в городе"""
    """course"""
    """news"""
    """если приходит сторка вида wiki <текст> то ищем статью по этому тексту"""
    
    body = message.text
    query = body.split(" ")[0]
    try:
        text = body.split(" ")[1]
    except IndexError:
        text = None
    if query in features.keys():
        "query text"
        "weather москва"
        "wiki москва"
        obj = features[query](text)
        obj.run()
        bot.send_message(message.chat.id, obj.message)
    else:
        bot.send_message(message.chat.id, "Некорректный запрос введите weather, wiki, course или news")


# присылаем сообщение в виде "<название группы> <текст сообщения>"
def handle(message):
    handlers = {
        "text": handle_text,
        "photo": handle_photo,
        "document": handle_document
    }
    
    # получили сообщение. Должны проверить есть ли у нас права, если есть - выполнить рассылку
    for user in users:
        if user["user_id"] == message.chat.id and message.chat.id == admin_id:
            # проверить тип пришедшего сообщения. обработать в соответсвии с его типом. если это текст - переслать текс
            # если это фото - отрпавить текст вместе с фото
            handlers[message.content_type](message) # вызов функции по ключу content_type
        elif user["user_id"] == message.chat.id:
            user_handle(message)
            
bot.polling(none_stop=True, interval=0)


# Дома сделать: 
# 1 вынести admin_id в отдельный файл
# 2 удалить из списка users пользователей, с одинаковым user_id
# 3 нарисовать диаграмму с алгоритмом работы бота
# 4 подумать над проектом - придумать идею, составить план реализации
