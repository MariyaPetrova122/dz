import urllib.request
import re


def export_text():
    regTextInFile = re.compile('<article>.*?</article>', flags=re.U | re.DOTALL)
    text_article = regTextInFile.findall(html)
    if (len(text_article))==0:
        i==i-1
        pass
    else:
        name="Статья"+str(i)+".txt"
        f=open(name,"x")
        f.write(str(text_article))
        f.close()


main_url = 'http://marpravda.ru/'
req = urllib.request.Request(main_url)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')


regPostTitle = re.compile('<div class="news_name"><a href="/news/assosiations/.*?/">.*?</a></div>', flags=re.U | re.DOTALL)
links = regPostTitle.findall(html)
new_links = []

regBeforeLink = re.compile('<.*?href="', flags=re.U | re.DOTALL)
regAfterLink = re.compile('">.*?div>', flags=re.U | re.DOTALL)
regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
for t in links:
    clean_t = regBeforeLink.sub("", t)
    clean_t = regAfterLink.sub("", clean_t)
    clean_t = regSpace.sub("", clean_t)
    new_links.append(clean_t)
    checked_links = []

i = 0
while i < 534:
    if checked_links.count(new_links[0]) == 0:
        url = main_url+new_links[0]+"/"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        print(i)

        try:
            export_text()
        except:
            pass


        regPostTitle = re.compile('<a href="/news/.*?/".*?">.*?</a>', flags=re.U | re.DOTALL)
        links = regPostTitle.findall(html)
        #print(links)



        regBeforeLink = re.compile('<.*?href="', flags=re.U | re.DOTALL)
        regAfterLink = re.compile('/".*?/a>', flags=re.U | re.DOTALL)
        regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
        for t in links:
            clean_t = regBeforeLink.sub("", t)
            clean_t = regAfterLink.sub("", clean_t)
            clean_t = regSpace.sub("", clean_t)
            new_links.append(clean_t)
        checked_links.append(new_links[0])
        #print(checked_links)
        new_links.remove(new_links[0])
        i += 1
    else:
        new_links.remove(new_links[0])
        i += 1
