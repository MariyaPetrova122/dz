import urllib.request
import re
req = urllib.request.Request('https://yandex.ru/pogoda/moscow/')
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
regSunset = re.compile('<div class="current-weather__info-row"><span class="current-weather__info-label">Восход: </span>.*?<span class="current-weather__info-label current-weather__info-label_type_sunset">Закат: </span>.*?</div>', flags= re.DOTALL)
sunset = regSunset.findall(html)
print(sunset)
new_titles = []
regTag = re.compile('<.*?>', flags=re.DOTALL)
regSpace = re.compile('\s{2,}', flags=re.DOTALL)
for t in sunset:
    clean_t = regSpace.sub("", t)
    clean_t = regTag.sub(" ", clean_t)
    new_titles.append(clean_t)
print(new_titles)
'''for t in sunset:
    clean_t = regSpace.sub("", t)
    clean_t = regTag.sub("", clean_t)
    new_titles.append(clean_t)'''
for t in new_titles:
    print(t)
