import os
os.system(r'C:\Python34\mystemish\mystem.exe -nidcs C:\Python34\mystemish\input.txt C:\Python34\mystemish\output.txt')

f = open('output.txt','r',encoding='UTF-8')
a = f.readlines()

i=1 #счетчик для получения словоформ и лемм
j=0 #счетчик для получения пунктуации
k=1 #номер слова в тексте

table_lemma = {} #ключ - словоформа, значение - лемма
table_number = {} #ключ - номер в тексте, значение - словоформа
table_leftpunc = {} #ключ - номер словоформы, значение - пунктуация слева
table_rightpunc = {} #ключ - номер словоформы, значение - пунктуация справа

keys = [] #список всех словоформ

while i<len(a)and k<len(a)/2:
    parts = a[i].split('{')
    info = parts[1].split('=')
    table_lemma[parts[0]] = info[0] #parts[0] = словоформы, info[0] = леммы
    table_number[k] = parts[0]
    keys.append(parts[0])
    table_leftpunc[k] = a[j] #a[j] = пунктуация
    j+=2
    table_rightpunc[k] = a[j]
    i+=2
    k+=1
    
f.close()
    
low_keys = [] #список из словоформ в нижнем регистре
all_wordforms = {} #словарь,в котором ключ - словоформа в нижнем регистре, а значение - в том виде, в каком эта словоформа встречается в тексте

for p in keys:
        low_wordform = p.lower()
        low_keys.append(low_wordform) #создаем список из словоформ в нижнем регистре
        all_wordforms[low_wordform] = p
        
low_keys = set(low_keys) #убираем повторяющиеся словоформы

f = open('tables.sql','w', encoding='UTF-8')

f.write('CREATE TABLE infowords (id INTEGER,wordform VARCHAR,lemma VARCHAR);'+'\n') #создаем вторую таблицу: словоформа  - лемма
num_lemma = {} #словарь для хранения id леммы из второй таблицы, чтобы заполнить столбик idLemma в первой таблице
r=1
for n in low_keys:
    b = table_lemma[all_wordforms[n]] #находит соответсвующую лемму
    f.write('INSERT INTO infowords (id,wordform,lemma) VALUES ('+str(r)+',"'+n+'","'+b+'");'+'\n')#добавляем значения в поля
    num_lemma[b] = r
    r+=1

f.write('CREATE TABLE words (id INTEGER,wordform VARCHAR,puncleft VARCHAR,puncright VARCHAR,numberInText INTEGER,idLemma INTEGER);'+'\n') # создаем первую таблицу
m=1
while m<k:
    g = num_lemma[table_lemma[table_number[m]]] #id леммы, соответствующей данной словоформе
    f.write('INSERT INTO words (id,wordform,puncleft,puncright,numberInText,idLemma) VALUES ('+str(m)+',"'+str(table_number[m])+'","'+str(table_leftpunc[m])+'","'+str(table_rightpunc[m])+'",'+str(m)+','+str(g)+');'+'\n');
    m+=1

f.close()

