import urllib.request
import json
import sys
import matplotlib.pyplot as plt
from matplotlib import style  # добавляем стили
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) #нужно будет, чтобы убрать смайлики

offsets = [0,50,100]
posts = []
all_ids = []
for off in offsets:
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-55284725&offset=' + str(off)+'&count=50')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    post = [text['text'].translate(non_bmp_map) for text in data['response'][1:]]
    ids = [text['id'] for text in data['response'][1:]]
    posts = posts + post
    all_ids = all_ids + ids

post_info = []
i=0
while i < len(all_ids):
    post_info.append([all_ids[i],posts[i],len(posts[i].split(' '))]) #массив списков, где указаны id поста, сам пост и его длина
    i+=1

final_com = [] #id поста и все комментарии к нему
general_length = {} #словарь, где ключ - id поста, значение - средняя длина комментариев к нему
user_info = {}
for num_post in all_ids:
    comments = []
    all_comments = []
    all_users = []
    length_com = 0
    offsets = [0,50,100]
    for off in offsets:
        req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-55284725&post_id='+str(num_post)+'&offset=' + str(off)+'&count=50')
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        comments = [text['text'].translate(non_bmp_map) for text in data['response'][1:]] #массив со всеми комментариями к одному посту + избавляемся от смайликов
        users = [text['uid'] for text in data['response'][1:]]
        all_comments+=comments #собираем комментарии со всех оффсетов
        all_users+=users
    for one_com in all_comments:
        length_com += len(one_com.split(' ')) #считаем сумму длин всех комментариев
    general_length[num_post] = round(length_com/len(all_ids)) #словарь, где ключ - id поста, значение - средняя длина комментариев к нему
    final_com.append([str(num_post),all_comments]) #собираем массив [id поста,  все комментарии к нему]

user_info = [] #id юзера и средняя длина его постов
k = 0
while k<len(all_users):
    user_info.append([all_users[k],len(all_comments[k].split(' '))])
    k+=1
'''
f = open('posts.txt','w',encoding = 'utf-8' #создаем текстовый файл с инф-ей о постах
for one_post in post_info:
    f.write('Текст поста:'+'\n'+one_post[1]+'Длина поста = '+one_post[2])
f.close()

with open('comments.txt', 'w',encoding='utf-8') as outfile: #создаем текстовый файл с инф-ей о комментариях
    json.dump(final_com, outfile, ensure_ascii=False)
'''

cities = []
for user in all_users:
    req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&fields=home_town'.format(str(user)))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    if 'home_town' not in (data['response'][0]):
        continue
    if data['response'][0]['home_town']!= '':
        cities.append([user,data['response'][0]['home_town']])

birthdays = []
for user in all_users:
    req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&fields=bdate'.format(str(user)))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    if 'bdate' not in (data['response'][0]):
        continue
    else:
        birthdays.append([user,data['response'][0]['bdate']])


post_com_len = {} #собираем массив с парами "длина поста" - "средняя длина комментариев к нему"
for one in post_info:
    post_com_len[one[2]]=general_length[one[0]]


def average_len(user_info,id_key): #функция дает на выходе словарь, включающий город и средн.длину поста или возраст и среднюю длину поста
    smart_user_info = {} #'smart'словарь, ключ - id юзера, значения - список: длины  всех его комментариев
    for c in user_info:
        if c[0] in smart_user_info:
            smart_user_info[c[0]].append(c[1])
        else:
            smart_user_info[c[0]] = [c[1]]
    keys = {} #словарь, ключ - город(возраст), значения -  id юзеров из этого города(возраста)
        if u[1] in keys:
            keys[u[1]].append(u[0])
        else:
            keys[u[1]] = [u[0]]
    average = {} #словарь, ключ - город(возраст), значения -  id юзеров из этого города(возраста)
    for key in keys.keys():
        ids = keys[key] #список юзеров для одного города(возраста)
        s = 0
        n = 0
        for u in ids:
            if u in smart_user_info: #если юзер в нашем 'smart'словаре
                s += sum(smart_user_info[u]) #сумма длин
                n += len(smart_user_info[u]) #кол-во длин
        average[key] = 0 if n == 0 else round(s / n)
    return average


def year(s): #найти год
    return int(s[-4:]) if '.' not in s[-4:] else -1

def id_age(birthdays): #найти возраст
    return [[u[0], 2017 - year(u[1])] for u in id_year if year(u[1]) > 0]

avg_by_city = average_len(user_info, cities)
avg_by_age = average_len(user_info, id_age(birthdays))

def dict_to_xy(d): #сделать из словаря два массива для построения графика
    x = []
    y = []
    for key in d.keys():
        x.append(key)
        y.append(d[key])
    return x, y

def plot_text(X, Y, header, xlabel, ylabel):
    style.use('ggplot')
    plt.figure(figsize=(30,15))
    plt.grid(True, color = 'black')  #вид сетки
    plt.xticks(range(len(X)), X, rotation = 90)
    plt.scatter(range(len(X)), Y, color = 'red', s = 10)
    plt.title(header)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(header)


def plot_numbers(X, Y, header, xlabel, ylabel):
    style.use('ggplot')
    plt.grid(True, color = 'black')  #вид сетки
    plt.scatter(X, Y, color = 'red', s = 5)
    plt.title(header)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(header)

x, y = stats.dict_to_xy(post_com_len)
plot.plot_numbers(X, Y, 'Соотношение длины поста с длинной комментариев','Средняя длина комментариев', 'Длина поста')

x, y = stats.dict_to_xy(avg_by_city)
plot.plot_text(x, y, 'avg_by_city', 'city', 'avg')

x, y = stats.dict_to_xy(avg_by_age)
plot.plot_numbers(x, y, 'avg_by_age', 'age', 'avg')



