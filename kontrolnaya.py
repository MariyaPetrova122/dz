import urllib.request
import re


def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('ISO-8859-1')
    except:
        print('Error at', pageUrl)
        return
        
commonUrl = 'file:///C:/Python33/thai_pages/'
for i in range(187, 205):
    almostUrl = commonUrl + str(i) + '.'
    for i in range(1,58):
        pageUrl = almostUrl + str(i)+'.html'  
        download_page(pageUrl)

req = urllib.request.Request('file:///C:/Python33/thai_pages/187.31.html')
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')

regWords = re.compile("<tr><td class=th><a href='.*?'>.*?</a>.*?</tr>", flags=re.U | re.DOTALL)
Words = regWords.findall(html)

regBeforeWord = re.compile("<tr><td class='th'.*?>", flags=re.U | re.DOTALL)
regMiddle = re.compile("</a>.*?<td class=", flags=re.U | re.DOTALL)
regBeforeThaiWord = re.compile("<tr><td class=th><a href.*?'>", flags = re.U|re.DOTALL)
regCleanMoreMiddle = re.compile("pos>.*?</td><td>", flags = re.U|re.DOTALL)
regCleanEnd = re.compile("</td></tr>",flags = re.U|re.DOTALL)
regQuotes = re.compile("&#34;",flags = re.U|re.DOTALL)



clean_Words = regBeforeWord.sub("", str(Words))
cleaner_Words = regMiddle.sub("", clean_Words)
evenCleanerWords = regBeforeThaiWord.sub("",cleaner_Words)
cleaner_middle = regCleanMoreMiddle.sub(":",evenCleanerWords)
so_clean = regCleanEnd.sub("",cleaner_middle)
best_clean = regQuotes.sub("",so_clean) # чистый текст, тип - строка

ThaiEngList = best_clean.split('.",')

ThaiEngDict = {}

for i in ThaiEngList:
    pair = i
    pair_parts = pair.split(":")
    a = pair_parts[0]
    b = pair_parts[1]
    ThaiEngDict[a] = b
    
print(ThaiEngDict)

