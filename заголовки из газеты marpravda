url = 'http://marpravda.ru/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'  
import urllib.request   
req = urllib.request.Request('http://marpravda.ru/', headers={'User-Agent':user_agent})  
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
import re
regPostTitle = re.compile('<div class="news_name".*?</div>', flags=re.DOTALL)
titles = regPostTitle.findall(html)
new_titles = []
regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
for t in titles:
    clean_t = regSpace.sub("", t)
    clean_t = regTag.sub("", clean_t)
    new_titles.append(clean_t)
f = open('text.txt', 'w')    
for t in new_titles:
    #print(t.replace("&quot;", "'"))
    f.write(t.replace("&quot;", "'")+"\n")
f.close()
