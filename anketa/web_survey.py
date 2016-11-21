from flask import Flask
from flask import url_for, render_template, request, redirect
import json

app = Flask(__name__)

@app.route('/')
def form():
    list_of_sentences = {
        '1':'Молодец',
        '2':'Ой,какой ты молодец',
        '3':'Иди куда хочешь',
        '4':'Нет, не обиделась',
        '5':'Все хорошо'}
    if request.args:
        return render_template('stats.html')
    return render_template('form.html', list_of_sentences = list_of_sentences)
answers = []
@app.route('/json')
def get_data():
    all_answers = json.dumps(request.args, ensure_ascii = False)
    new_answers = json.loads(all_answers) #класс - словарь
    with open('people_responds_temp.json', 'w', encoding = 'utf-8-sig') as f:
        json.dump(new_answers, f, ensure_ascii = False) #складываем ответы
    f.close()
    
    with open('people_responds_temp.json', 'r', encoding = 'utf-8-sig') as f:
        all_resp = json.load(f)
        answers.append(all_resp)
    f.close()
    with open('people_responds.json', 'w', encoding = 'utf-8-sig') as f:
        json.dump(answers,f,ensure_ascii=False)
    f.close()
    with open('people_responds.json', 'r', encoding = 'utf-8-sig') as f:
        final_resp = json.load(f)
    f.close()
    return render_template('results.html',final_resp =final_resp)

women = []
men = []
women_help = []
men_help = []
w_1 = []
w_2 = []
w_3 = []
w_4 = []
w_5 = []
m_1 = []
m_2 = []
m_3 = []
m_4 = []
m_5 = []


@app.route('/stats')
def get_stats():
    with open('people_responds.json', 'r', encoding = 'utf-8-sig') as f:
        need_for_stat = json.load(f)
    f.close()
    for i in need_for_stat:
        if i['gender'] =='woman':
            women.append(i)
        else:
            men.append(i)
            
    for i in women:
        w_1.append(i['1'])
        w_2.append(i['2'])
        w_3.append(i['3'])
        w_4.append(i['4'])
        w_5.append(i['5'])
    for i in men:
        m_1.append(i['1'])
        m_2.append(i['2'])
        m_3.append(i['3'])
        m_4.append(i['4'])
        m_5.append(i['5'])
        
        
    return render_template('stats.html', need_for_stat=need_for_stat, men = men, women= women, w_1=w_1,w_2=w_2,w_3=w_3,w_4=w_4,w_5=w_5,m_1=m_1,m_2=m_2,m_3=m_3,m_4=m_4,m_5=m_5)
        
@app.route('/search')
def search():
    if request.args:
        number = request.args['number']
        gender = request.args ['gender']
        if request.args['gender'] == 'woman':
            if request.args['number'] == '1':
                here_we_go = w_1
            elif request.args['number'] == '2':
                here_we_go = w_2
            elif request.args['number'] == '3':
                here_we_go = w_3
            elif request.args['number'] == '4':
                here_we_go = w_4
            else:
                here_we_go = w_5
        else:
            if request.args['number'] == '1':
                here_we_go = m_1
            elif request.args['number'] == '2':
                here_we_go = m_2
            elif request.args['number'] == '3':
                here_we_go = m_3
            elif request.args['number'] == '4':
                here_we_go = m_4
            else:
                here_we_go = m_5
                           
        return render_template('search_results.html',number = number, gender = gender, here_we_go=here_we_go)
    return render_template('search.html')

@app.route('/results')
def get_search_result():
    return render_template('search_results.html',number = number, gender = gender,here_we_go=here_we_go)

if __name__ == '__main__':
    app.run(debug=True)
