import flask
import telebot
import conf
import urllib.request
import json
import networkx as nx
import matplotlib.pyplot as plt

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Этот бот расскажет тебе о друзьях твоих друзей. Зови меня Большой Брат. \n Отправь мне /start, чтобы начать!")

@bot.message_handler(commands=['start'])
def ask_for_phrase(message):
	bot.send_message(message.chat.id, "Отправь же мне id пользователя,о котором ты хочешь что-то узнать!")

request=''

@bot.message_handler(regexp="[0-9]+|")
def handle_message(message):
    request = urllib.request.Request('https://api.vk.com/method/friends.get?user_id='+str(message))
    response = urllib.request.urlopen(request)
    result = response.read().decode('utf-8')
    main_list = json.loads(result)
    friends = main_list['response']
    main_friends = friends
    labels = {}
    G = nx.Graph()
    for ids in friends:
        req = urllib.request.Request('https://api.vk.com/method/users.get?user_id='+str(ids))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        user_info = json.loads(result)
        name = user_info['response'][0]['last_name']+' '+user_info['response'][0]['first_name']
        labels[ids]=name
        G.add_node(ids,label = name)
    for friend in main_friends:
        req = urllib.request.Request('https://api.vk.com/method/friends.get?user_id='+str(friend))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        main_list = json.loads(result)
        try:
            friends = main_list['response']
            for i in main_friends:
                if i in friends:
                    G.add_edge(friend,i)
        except:
            print("Oops!")
            pass
    nx.write_gexf(G, 'graph_file.gexf') #ПРОПИСАТЬ ПУТЬ НА пав
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='red', node_size=50)
    nx.draw_networkx_edges(G, pos, edge_color='yellow')
    nx.draw_networkx_labels(G, pos,labels,font_size=20, font_family='Arial')
    plt.axis('off')
    plt.savefig("https://www.pythonanywhere.com/user/bigbrother/mysite/Graph.png", format="PNG")
    bot.send_message(message.chat.id, 'Количество друзей пользователя:'+ G.number_of_nodes()+'/n'+'Количество отношений между друзьями пользователя:'+G.number_of_edges()+'/n'+'Связанность узлов графа'+nx.transitivity(G))
    photo = open('https://www.pythonanywhere.com/user/bigbrother/mysite/Graph.png', 'rb')
    tb.send_photo(chat_id, photo)


@bot.message_handler(regexp="[a-яА-Я]+|[.,;:?!]")
def handle_message(message):
    bot.send_message(message.chat.id, 'Большой брат расстроен, ведь он просил тебя отправить ему id, состоящее из цифр!')

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
