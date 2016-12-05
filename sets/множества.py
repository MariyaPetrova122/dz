import urllib.request # импортируем модули
import re

links = ["http://tass.ru/mezhdunarodnaya-panorama/3838909","https://ria.ru/spravka/20161204/1482734890.html","http://www.kp.ru/online/news/2589517/","http://echo.msk.ru/news/1886080-echo.html"]
first_link = links[0]
second_link = links[1]
third_link = links[2]
fourth_link = links[3]

req = urllib.request.Request(first_link)
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
regText = re.compile('<div class="b-material-text__l js-mediator-article">.*?<div id="block_material_text_broadcast"', flags=re.U | re.DOTALL)
regCl = re.compile('<div id="block_material_text_broadcast"', flags=re.U | re.DOTALL)
regClean = re.compile('<.*?>', flags=re.U | re.DOTALL)
regCleaner = re.compile('\n', flags=re.U | re.DOTALL)
regCleanest = re.compile('&nbsp;', flags=re.U | re.DOTALL)
regCleanClean = re.compile('\t', flags=re.U | re.DOTALL) #регулярки для чистки текста

text = regText.findall(html)
for t in text:
        clean_text=regClean.sub("",t)
        cl_text = regCl.sub("",clean_text)
        cleaner_text= regCleaner.sub("",cl_text)
        cleanest_text = regCleanest.sub("", cleaner_text)
        super_clean = regCleanClean.sub("", cleanest_text) #чистим текст
        first = super_clean.split(' ') #создаем список, элементы которого - слова из текста
s_first = set(first) #преобразуем список во множество
    
   
req = urllib.request.Request(second_link)
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
regText = re.compile('</script></div></div></div>.*?<div class="b-article__bottom-info">', flags=re.U | re.DOTALL)
regCl = re.compile('{.*?}', flags=re.U | re.DOTALL)
regClean = re.compile('<.*?>', flags=re.U | re.DOTALL)
regCleaner = re.compile('\n', flags=re.U | re.DOTALL)
regCleanest = re.compile('&nbsp;', flags=re.U | re.DOTALL) #регулярки для чистки текста
second = []
text = regText.findall(html)
for t in text:
        clean_text=regClean.sub("",t)
        cl_text = regCl.sub("",clean_text)
        cleaner_text= regCleaner.sub("",cl_text)
        cleanest_text = regCleanest.sub("", cleaner_text) #чистим текст
        second = cleanest_text.split(' ') #создаем список, элементы которого - слова из текста

s_second = set(second) #преобразуем список во множество


req = urllib.request.Request(third_link)
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
regText = re.compile('<div class="text" itemprop="articleBody" id="hypercontext">.*?</div></article><div class="externalBlock">', flags=re.U | re.DOTALL)
regClean = re.compile('<.*?>', flags=re.U | re.DOTALL)
regCleaner = re.compile('\n', flags=re.U | re.DOTALL) #регулярки для чистки текста

text = regText.findall(html)
third = []
for t in text:
        clean_text=regClean.sub("",t)
        cleaner_text= regCleaner.sub("",clean_text) #чистим текст
        third = clean_text.split(' ') #создаем список, элементы которого - слова из текста

s_third = set(third) #преобразуем список во множество


req = urllib.request.Request(fourth_link)
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
regText = re.compile('<span class="_ga1_on_ include-relap-widget contextualizable">.*?</p>', flags=re.U | re.DOTALL)
regClean = re.compile('<.*?>', flags=re.U | re.DOTALL)
regCleaner = re.compile('\n', flags=re.U | re.DOTALL)
regCleanest = re.compile('\xa0', flags=re.U | re.DOTALL)
regCleanClean = re.compile('\r', flags=re.U | re.DOTALL) #регулярки для чистки текста

text = regText.findall(html)
fourth = [] 
for t in text:
        clean_text=regClean.sub("",t)
        cleaner_text= regCleaner.sub("",clean_text)
        cleanest_text = regCleanest.sub("", cleaner_text)
        super_clean = regCleanClean.sub("", cleanest_text) #чистим текст
        fourth = super_clean.split(' ') #создаем список, элементы которого - слова из текста

s_fourth = set(fourth) #преобразуем список во множество


cross_all = s_first&s_second&s_third&s_fourth #находим пересечение всех множеств (общие слова)
subtract_all = s_first^s_second^s_third^s_fourth #находим симметричную разность ( слова, которые не встречаются в других статьях)

f = open('cross.txt','w') #записываем в файл общие слова
for i in sorted(cross_all): # sorted - для алфавитного порядка
    f.write(i + '\n')
f.close()

f = open('subtract.txt','w') #записываем в файл слова, которые не встречаются в других статьях
for i in sorted(subtract_all): # sorted - для алфавитного порядка
    f.write(i + '\n')
f.close()

