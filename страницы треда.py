import urllib.request

def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('ISO-8859-1')
    except:
        print('Error at', pageUrl)
        return
  
commonUrl = 'http://www.forumishqiptar.com/threads/79403-%C3%87far%C3%AB-%C3%ABsht%C3%AB-dashuria/page'
for i in range(1,77):
    pageUrl = commonUrl + str(i)
    download_page(pageUrl)
download_page('http://www.forumishqiptar.com/threads/79403-%C3%87far%C3%AB-%C3%ABsht%C3%AB-dashuria')
