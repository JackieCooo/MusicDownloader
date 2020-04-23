import requests
import time
import json
import os
import random
import base64
from binascii import hexlify
from Crypto.Cipher import AES
from urllib.request import urlretrieve
from mutagen import id3


class NeteaseMusic(object):  # 网易云音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.ep = NeteaseEncrypyed()
        self.song_list = []

    def search_music(self, search_name, page, n):
        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        text = {'s': search_name, 'type': 1, 'offset': page * 30, 'sub': 'false', 'limit': 30}
        data = self.ep.search(text)
        res = requests.post(url, data=data).json()['result']['songs']
        for i in res:
            n += 1
            temp = ''
            self.song_list.append(i)
            for j in i['ar']:
                temp += j['name'] + '/'
            second = int(i['dt'] / 1000 % 60)
            if second < 10:
                second = '0' + str(second)
            print(f'{n}. {i["name"]}\t{temp[:-1]}\t{i["al"]["name"]}\t{int(i["dt"]/1000//60)}:{second}')

    @staticmethod
    def download_music(song_id, filename):
        song_url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'
        filepath = filename + '.mp3'
        urlretrieve(song_url, filepath)

    @staticmethod
    def get_lyric(filename):
        url = 'http://music.163.com/api/song/media?id=461518855'
        res = requests.get(url).json()['lyric']
        filepath = filename + '.txt'
        with open(filepath, 'w') as f:
            f.write(res)

    @staticmethod
    def cover_download(cover_url):
        res = requests.get(url=cover_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    def get_song_info(self, op):
        artist_name = ''
        song_name = self.song_list[int(op) - 1]['name']
        for i in self.song_list[int(op) - 1]['ar']:
            artist_name += i['name'] + '、'
        album_name = self.song_list[int(op) - 1]["al"]["name"]
        song_id = self.song_list[int(op) - 1]['id']
        img_url = self.song_list[int(op) - 1]['al']['picUrl']
        filename = song_name + ' - ' + artist_name[:-1]
        self.download_music(song_id, filename)
        self.cover_download(img_url)
        info = SongInfoInsert()
        info.song_info_insert(filename, song_name, artist_name, album_name)
        self.get_lyric(filename)


class NeteaseEncrypyed(object):  # 网易云音乐加密程序

    def __init__(self):
        self.pub_key = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'

    @staticmethod
    def create_secret_key(size):
        return hexlify(os.urandom(size))[:16].decode('utf-8')

    @staticmethod
    def aes_encrypt(text, key):
        iv = '0102030405060708'
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        iv = iv.encode('utf-8')
        key = key.encode('utf-8')
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        text = text.encode('utf-8')
        result = encryptor.encrypt(text)
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    @staticmethod
    def rsa_encrpt(text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(hexlify(text.encode('utf-8')), 16), int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def work(self, ids, br=128000):
        text = {'ids': [ids], 'br': br, 'csrf_token': ''}
        text = json.dumps(text)
        i = self.create_secret_key(16)
        encText = self.aes_encrypt(text, self.nonce)
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        return data

    def search(self, text):
        text = json.dumps(text)
        i = self.create_secret_key(16)
        encText = self.aes_encrypt(text, self.nonce)
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        return data


class QqMusic(object):  # QQ音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Referer': 'https: // y.qq.com / portal / player.html'
        }
        self.song_list = []
        self.lyric = None
        self.trans = None
        self.music_type = [['C400', '.m4a'], ['M500', '.mp3'], ['M800', '.mp3'], ['A000', '.ape'], ['F000', '.flac']]

    def search_music(self, search_name, page, n):
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        params = {
            'new_json': 1,
            'aggr': 1,
            'cr': 1,
            'flag_qc': 0,
            'p': page,
            'n': 30,
            'w': search_name
        }
        search_result = requests.get(url=url, params=params, headers=self.headers).content[9:-1]
        res = json.loads(search_result)['data']['song']['list']
        for i in res:
            temp = ''
            n += 1
            self.song_list.append(i)
            for j in i['singer']:
                temp += j['name'] + '/'
            second = int(i["interval"] % 60)
            if second < 10:
                second = '0' + str(second)
            print(f'{n}. {i["name"]}\t{temp[:-1]}\t{i["album"]["name"]}\t{int(i["interval"]//60)}:{second}')
        return n

    @staticmethod
    def download_music(songmid, url_param, filename):
        guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
        params = {
            'format': 'json',
            'cid': 205361747,
            'uin': 0,
            'songmid': songmid,
            'filename': url_param,
            'guid': guid,
        }
        vkey = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg', params=params).json()['data']['items'][0]['vkey']
        # print(f'vkey:{vkey}')
        url = f'http://dl.stream.qqmusic.qq.com/{url_param}?vkey={vkey}&guid={guid}&uin=0&fromtag=66'
        filepath = filename + '.mp3'
        urlretrieve(url=url, filename=filepath)

    def get_lyric(self, songmid, filename):
        lrc_url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?g_tk=753738303&songmid=' + songmid
        headers = {
            'Referer': 'https://y.qq.com/portal/player.html',
            'Cookie': 'skey=@LVJPZmJUX; p',
        }
        res = requests.get(lrc_url, headers=headers)
        lrc_dict = json.loads(res.text[18:-1])
        if lrc_dict.get('lyric'):
            self.lyric = base64.b64decode(lrc_dict['lyric']).decode()
        if lrc_dict.get('trans'):
            self.trans = base64.b64decode(lrc_dict['trans']).decode()
        filepath = filename + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.lyric)

    @staticmethod
    def cover_download(pmid):
        url = f'https://y.gtimg.cn/music/photo_new/T002R300x300M000{pmid}.jpg?'
        params = {
            'max_age': '2592000'
        }
        res = requests.get(url=url, params=params).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    def get_song_info(self, op):
        artist_name = ''
        song_name = self.song_list[int(op) - 1]['name']
        for i in self.song_list[int(op) - 1]['singer']:
            artist_name += i['name'] + '、'
        album_name = self.song_list[int(op) - 1]['album']['name']
        songmid = self.song_list[int(op) - 1]['mid']
        pmid = self.song_list[int(op) - 1]['album']['pmid']
        url_param = self.music_type[1][0] + songmid + self.music_type[1][1]
        filename = song_name + ' - ' + artist_name[:-1]
        self.download_music(songmid, url_param, filename)
        self.cover_download(pmid)
        info = SongInfoInsert()
        info.song_info_insert(filename, song_name, artist_name, album_name)
        self.get_lyric(songmid, filename)


class KugoMusic(object):  # 酷狗音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.song_list = []

    def search_music(self, search_name, page, n):
        params = {
            'keyword': search_name,
            'page': page,
            'pagesize': '30',
            'userid': '-1',
            'clientver': '',
            'platform': 'WebFilter',
            'tag': '',
            'filter': '2',
            'iscorrection': '1',
            'privilege_filter': '0',
            '_': int(time.time() * 1000)
        }
        res = requests.get('https://songsearch.kugou.com/song_search_v2', params=params, headers=self.headers).json()['data']['lists']
        for i in res:
            n += 1
            self.song_list.append(i)
            second = int(i["Duration"] % 60)
            if second < 10:
                second = '0' + str(second)
            print(f'{n}. {i["SongName"]}\t{i["SingerName"]}\t{i["AlbumName"]}\t{int(i["Duration"]//60)}:{second}')

    @staticmethod
    def download_music(filename):
        url = 'http://www.kugou.com/yy/index.php?'
        params = {
            'r': 'play/getdata',
            'hash': '85F78E1B540E147DD07F46BC10E19E09'
        }
        headers = {
            "Cookie": "kg_mid=cbaba0008ce7624cb96876169f5bae0d; kg_dfid=2lP8ls2CT9Wh0s6XuX3M0nwk; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; KuGooRandom=66331587086741307; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1587085723,1587086956,1587125795; ACK_SERVER_10015=%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1587127029"
        }
        res = requests.get(url=url, params=params, headers=headers).json()
        download_url = res['data']['play_url']
        filepath = filename + '.mp3'
        urlretrieve(download_url, filepath)
        cover_url = res['data']['img']
        urlretrieve(cover_url, 'cover.jpg')
        filepath = filename + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(res['data']['lyrics'])

    def get_song_info(self, op):
        song_name = self.song_list[int(op) - 1]['SongName']
        artist_name = self.song_list[int(op) - 1]['SingerName']
        album_name = self.song_list[int(op) - 1]['AlbumName']
        filename = song_name + ' - ' + artist_name
        self.download_music(filename)
        info = SongInfoInsert()
        info.song_info_insert(filename, song_name, artist_name, album_name)


class KuwoMusic(object):  # 酷我音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'referer': 'http://www.kuwo.cn/search/list?key=whatever',
            'csrf': 'RUJ53PGJ4ZD',
            'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1577029678,1577034191,1577034210,1577076651; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1577080777; kw_token=RUJ53PGJ4ZD',
        }
        self.song_list = []

    def search_music(self, search_name, page, n):
        url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
        params = {
            'key': search_name,
            'pn': page,
            'rn': 30,
            'reqId': '6a22ad90-6381-11ea-ad74-db939e27359f'
        }
        res = requests.get(url=url, params=params, headers=self.headers).json()['data']['list']
        for i in res:
            n += 1
            self.song_list.append(i)
            second = int(i['duration'] % 60)
            if second < 10:
                second = '0' + str(second)
            print(f'{n}. {i["name"]}\t{i["artist"]}\t{i["album"]}\t{int(i["duration"] // 60)}:{second}')

    @staticmethod
    def download_music(song_id, filename):
        url = " http://www.kuwo.cn/url?"
        params = {
            'format': 'mp3',
            'rid': song_id,
            'response': 'url',
            'type': 'convert_url3',
            'br': 128
        }
        download_url = requests.get(url=url, params=params).json()['url']
        filepath = filename + '.mp3'
        res = requests.get(url=download_url).content
        with open(filepath, 'wb') as f:
            f.write(res)

    @staticmethod
    def cover_download(img_url):
        res = requests.get(url=img_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    def get_lyric(self, song_id, filename):
        url = 'http://m.kuwo.cn/newh5/singles/songinfoandlrc?'
        params = {
            'musicId': song_id,
            'reqId': 'bf14da00-816b-11ea-ab79-5733d1734573'
        }
        res = requests.get(url=url, params=params, headers=self.headers).json()['data']['lrclist']
        filepath = filename + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            for i in res:
                minute = round(float(i['time']) // 60)
                if minute < 10:
                    minute = '0' + str(minute)
                else:
                    minute = str(minute)
                second = round(float(i['time']) % 60, 2)
                if second < 10:
                    second = '0' + str(second)
                else:
                    second = str(second)
                write_content = '[' + minute + ':' + second + ']' + i['lineLyric'] + '\n'
                f.write(write_content)

    def get_song_info(self, op):
        song_name = self.song_list[int(op) - 1]['name']
        artist_name = self.song_list[int(op) - 1]['artist']
        album_name = self.song_list[int(op) - 1]["album"]
        img_url = self.song_list[int(op) - 1]['albumpic']
        song_id = self.song_list[int(op) - 1]['rid']
        filename = song_name + ' - ' + artist_name
        self.download_music(song_id, filename)
        self.cover_download(img_url)
        info = SongInfoInsert()
        info.song_info_insert(filename, song_name, artist_name, album_name)
        self.get_lyric(song_id, filename)


class MiguMusic(object):  # 咪咕音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            'Referer': 'https://m.music.migu.cn/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36'
        }
        self.song_list = []
        self.song_name = None
        self.album_name = None
        self.artist_name = ''
        self.search_name = None
        self.n = None

    def search_music(self, search_name, page, n):
        url = 'http://pd.musicapp.migu.cn/MIGUM3.0/v1.0/content/search_all.do'
        params = {
            'ua': 'Android_migu',
            'version': '5.0.1',
            'text': search_name,
            'pageNo': page,
            'pageSize': 30,
            'searchSwitch': '{"song":1,"album":0,"singer":0,"tagSong":0,"mvSong":0,"songlist":0,"bestShow":1}',
        }
        res = requests.get(url, params=params, headers=self.headers).json()['songResultData']['result']
        for i in res:
            temp = ''
            n += 1
            for j in i['singers']:
                temp += j['name'] + '/'
            self.song_list.append(i)
            try:
                print(f'{n}. {i["name"]}\t{temp[:-1]}\t{i["albums"][0]["name"]}')
            except KeyError:
                print(f'{n}. {i["name"]}\t{temp[:-1]}\tUnknown')

    def download_music(self, download_url, filename):
        res = requests.get(url=download_url, headers=self.headers, stream=True).content
        filepath = filename + '.mp3'
        with open(filepath, 'wb') as f:
            f.write(res)

    @staticmethod
    def cover_download(img_url):
        res = requests.get(url=img_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    @staticmethod
    def get_lyric(lyric_url, filename):
        res = requests.get(url=lyric_url).text
        filepath = filename + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(res)

    def get_song_info(self, op):
        artist_name = ''
        song_name = self.song_list[int(op) - 1]['name']
        for i in self.song_list[int(op) - 1]['singers']:
            artist_name += i['name'] + '、'
        album_name = self.song_list[int(op) - 1]["albums"][0]["name"]
        img_url = self.song_list[int(op) - 1]['imgItems'][1]['img']
        download_url = f"https://app.pd.nf.migu.cn/MIGUM3.0/v1.0/content/sub/listenSong.do?channel=mx&copyrightId={self.song_list[int(op) - 1]['copyrightId']}&contentId={self.song_list[int(op) - 1]['contentId']}&toneFlag=HQ&resourceType={self.song_list[int(op) - 1]['resourceType']}&userId=15548614588710179085069&netType=00"
        lyric_url = self.song_list[int(op) - 1]['lyricUrl']
        filename = song_name + ' - ' + artist_name[:-1]
        self.download_music(download_url, filename)
        self.cover_download(img_url)
        info = SongInfoInsert()
        info.song_info_insert(filename, song_name, artist_name, album_name)
        self.get_lyric(lyric_url, filename)


class XiamiMusic(object):  # 虾米音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml; "
                      "q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "text/html",
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "http://www.xiami.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        self.song_list = []

    def search_music(self, search_name, page, n):
        url = 'http://api.xiami.com/web'
        params = {
            'v': '2.0',
            'app_key': '1',
            'key': search_name,
            'page': page,
            'limit': 30,
            'r': 'search/songs'
        }
        res = requests.get(url=url, params=params, headers=self.headers).json()['data']['songs']
        for i in res:
            n += 1
            print(f'{n}. {i["song_name"]}\t{i["artist_name"]}\t{i["album_name"]}')
            self.song_list.append(i)
        return n

    @staticmethod
    def download_music(url, file_name):
        res = requests.get(url=url, stream=True).content
        filepath = file_name + '.mp3'
        with open(filepath, 'wb') as f:
            f.write(res)

    @staticmethod
    def cover_download(url):
        res = requests.get(url=url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    @staticmethod
    def get_lyric(url, file_name):
        if file_name == '':
            return 'No lyric'
        filepath = file_name + '.txt'
        res = requests.get(url=url).text
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(res)

    def get_song_info(self, op):
        song_name = self.song_list[int(op) - 1]['song_name']
        artist_name = self.song_list[int(op) - 1]['artist_name']
        album_name = self.song_list[int(op) - 1]["album_name"]
        img_url = self.song_list[int(op) - 1]['album_logo']
        download_url = self.song_list[int(op) - 1]["listen_file"]
        lyric_url = self.song_list[int(op) - 1]['lyric']
        file_name = song_name + ' - ' + artist_name
        self.download_music(download_url, file_name)
        self.cover_download(img_url)
        info = SongInfoInsert()
        info.song_info_insert(file_name, song_name, artist_name, album_name)
        self.get_lyric(lyric_url, file_name)


class Run(object):

    def __init__(self):
        self.search_name = None
        self.sess = None
        self.n = None  # 音乐序号

    def run(self):
        page = 1
        self.engine_switch()
        while True:
            op = input()
            if op == 'down':
                page += 1
                self.sess.search_music(self.search_name, page, self.n)
            elif op.isdigit():
                self.sess.get_song_info(op)
            elif op == 'search':
                self.n = 0
                self.search_name = input('输入音乐名：')
                self.n = self.sess.search_music(self.search_name, page, self.n)
            elif op == 'quit':
                break
            elif op == 'source':
                print('1. 网易云  2. QQ音乐  3. 酷狗音乐  4. 酷我音乐  5. 虾米音乐  6. 咪咕音乐')
                source = int(input('输入搜索引擎序号'))
                self.engine_switch(source)
            else:
                print('输入错误')

    def engine_switch(self, source=1):  # 切换搜索引擎，默认为网易云音乐
        if source == 1:
            self.sess = NeteaseMusic()
        elif source == 2:
            self.sess = QqMusic()
        elif source == 3:
            self.sess = KugoMusic()
        elif source == 4:
            self.sess = KuwoMusic()
        elif source == 5:
            self.sess = XiamiMusic()
        elif source == 6:
            self.sess = MiguMusic()
        else:
            print('输入错误')


class SongInfoInsert(object):

    @staticmethod
    def song_info_insert(file_name, song_name, artist_name, album_name):
        with open('cover.jpg', 'rb') as f:
            pic_data = f.read()
        info = {
            'picData': pic_data,
            'title': song_name,
            'artist': artist_name,
            'album': album_name
        }
        filepath = file_name + '.mp3'
        try:
            song_file = id3.ID3(filepath)
            song_file['APIC'] = id3.APIC(  # 插入封面
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Cover',
                data=info['picData']
            )
            song_file['TIT2'] = id3.TIT2(  # 插入歌名
                encoding=3,
                text=info['title']
            )
            song_file['TPE1'] = id3.TPE1(  # 插入歌手
                encoding=3,
                text=info['artist']
            )
            song_file['TALB'] = id3.TALB(  # 插入专辑名
                encoding=3,
                text=info['album']
            )
            song_file.save()
        except Exception as error:
            print('无法写入歌曲信息')
            print(f'报错：{error}')
        finally:
            os.remove('cover.jpg')


if __name__ == '__main__':
    run = Run()
    run.run()
