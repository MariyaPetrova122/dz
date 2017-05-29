import flask
import telebot
import conf
import random
import shelve
from telebot import types

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

# предположим, отзывы у нас хранятся в виде csv-файла с номерами отзывов и собственно текстами
with open('/home/2016learnpython/myapp/reviews.csv', 'r', encoding='utf-8') as f:
    reviews = {}  # создадим словать отзывов
    for line in f:
        num, text = line.strip().split('\t')
        reviews[num] = text
review_keys = list(reviews.keys())  # и отдельно массив ключей


# собираем клавиатуру для разметки (возможно имеет смысл добавить кнопку "не знаю"?)
keyboard = types.ReplyKeyboardMarkup(row_width=3)
btn1 = types.KeyboardButton('+')
btn2 = types.KeyboardButton('-')
btn3 = types.KeyboardButton('=')
keyboard.add(btn1, btn2, btn3)

# shelve используется как мини-база данных, там можно хранить файлы в виде "ключ-значение"
# в этой базе мы будем хранить информацию о том, какой отзыв мы недавно прислали юзеру
shelve_name = '/home/USERNAME/myapp/shelve.db'  # Файл с хранилищем

def set_user_review(chat_id, review):
    """
    Записываем юзера в базу данных и запоминаем номер отзыва, который мы ему дали
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = review


def get_user_review(chat_id):
    """
    Вспоминаем, какой отзыв мы отправили на разметку
    :return: (str) Номер отзыва / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            review = storage[str(chat_id)]
            return review
        # Если человека нет в базе, ничего не возвращаем
        except KeyError:
            return None

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команду /help
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот для разметки отзывов на кинофильмы.\n Положительные отзывы отмечаются плюсом +, отрицательные минусом -, а нейтральные знаком равно =.\n Для того, чтобы начать отправьте команду /start.")

# этот обработчик запускает функцию, когда пользователь отправляет команду /start
@bot.message_handler(commands=['start'])
def send_first_review(message):
    review_num = random.choice(review_keys)
    bot.send_message(message.chat.id, reviews[review_num], reply_markup=keyboard)
    set_user_review(message.chat.id, review_num)


@bot.message_handler(regexp='[-+=]')  # этот обработчик реагирует на символы разметки и записывает результаты
def get_answer(message):
    review_num = get_user_review(message.chat.id)  # проверяем, есть ли юзер в базе данных
    if review_num:
        # если есть, открываем файл с результатами и записываем туда разметку
        with open('/home/USERNAME/myapp/results.csv', 'a', encoding='utf-8') as results:
            results.write(review_num + '\t' + message.text + '\n')
        # и сразу отправляем новый отзыв
        review_num = random.choice(review_keys)
        bot.send_message(message.chat.id, reviews[review_num], reply_markup=keyboard)
        set_user_review(message.chat.id, review_num)
    else:
        # если нет, то что-нибудь говорим об этом
        bot.send_message(message.chat.id, 'Вы не разметили отзыв.')


# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
