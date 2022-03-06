from cgi import test
import random
import re
import nltk
import pickle
import json 
import os.path

'''
 BOT_CONFIG = {
    "intents": { # Намерения пользователя
        "hello": { # Намерение поздороваться
            "examples": ["Привет", "Добрый день", "Шалом", "Здрасте", "Здравствуйте", "Доброе время суток"],
            "responses": ["Привет, человек", "И вам здрасте", "Йоу"],
        },
         "bye": { # Намерение попрощаться 
            "examples": ["Пока", "До свидания", "Досвидос", "Прощай"],
            "responses": ["Счастливо", "До свидания", "Если что - возвращайтесь"]
        },
        "how_are_you": { # Намерение узнать как дела
            "examples": ["Как дела", "Что делаешь", "Какие делища", "Как поживаешь", "Чо как"],
            "responses": ["Маюсь фигней", "Учу Python", "Смотрю вебинары Скиллбокс"],      
        },
    },
    "failure_phrases": ["Йа ничо ни понил", "Что-то непонятно", "Я всего лишь бот, сформулируйте попроще"]
} ##
'''
project_path = "/home/user/environments/my_env/script/chat_bot/"
with open(project_path + 'big_bot_config.json') as config_file:
    BOT_CONFIG = json.load(config_file)

def filter(text): # Функция, которая приводит текст к нижнему регистру и убирает занки препинания
    text = text.lower() # Приводит текст к нижнему регистру
    punctuation = r"[^\w\s]" # Регулярное выражение позволяет выбрать все кроме(^) букв(\w) и пробелов(\s)
    return re.sub(punctuation, "", text) # Заменяет все знаки препинания на пустую строку

def isMatching(text1, text2): #  Функция, которая производит расчет на сколько тексты различны(схожи)
    text1 = filter(text1)
    text2 = filter(text2)
    distance = nltk.edit_distance(text1, text2) # Расчет растояния между двумя текстами (их различие)
    average_length = (len(text1) + len(text2)) / 2 # Расчет средней длины текстов
    return distance / average_length < 0.4 # Возращает совпадают тексты или нет

def getIntent(text):
    all_intents = BOT_CONFIG["intents"]
    for name, date in all_intents.items(): # пройти все намерения и положиь названия в name, остальное в data
        for example in date['examples']: # пройти по всем примерам этого интента и положить текст в переменную example
            if isMatching(text, example): # если текст совпадает с примером
                return name

def getAnswer(intent):
    responses = BOT_CONFIG['intents'][intent]["responses"]
    return random.choice(responses)

def bot(text): # Функция = бот
    intent = getIntent(text)
    if not intent: #  Если намерение не найдено
        test = vectorizer.transform([text])
        intent = model.predict(test)[0] # Подключить модель машинного обучения

    print('Intent =', intent)

    if intent: # если намерение найдено - вывести ответ
        return getAnswer(intent)
    
    # Заглушка
    failure_phrases = BOT_CONFIG['failure_phrases']
    return random.choice(failure_phrases)

# Создание модели машинного обучения (задача модели - это по "х" научиьтся находить "н")

# 1. Собрать тексты
x = []
# 2. Собрать классы 
y = []

for name, data in BOT_CONFIG["intents"].items():
    for example in data['examples']:
        x.append(example)
        y.append(name)

# NLP / NLU
# Свсести набор текстов к набору чисел
# Подключем библиотеку векторайзера
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = CountVectorizer()
# vectorizer = TfidfVectorizer()
vectorizer.fit(x) # передать набор текстов, чтобы их проанализировать и обучить vectorizer

x_vectorized = vectorizer.transform(x) #  перекодировать тексты в вектора (наборы чисел)

# выбор модели (на данный момент  LogisticRegression)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

file_name = 'model.bin'
if  not os.path.isfile(project_path + file_name): # Если не существует файла модели, обучить модель и записать в файл
   # model = LogisticRegression()
    model = RandomForestClassifier()
    model.fit(x_vectorized, y) #  обучение модели по "х" опрределить "y"
    pickle.dump(model, open(project_path + file_name, 'wb'))
else: # Если файл модели есть загрузить модель из файла
    model = pickle.load(open(project_path + file_name, 'rb'))

# print(model.score(x_vectorized, y))
'''
text = input()
while text != 'стоп':
    print(bot(text))
    text = input()
'''
# Зарегистратировать нового бота и получить ключ доступа @BotFather
# Подключить наш лод к библиотеке telegram-bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_KEY = '5285593507:AAAH1LLOeH8c2CCMHNFG238JyVQLk5eSkW3o'

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


updater = Updater(BOT_KEY)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
