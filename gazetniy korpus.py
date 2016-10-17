import urllib.request
import re
import os

def author_name(html):
    regAuthorFile = re.compile('<div class="autor_name">.*?<a.*?</a>', flags=re.U | re.DOTALL)
    author = regAuthorFile.findall(html)
    regCleanFront = re.compile('<div.*?href=".*?">', flags=re.U | re.DOTALL)
    regClearBack = re.compile('</a>', flags=re.U | re.DOTALL)
    for t in author:
        clean_author = regCleanFront.sub("", t)
        clean_author = regClearBack.sub("", clean_author)
        return(clean_author)

def article_name(html):
    regArticleName = re.compile('<h1.*?</h1>', flags=re.U | re.DOTALL)
    name_of_article = regArticleName.findall(html)
    regCleanName = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for t in name_of_article:
       clean_name = regCleanName.sub("", t)
       clean_name = regSpace.sub("", clean_name)
       return(clean_name)

def date(html):
    regDateInFile = re.compile('<span class="date".*?</span>', flags=re.U | re.DOTALL)
    date_article = regDateInFile.findall(html)
    regCleanDate = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for t in date_article:
        clean_date = regCleanDate.sub("", t)
        clean_date = regSpace.sub("", clean_date)
        return(clean_date)

def topic(html):
    regTopicInFile = re.compile('<a class="rubric" href=.*?</a>', flags=re.U | re.DOTALL)
    topic_article = regTopicInFile.findall(html)
    regCleanTopic = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regClearTopicEnding = re.compile('</a>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for t in topic_article:
        clean_topic = regCleanTopic.sub("", t)
        clean_topic = regClearTopicEnding.sub("", clean_topic)
        clean_topic = regSpace.sub("", clean_topic)
        return(clean_topic)

def article_links(html):
    regArticleLink = re.compile('<div class="news_name"><a href="/news/.*?/">.*?</a></div>',flags=re.U | re.DOTALL)
    links_of_articles = regArticleLink.findall(html)
    f_li=[]
    regCleanFinLinksFront = re.compile('<div.*?href="',flags=re.U | re.DOTALL)
    regCleanFinLinksBack = re.compile('/">.*?</div>',flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for a in links_of_articles:
        clean_finally_links = regCleanFinLinksFront.sub("",a)
        clean_finally_links = regCleanFinLinksBack.sub("/",clean_finally_links)
        clean_finally_links= regSpace.sub("",clean_finally_links)
        f_li.append(clean_finally_links)
    return(f_li)


main_url = 'http://marpravda.ru/'
req = urllib.request.Request(main_url)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
regLinks = re.compile('<a href="/news/.*?/" >.*?</a>', flags=re.U | re.DOTALL)
links = regLinks.findall(html)

useful_links=[]
regImportantLink=re.compile('\t.*?<ul class="root-item">.*?\t\t',flags=re.U | re.DOTALL)
regBeforeLink = re.compile('<.*?href="', flags=re.U | re.DOTALL)
regMiddleLink= re.compile('" class="root-item">.*?/', flags=re.U | re.DOTALL)
regAfterLink = re.compile('/" >.*?a>', flags=re.U | re.DOTALL)
regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
for t in links:
    clean_links=regImportantLink.sub("",t)
    clean_links = regBeforeLink.sub("", clean_links)
    clean_links=regMiddleLink.sub("\n"+'/',clean_links)
    clean_links = regAfterLink.sub("/", clean_links)
    clean_links = regSpace.sub("", clean_links)
    useful_links.append(clean_links)

useful_links= useful_links[:-2]
useful_links[0]='/news/business'

print(useful_links)
i=0

abs_fin_links=[]
while i<len(useful_links):
    try:
        url = main_url+useful_links[i]
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        article_links(html)
        super_list=article_links(html)
        abs_fin_links.extend(super_list)
    except:
        pass
    i+=1


for i in range (0,len(abs_fin_links)):
    try:
        url=main_url+abs_fin_links[i]
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        author_name(html)
        clean_author =author_name(html)
        article_name(html)
        clean_name=article_name(html)
        date(html)
        clean_date=date(html)
        topic(html)
        clean_topic=topic(html)
        regTextInFile = re.compile('<article>.*?</article>', flags=re.U | re.DOTALL)
        text_article = regTextInFile.findall(html)
        i+=1
        file_top = '@au'+' '+str(clean_author)+'\n'+'@ti'+' '+str(clean_name)+'\n'+'@da'+' '+str(clean_date)+'\n'+'@topic'+' '+str(clean_topic)+'\n'+'@url'+' '+url+'\n'
        year=str(clean_date)[-4:]
        month=str(clean_date)[-7:-5]
        path='газета'+os.sep+'main'+os.sep+year+os.sep+month
        if not os.path.exists(path):
            os.makedirs(path)
        name = 'Статья' + str[i]+'.txt'
        f=open(газета/main/year/month/name,'w', encoding='UTF-8')
        f.write(file_top)
        f.write(text_article)
        f.close()
    except:
        pass
        i+=1













