import os
os.system(r'C:\Python34\mystemish\mystem.exe -nidcs C:\Python34\mystemish\input.txt C:\Python34\mystemish\output.txt')

f = open('output.txt','r',encoding='UTF-8')
a = f.readlines()

i=1 #счетчик для получения словоформ и лемм
j=0 #счетчик для получения пунктуации
k=1 #номер слова в тексте

table_lemma = {} #ключ - словоформа, значение - лемма
table_number = {} #ключ - номер в тексте, значение - словоформа
table_leftpunc = {} #ключ - словоформа, значение - пунктуация слева
table_rightpunc = {} #ключ - словоформа, значение - пунктуация справа

while i<len(a)and k<len(a)/2:
    parts = a[i].split('{')
    #print(parts[0])
    info = parts[1].split('=')
    #print(info[0])
    table_lemma[parts[0]] = info[0] #parts[0] = словоформы, info[0] = леммы
    table_number[k] = parts[0]
    table_leftpunc[k] = a[j] #a[j] = пунктуация
    j+=2
    table_rightpunc[k] = a[j]
    i+=2
    k+=1
  
f.close()
    
m=1
r=1

f = open('tables.sql','w', encoding='UTF-8')
f.write('CREATE TABLE words (id INTEGER,wordform VARCHAR,puncleft VARCHAR,puncright VARCHAR,numberInText INTEGER,idLemma INTEGER);'+'\n')
while m<k:
    f.write('INSERT INTO words (id,wordform,puncleft,puncright,numberInText,idLemma) VALUES ('+str(m)+',"'+str(table_number[m])+'","'+str(table_leftpunc[m])+'","'+str(table_rightpunc[m])+'",'+str(m)+','+str(m)+');'+'\n');
    m+=1
f.write('CREATE TABLE infowords (id INTEGER,wordform VARCHAR,lemma VARCHAR);'+'\n')
while r<k:
    low_wordform = table_number[r].lower()
    f.write('INSERT INTO infowords (id,wordform,lemma) VALUES ('+str(r)+',"'+low_wordform+'","'+table_lemma[table_number[r]]+'");'+'\n')
    r+=1
f.close()

