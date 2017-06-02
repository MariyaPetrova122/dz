import flask
import telebot
import conf
from pymorphy2 import MorphAnalyzer
from random import choice
import re
morph = MorphAnalyzer()

def sep_words(m):
    #у маши все плохо, потому что курица ест дерево
    reg = re.compile('[a-яА-Я0-9]+|[.,;:?!]+')
    return reg.findall(m)
  

def get_me_a_word(m):
    #print(morph.parse(m))
    info = morph.parse(m)[0]
    key = str(info.tag).split()[0]
    if key in lemms:
        u_word_form = str(info.tag).split()
        if len(u_word_form) < 2:
            return m
        u_word_form = u_word_form[1]
        new_word = choice(lemms[key])
        a = morph.parse(new_word)[0]
        useful_form = a.inflect(set(u_word_form.split(',')))
        return useful_form.word
    else:
        return m

lemms = {}

f = open('1grams-3.txt','r',encoding = 'utf-8')
data = f.readlines()
data = data[:10000]
for i in data:
    lexema = i.split()[1]
    first = morph.parse(lexema)[0]
    # print(first.word, str(first.tag).split()[0])
    key = str(first.tag).split()[0]
    if key in lemms:
        lemms[key].append(first.word)
    else:
        lemms[key] = [first.word]
#print(lemms)
#print(sum([len(v) for k, v in lemms.items()]))


WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Этот бот, отправит тебе предложение, которое очень похоже на твое, но заменит в нем слова на другие. \n Отправь мне /start, чтобы начать!")

@bot.message_handler(commands=['start'])
def ask_for_phrase(message):
	bot.send_message(message.chat.id, "Отправь же мне какую-нибудь фразу!")

final_phrase = ''

@bot.message_handler(content_types=["text"])  # reacts to any text message
def send_new_phrase(message):
    #user_sent = input("enter text: ")
    user_words = message.split()
    for m in user_words:
        for w in sep_words(m):
            final_phrase += w          
    tb.reply_to(message, final_phrase) #text
    #print(get_me_a_word(w), end = '')
    #print(end = ' ')

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
