
# -*- coding: utf-8 -*-
import flask
import telebot
import conf

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Салют, Вера! Этот бот, позволит тебе общаться с тем, кто всегда поймет и поддержит. Встречай Меладзе-Бот!")

greet_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_hi)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет, Валера! Я скучал.", reply_markup=kb.greet_kb)

@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует все прочие сообщения
def send_len(message):
	bot.send_message(message.chat.id, 'В вашем сообщении {} символов.'.format(len(message.text)))
  
button1 = KeyboardButton('Давай поговорим, мне нужно излить душу.)
button2 = KeyboardButton('Хочу песню!')


markup3 = ReplyKeyboardMarkup().add(
    button1).add(button2)
    
@dp.message_handler(commands=['hi3'])
async def process_hi3_command(message: types.Message):
    await message.reply("Третье - добавляем больше кнопок", reply_markup=kb.markup3)
			 
@dp.callback_query_handler(func=lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
    chat_handler = CommandHandler('talk', lets_talk, pass_args=True)
    updater.dispatcher.add_handler(chat_handler)
			 
@send_typing_action
def lets_talk(bot, update):
    args = input("Entre a phrase: ")
    with open('texts.txt', 'r') as data:
        data = data.read().split('\n')
        model= Doc2Vec.load("d2v.model")
        #to find the vector of a document which is not in training data
        test_data = [w for w in word_tokenize(' '.join(args).lower()) if w.isalnum()]
        v1 = model.infer_vector(test_data)
        similar_doc = model.docvecs.most_similar([v1])
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id, text=data[int(similar_doc[0][0])])



    
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
        
     
if __name__ == '__main__':
    bot.polling(none_stop=True)
