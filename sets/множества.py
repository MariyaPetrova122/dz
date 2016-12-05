import urllib.request # импортируем модуль
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
regCleanClean = re.compile('\t', flags=re.U | re.DOTALL)

text = regText.findall(html)
for t in text:
        clean_text=regClean.sub("",t)
        cl_text = regCl.sub("",clean_text)
        cleaner_text= regCleaner.sub("",cl_text)
        cleanest_text = regCleanest.sub("", cleaner_text)
        super_clean = regCleanClean.sub("", cleanest_text)
        #print(super_clean)
        first = super_clean.split(' ')

s_first = set(first)
#print(s_first)
        

req = urllib.request.Request(second_link)
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
regText = re.compile('</script></div></div></div>.*?<div class="b-article__bottom-info">', flags=re.U | re.DOTALL)
regCl = re.compile('{.*?}', flags=re.U | re.DOTALL)
regClean = re.compile('<.*?>', flags=re.U | re.DOTALL)
regCleaner = re.compile('\n', flags=re.U | re.DOTALL)
regCleanest = re.compile('&nbsp;', flags=re.U | re.DOTALL)
second = []
text = regText.findall(html)
for t in text:
        clean_text=regClean.sub("",t)
        cl_text = regCl.sub("",clean_text)
        cleaner_text= regCleaner.sub("",cl_text)
        cleanest_text = regCleanest.sub("", cleaner_text)
        #print(cleanest_text)
        second = cleanest_text.split(' ')

s_second = set(second)
#print(s_second)


req = urllib.request.Request(third_link)
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
regText = re.compile('<div class="text" itemprop="articleBody" id="hypercontext">.*?</div></article><div class="externalBlock">', flags=re.U | re.DOTALL)
regClean = re.compile('<.*?>', flags=re.U | re.DOTALL)
regCleaner = re.compile('\n', flags=re.U | re.DOTALL)

text = regText.findall(html)
third = []
for t in text:
        clean_text=regClean.sub("",t)
        cleaner_text= regCleaner.sub("",clean_text)
        #print(clean_text)
        third = clean_text.split(' ')

s_third = set(third)
#print(s_third)


req = urllib.request.Request(fourth_link)
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
regText = re.compile('<span class="_ga1_on_ include-relap-widget contextualizable">.*?</p>', flags=re.U | re.DOTALL)
regClean = re.compile('<.*?>', flags=re.U | re.DOTALL)
regCleaner = re.compile('\n', flags=re.U | re.DOTALL)
regCleanest = re.compile('\xa0', flags=re.U | re.DOTALL)
regCleanClean = re.compile('\r', flags=re.U | re.DOTALL)

text = regText.findall(html)
fourth = []
for t in text:
        clean_text=regClean.sub("",t)
        cleaner_text= regCleaner.sub("",clean_text)
        cleanest_text = regCleanest.sub("", cleaner_text)
        super_clean = regCleanClean.sub("", cleanest_text) # type = str
        #print(super_clean)
        fourth = super_clean.split(' ')

s_fourth = set(fourth)
#print(s_fourth)



cross_first_second = s_first&s_second
cross_first_third = s_first&s_third
cross_first_fourth = s_first&s_fourth
cross_second_third = s_second&s_third
cross_second_fourth = s_second&s_fourth
cross_third_fourth = s_third&s_fourth

cross_all = s_first&s_second&s_third&s_fourth 
subtract_all = s_first^s_second^s_third^s_fourth

#print(cross_all)
#print(subtract_all)

f = open('cross.txt','w')
for i in sorted(cross_all):
    f.write(i + '\n')
f.close()

f = open('subtract.txt','w')
for i in sorted(subtract_all):
    f.write(i + '\n')
f.close()

