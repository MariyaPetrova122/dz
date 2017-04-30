import urllib.request
import json
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

offsets = [0,100]
posts = []
all_ids = []
for off in offsets:
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-55284725&offset=' + str(off)+'&count=100')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    post = [text['text'].translate(non_bmp_map) for text in data['response'][1:]]
    ids = [text['id'] for text in data['response'][1:]]
    posts = posts + post
    all_ids = all_ids + ids

post_info = []
i=0
while i < len(all_ids):
    post_info.append([all_ids[i],posts[i],len(posts[i].split(' '))])
    i+=1
#print(post_info)


comments = []
all_comments = []
final_com = []

for num_post in all_ids:
    offsets = [0,100]
    for off in offsets:
        req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-55284725&post_id='+str(num_post)+'&offset=' + str(off)+'&count=100')
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        #d = {all_ids[id_post]: k[i] for i in range(len(all_ids))}
        comments = [text['text'].translate(non_bmp_map) for text in data['response'][1:]]
        #ids = [text['id'] for text in data['response'][1:]]
        all_comments +=comments
    #final_com += all_comments #[all_ids[id_post], all_comments]
 
    
print(len(all_comments))
