import urllib.request
import re



def author_name():
    regAuthorFile = re.compile('<div class="autor_name">.*?<a>.*?</a>', flags=re.U | re.DOTALL)
    author = regAuthorFile.findall(html)
    regCleanFront = re.compile('<div.*?href=".*?">', flags=re.U | re.DOTALL)
    regClearBack = re.compile('</a>', flags=re.U | re.DOTALL)
    for t in author:
        clean_author = regCleanFront.sub("", t)
        clean_author = regClearBack.sub("", clean_author)
        print(clean_author)



def article_name():
    regArticleName = re.compile('<h1.*?</h1>', flags=re.U | re.DOTALL)
    name_of_article = regArticleName.findall(html)
    regCleanName = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for t in name_of_article:
       clean_name = regCleanName.sub("", t)
       clean_name = regSpace.sub("", clean_name)
       print(clean_name)

def date():
    regDateInFile = re.compile('<span class="date".*?</span>', flags=re.U | re.DOTALL)
    date_article = regDateInFile.findall(html)
    regCleanDate = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for t in date_article:
        clean_date = regCleanDate.sub("", t)
    clean_date = regSpace.sub("", clean_date)
    print(clean_date)


def topic():
    regTopicInFile = re.compile('<a class="rubric" href=.*?</a>', flags=re.U | re.DOTALL)
    topic_article = regTopicInFile.findall(html)
    regCleanTopic = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regClearTopicEnding = re.compile('</a>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for t in topic_article:
        clean_topic = regCleanTopic.sub("", t)
        clean_topic = regClearTopicEnding.sub("", clean_topic)
        clean_topic = regSpace.sub("", clean_topic)
        print(clean_topic)


def export_text():
    regTextInFile = re.compile('<article>.*?</article>', flags=re.U | re.DOTALL)
    text_article = regTextInFile.findall(html)
    if (len(text_article))==0:
        i==i-1
        pass
    else:
        name="Статья"+str(i)+".txt"
        f=open(name,"x")
        file_top = '@au%\n@ti%\n@da%\n@topic%\n@url%\n'
        f.write(file_top % (clean_author, clean_name, clean_date, clean_topic,url) )
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
            author_name()
            article_name()
            date()
            topic()
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
