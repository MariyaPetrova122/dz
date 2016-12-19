import re
import urllib.request

 
req = urllib.request.Request('http://www.adygvoice.ru/wp/category/politics/')
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
   

regText = re.compile('>.*?<', flags=re.U | re.DOTALL)
regCleanText = re.compile('><',flags=re.U | re.DOTALL)
regCleanerText = re.compile('\n\.*?t',flags=re.U | re.DOTALL)
regCleanClean =  re.compile('>',flags=re.U | re.DOTALL)
regClClClean =  re.compile('<',flags=re.U | re.DOTALL)
regGR = re.compile('<div class="infinitescroll">.*?<div id="site-info">',flags=re.U | re.DOTALL)
reg = re.compile('[a-яА-Я0-9]+|[.,;:?!]')


text = regText.findall(html)
clean_text = regCleanText.sub('',str(text))
cleaner_text = regCleanerText.sub('',clean_text)
cleanest_text = regCleanClean.sub('',cleaner_text)
the_cleanest_text = regClClClean.sub('',cleanest_text)
get_rid_text = regGR.sub('', the_cleanest_text)
k = reg.findall(get_rid_text)

allwords = []

a = open('adyghe-unparsed-words.txt', 'r', encoding = 'UTF-8')
for line in a:
    line = line[:-2]
    allwords.append(line)
    
allwords = set(allwords)
k = set(k)
special_words = k & allwords


file = open('wordlist.txt','w',encoding = 'UTF-8')
file.write(special_words)
file.close()

