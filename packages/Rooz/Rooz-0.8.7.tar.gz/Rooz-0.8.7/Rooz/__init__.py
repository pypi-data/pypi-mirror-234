import os
try:
    os.system('pip install requests')
    os.system('pip install yt-dlp')
    os.system('pip install user-agent')
    os.system('pip install json')
    os.system('pip install re')

except:
    import requests , yt_dlp
    from user_agent import generate_user_agent
    import json , re , os
    from yt_dlp import *
    from os import system

class Download:
    def __init__(self, link):
        self.link = link
       

    def DownThreads(self):
        url = f"https://api.threadsphotodownloader.com/v2/media?url={self.link}"
        head = {'User-Agent':generate_user_agent()}
        dat={"url":f'{self.link}'}
        re=requests.get(url, headers=head, data=dat).json()
        return re


    def hi(self):
        return 'hi'
    
    def DownTikTok(self):

        h = {"referer":"https://lovetik.com/sa/video/",
             "origin":"https://lovetik.com",
            "user-agent":generate_user_agent()}
        d = {"query":self.link}
        url =requests.post("https://lovetik.com/api/ajax/search",h,d).json()
        vlink = url['links'][0]['a']



        Url = 'https://www.veed.io/video-downloader-ap/api/download-content'

        data = {"url":self.link }

        req = requests.post(Url , data ).json()

        daa = json.loads(json.dumps(req))
        
        title = daa["title"]
        username = daa["username"]
        author_url = f'https://tiktok/@{username}'

        dmj = {
            'Video_Url': f'{vlink}',
            'Title': f'{title}',
            'Author_Url': f'{author_url}'}

        return dmj
        #print(dmj)
    def DownSoundCloud(self):
        url = 'https://www.klickaud.co/download.php'
        data = {'value': self.link,
        'afae4540b697beca72538dccafd46ea2ce84bec29b359a83751f62fc662d908a':'2106439ef3318091a603bfb1623e0774a6db38ca6579dae63bcbb57253d2199e'}
        req = requests.post(url , data).text
        linnk = re.findall(r'href="(https://cf-media.sndcdn.com/[^"]+)', req)[0]
        photo = re.findall(r'<img src="(https://i1.sndcdn.com[^"]+)', req)[0]
        dmmj  =  {
        'Audio_link':linnk,
        'Thumbnail_link':photo}
        return dmmj

    def DownPinterest(self):
        li = self.link
        rep = li.replace('https://pin.it/', '')


        url = 'https://pintodown.com/wp-admin/admin-ajax.php'

        data = {'action': 'pinterest_action',
        'pinterest': f'is_private_video=&pinterest_video_url=https%3A%2F%2Fpin.it%2F{rep}'}

        req = requests.post(url , data).json()

        Op = req['data']
        return Op

    def DownFaceBook(self):
        url = 'https://www.getfvid.com/downloader'

        data = {'url': self.link}

        req = requests.post(url , data).text

        linkv = re.findall(r'<a href="([^"]+)', req)[4]
        dmj={'Video_Url':linkv}
        return dmj

    def DownFromVodu(self):
        url = self.link

        id = url.replace('https://movie.vodu.me/index.php?do=view&type=post&id=','')

        #print(id)
        data = {'do':'view',
        'type':'post',
        'id':id}

        req = requests.get(url , data).text

        title = re.findall(r'data-title="([^"]+)', req)

        vidl=re.findall(r'data-url="([^"]+)', req)

        p = re.findall(r'<img src="([^"]+)' , req)[1]
        pt = f'https://movie.vodu.me/{p}'
        #print(pt)

        for i in range(len(vidl)):
            dmj = {'title':title[i],
            'video_link':vidl[i],
            'poster':pt}
            return dmj
        return '\n\n' 
    
    def DownYouTube(self):
        url = f'https://yt.hidd004.repl.co/?link={self.link}'

        req=requests.get(url).text
        return req
    

class Search:
    def __init__(self, word):
        self.word = word
        

    def SeVodu(self):

        url = f'https://movie.vodu.me/index.php?do=list&title={self.word}'

        data = {'do': 'list','title': self.word}

        req = requests.get(url , data).text
        vidlink = re.findall(r'<div class="mytitle"> <a href="([^"]+)' , req)
        for i in range(len(vidlink)):
            n= re.findall(r'<div class="mytitle"> <a href="([^"]+)"([^""]+) ' , req)[i][1]
            nn = n.replace('>','')
            b = nn.split('<')[0]
            vl = re.findall(r'<div class="mytitle"> <a href="([^"]+)' , req)[i]
            vll = f'https://movie.vodu.me/{vl}'
            dmj = {'Name':b,
            'Link':vll}
            return dmj
        
    def SeAkoam(self):
        url = f'https://akwam.us/search?q={self.word}'

        req = requests.get(url).text

        fname = re.findall(r'class="text-white">([^>]+)' , req)
        #s = fname.split('</a')[0]

        #flink = 
        for i in range(len(fname)):
            fame = re.findall(r'class="text-white">([^>]+)' , req)[i]
            ss = fame.split('</a')[0]
            return ss
        


    
