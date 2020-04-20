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


class NeteaseMusicDownload(object):

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers = self.headers
        self.ep = Encrypyed()
        self.song_id_list = []
        self.song_id = None
        self.song_name = None
        self.album_name = None
        self.artist_name = ''
        self.song_list = None
        self.n = 0
        self.cover_url = None
        self.song_file_name = None
        self.search_name = None

    def search_song(self, search_content, page, search_type=1, limit=30):
        """
        根据音乐名搜索
      :params search_content: 音乐名
      :params search_type: 不知
      :params limit: 返回结果数量
      return: 可以得到id 再进去歌曲具体的url
        """
        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        text = {'s': search_content, 'type': search_type, 'offset': page * 30, 'sub': 'false', 'limit': limit}
        data = self.ep.search(text)
        resp = self.session.post(url, data=data)
        result = resp.json()
        if result['result']['songCount'] <= 0:
            print('搜不到！！')
        else:
            self.song_list = result['result']['songs']
            for i in self.song_list:
                self.n += 1
                temp = ''
                self.song_id_list.append(i['id'])
                for j in i['ar']:
                    temp += j['name'] + '/'
                second = int(i['dt'] / 1000 % 60)
                if second < 10:
                    second = '0' + str(second)
                print(f'{self.n}. {i["name"]}\t{temp[:-1]}\t{i["al"]["name"]}\t{int(i["dt"]/1000//60)}:{second}')

    def download_music(self):
        song_url = f'http://music.163.com/song/media/outer/url?id={self.song_id}.mp3'
        self.song_file_name = self.song_name + ' - ' + self.artist_name[:-1] + '.mp3'
        urlretrieve(song_url, self.song_file_name)

    def get_lyric(self):
        url = 'http://music.163.com/api/song/media?id=461518855'
        resp = self.session.get(url)
        result = resp.json()['lyric']
        lyric_file_name = self.song_name + ' - ' + self.artist_name[:-1] + '.txt'
        with open(lyric_file_name, 'w') as f:
            f.write(result)

    def cover_download(self):
        res = requests.get(url=self.cover_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    def song_info_insert(self):
        with open('cover.jpg', 'rb') as f:
            pic_data = f.read()
        info = {
            'picData': pic_data,
            'title': self.song_name,
            'artist': self.artist_name,
            'album': self.album_name
        }
        song_file = id3.ID3(self.song_file_name)
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
        os.remove('cover.jpg')

    def run(self):
        page = 0
        while True:
            op = input()
            if op == 'down':
                page += 1
                self.search_song(self.search_name, page)
            elif op.isdigit():
                self.song_id = self.song_id_list[int(op) - 1]
                self.song_name = self.song_list[int(op) - 1]['name']
                for i in self.song_list[int(op) - 1]['ar']:
                    self.artist_name += i['name'] + '、'
                self.album_name = self.song_list[int(op) - 1]['al']['name']
                self.cover_url = self.song_list[int(op) - 1]['al']['picUrl']
                self.download_music()
                self.cover_download()
                self.song_info_insert()
                self.get_lyric()
            elif op == 'search':
                self.n = 0
                self.search_name = input('输入音乐名：')
                self.search_song(self.search_name, page)
            elif op == 'quit':
                break
            else:
                print('输入错误')


class Encrypyed():

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


class QqMusicDownload(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Referer': 'https: // y.qq.com / portal / player.html'
        }
        self.song_list = None
        self.song_name = None
        self.album_name = None
        self.artist_name = ''
        self.songmid_list = []
        self.search_name = None
        self.songmid = None
        self.n = None
        self.lyric = None
        self.trans = None
        self.pmid = None
        self.filepath = None

    def search_music(self, page, limit=30):
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        params = {
            'new_json': 1,
            'aggr': 1,
            'cr': 1,
            'flag_qc': 0,
            'p': page,
            'n': limit,
            'w': self.search_name
        }
        search_result = requests.get(url=url, params=params, headers=self.headers).content[9:-1]
        self.song_list = json.loads(search_result)['data']['song']['list']
        for i in self.song_list:
            temp = ''
            self.n += 1
            self.songmid_list.append(i['mid'])
            for j in i['singer']:
                temp += j['name'] + '/'
            second = int(i["interval"] % 60)
            if second < 10:
                second = '0' + str(second)
            print(f'{self.n}. {i["name"]}\t{temp[:-1]}\t{i["album"]["name"]}\t{int(i["interval"]//60)}:{second}')

    def download_music(self):
        music_type = [['C400', '.m4a'], ['M500', '.mp3'], ['M800', '.mp3'], ['A000', '.ape'], ['F000', '.flac']]
        filename = music_type[1][0] + self.songmid + music_type[1][1]
        guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
        d = {
            'format': 'json',
            'cid': 205361747,
            'uin': 0,
            'songmid': self.songmid,
            'filename': filename,
            'guid': guid,
        }
        r = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg', params=d, verify=False)
        vkey = json.loads(r.content)['data']['items'][0]['vkey']
        print(f'vkey:{vkey}')
        download_url = f'http://dl.stream.qqmusic.qq.com/{filename}?vkey={vkey}&guid={guid}&uin=0&fromtag=66'
        self.filepath = self.song_name + ' - ' + self.artist_name[:-1] + music_type[1][1]
        urlretrieve(download_url, self.filepath)

    def get_lyric(self):
        lrc_url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?g_tk=753738303&songmid=' + self.songmid
        headers = {
            'Referer': 'https://y.qq.com/portal/player.html',
            'Cookie': 'skey=@LVJPZmJUX; p',
        }
        resp = requests.get(lrc_url, headers=headers)
        lrc_dict = json.loads(resp.text[18:-1])
        if lrc_dict.get('lyric'):
            self.lyric = base64.b64decode(lrc_dict['lyric']).decode()
        if lrc_dict.get('trans'):
            self.trans = base64.b64decode(lrc_dict['trans']).decode()
        filepath = self.song_name + ' - ' + self.artist_name[:-1] + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.lyric)

    def cover_download(self):
        url = f'https://y.gtimg.cn/music/photo_new/T002R300x300M000{self.pmid}.jpg?'
        params = {
            'max_age': '2592000'
        }
        res = requests.get(url=url, params=params).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    def song_info_insert(self):
        with open('cover.jpg', 'rb') as f:
            pic_data = f.read()
        info = {
            'picData': pic_data,
            'title': self.song_name,
            'artist': self.artist_name,
            'album': self.album_name
        }
        song_file = id3.ID3(self.filepath)
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
        os.remove('cover.jpg')

    def run(self):
        page = 1
        while True:
            op = input()
            if op == 'down':
                page += 1
                self.search_music(page)
            elif op.isdigit():
                self.songmid = self.songmid_list[int(op) - 1]
                self.song_name = self.song_list[int(op) - 1]['name']
                for i in self.song_list[int(op) - 1]['singer']:
                    self.artist_name += i['name'] + '、'
                self.album_name = self.song_list[int(op) - 1]['album']['name']
                self.pmid = self.song_list[int(op) - 1]['album']['pmid']
                self.download_music()
                self.cover_download()
                self.song_info_insert()
                self.get_lyric()
            elif op == 'search':
                self.n = 0
                self.search_name = input('输入音乐名：')
                self.search_music(page)
            elif op == 'quit':
                break
            else:
                print('输入错误')


class KugoMusicDownload(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.song_list = None
        self.song_name = None
        self.album_name = None
        self.artist_name = ''
        self.song_hash_list = []
        self.search_name = None
        self.song_hash = None
        self.n = None
        self.filepath = None

    def search_music(self, page):
        params = {
            'keyword': self.search_name,
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
        res = requests.get('https://songsearch.kugou.com/song_search_v2', params=params, headers=self.headers).content
        self.song_list = json.loads(res)['data']['lists']
        # print(self.song_list)
        for i in self.song_list:
            self.n += 1
            self.song_hash_list.append(i['FileHash'])
            second = int(i["Duration"] % 60)
            if second < 10:
                second = '0' + str(second)
            print(f'{self.n}. {i["SongName"]}\t{i["SingerName"]}\t{i["AlbumName"]}\t{int(i["Duration"]//60)}:{second}')

    def download_music(self):
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
        # print(download_url)
        self.filepath = self.song_name + ' - ' + self.artist_name + '.mp3'
        urlretrieve(download_url, self.filepath)
        cover_url = res['data']['img']
        urlretrieve(cover_url, 'cover.jpg')
        filepath = self.song_name + ' - ' + self.artist_name + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(res['data']['lyrics'])

    def song_info_insert(self):
        with open('cover.jpg', 'rb') as f:
            pic_data = f.read()
        info = {
            'picData': pic_data,
            'title': self.song_name,
            'artist': self.artist_name,
            'album': self.album_name
        }
        song_file = id3.ID3(self.filepath)
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
        os.remove('cover.jpg')

    def run(self):
        page = 1
        while True:
            op = input()
            if op == 'down':
                page += 1
                self.search_music(page)
            elif op.isdigit():
                self.song_hash = self.song_hash_list[int(op) - 1]
                self.song_name = self.song_list[int(op) - 1]['SongName']
                self.artist_name = self.song_list[int(op) - 1]['SingerName']
                self.album_name = self.song_list[int(op) - 1]['AlbumName']
                self.download_music()
                self.song_info_insert()
            elif op == 'search':
                self.n = 0
                self.search_name = input('输入音乐名：')
                self.search_music(page)
            elif op == 'quit':
                break
            else:
                print('输入错误')


class KuwoMusic(object):

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'referer': 'http://www.kuwo.cn/search/list?key=whatever',
            'csrf': 'RUJ53PGJ4ZD',
            'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1577029678,1577034191,1577034210,1577076651; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1577080777; kw_token=RUJ53PGJ4ZD',
        }
        self.song_id_list = []
        self.song_id = None
        self.song_name = None
        self.album_name = None
        self.artist_name = None
        self.song_list = None
        self.n = 0
        self.cover_url = None
        self.song_file_name = None
        self.search_name = None

    def search_song(self, page):
        url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
        params = {
            'key': self.search_name,
            'pn': page,
            'rn': 30,
            'reqId': '6a22ad90-6381-11ea-ad74-db939e27359f'
        }
        res = requests.get(url=url, params=params, headers=self.headers).json()
        self.song_list = res['data']['list']
        for i in self.song_list:
            self.n += 1
            self.song_id_list.append(i['rid'])
            second = int(i['duration'] % 60)
            if second < 10:
                second = '0' + str(second)
            print(f'{self.n}. {i["name"]}\t{i["artist"]}\t{i["album"]}\t{int(i["duration"] // 60)}:{second}')

    def download_music(self):
        url = " http://www.kuwo.cn/url?"
        params = {
            'format': 'mp3',
            'rid': self.song_id,
            'response': 'url',
            'type': 'convert_url3',
            'br': 128
        }
        download_url = requests.get(url=url, params=params).json()['url']
        print(download_url)
        self.song_file_name = self.song_name + ' - ' + self.artist_name + '.mp3'
        music = requests.get(url=download_url).content
        with open(self.song_file_name, 'wb') as f:
            f.write(music)

    def cover_download(self):
        res = requests.get(url=self.cover_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    def get_lyric(self):
        url = 'http://m.kuwo.cn/newh5/singles/songinfoandlrc?'
        params = {
            'musicId': self.song_id,
            'reqId': 'bf14da00-816b-11ea-ab79-5733d1734573'
        }
        res = requests.get(url=url, params=params, headers=self.headers).json()['data']['lrclist']
        # print(res)
        filepath = self.song_name + ' - ' + self.artist_name + '.txt'
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

    def song_info_insert(self):
        with open('cover.jpg', 'rb') as f:
            pic_data = f.read()
        info = {
            'picData': pic_data,
            'title': self.song_name,
            'artist': self.artist_name,
            'album': self.album_name
        }
        song_file = id3.ID3(self.song_file_name)
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
        os.remove('cover.jpg')

    def run(self):
        page = 0
        while True:
            op = input()
            if op == 'down':
                page += 1
                self.search_song(page)
            elif op.isdigit():
                self.song_id = self.song_id_list[int(op) - 1]
                self.song_name = self.song_list[int(op) - 1]['name']
                self.artist_name = self.song_list[int(op) - 1]['artist']
                self.album_name = self.song_list[int(op) - 1]['album']
                self.cover_url = self.song_list[int(op) - 1]['albumpic']
                self.download_music()
                self.cover_download()
                self.song_info_insert()
                self.get_lyric()
            elif op == 'search':
                self.n = 0
                self.search_name = input('输入音乐名：')
                self.search_song(page)
            elif op == 'quit':
                break
            else:
                print('输入错误')


class MiguMusic(object):

    def __init__(self):
        self.headers = {
            'Referer': 'https://m.music.migu.cn/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36'
        }
        self.song_list = None
        self.song_name = None
        self.album_name = None
        self.artist_name = ''
        self.search_name = None
        self.n = None

    def search_music(self, page):
        url = 'http://pd.musicapp.migu.cn/MIGUM3.0/v1.0/content/search_all.do'
        params = {
            'ua': 'Android_migu',
            'version': '5.0.1',
            'text': self.search_name,
            'pageNo': page,
            'pageSize': 30,
            'searchSwitch': '{"song":1,"album":0,"singer":0,"tagSong":0,"mvSong":0,"songlist":0,"bestShow":1}',
        }
        self.song_list = requests.get(url, params=params, headers=self.headers).json()['songResultData']['result']
        # print(self.song_list)
        for i in self.song_list:
            temp = ''
            self.n += 1
            for j in i['singers']:
                temp += j['name'] + '/'
            try:
                print(f'{self.n}. {i["name"]}\t{temp[:-1]}\t{i["albums"][0]["name"]}')
            except KeyError:
                print(f'{self.n}. {i["name"]}\t{temp[:-1]}')

    def download_music(self, download_url, name):
        res = requests.get(url=download_url, headers=self.headers, stream=True).content
        # print(res)
        filepath = name + '.mp3'
        # print(filepath)
        with open(filepath, 'wb') as f:
            f.write(res)

    @staticmethod
    def cover_download(img_url):
        res = requests.get(url=img_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    @staticmethod
    def get_lyric(lyric_url, name):
        res = requests.get(url=lyric_url).text
        filepath = name + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(res)

    def song_info_insert(self, name):
        with open('cover.jpg', 'rb') as f:
            pic_data = f.read()
        info = {
            'picData': pic_data,
            'title': self.song_name,
            'artist': self.artist_name,
            'album': self.album_name
        }
        filepath = name + '.mp3'
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
        os.remove('cover.jpg')

    def run(self):
        page = 1
        while True:
            op = input()
            if op == 'down':
                page += 1
                self.search_music(page)
            elif op.isdigit():
                self.song_name = self.song_list[int(op) - 1]['name']
                for i in self.song_list[int(op) - 1]['singers']:
                    self.artist_name += i['name'] + '、'
                try:
                    self.album_name = self.song_list[int(op) - 1]["albums"][0]["name"]
                except KeyError:
                    self.album_name = 'Unknown'
                img_url = self.song_list[int(op) - 1]['imgItems'][1]['img']
                download_url = f"https://app.pd.nf.migu.cn/MIGUM3.0/v1.0/content/sub/listenSong.do?channel=mx&copyrightId={self.song_list[int(op) - 1]['copyrightId']}&contentId={self.song_list[int(op) - 1]['contentId']}&toneFlag=HQ&resourceType={self.song_list[int(op) - 1]['resourceType']}&userId=15548614588710179085069&netType=00"
                # print(download_url)
                lyric_url = self.song_list[int(op) - 1]['lyricUrl']
                file_name = self.song_name + ' - ' + self.artist_name[:-1]
                self.download_music(download_url, file_name)
                self.cover_download(img_url)
                self.song_info_insert(file_name)
                self.get_lyric(lyric_url, file_name)
            elif op == 'search':
                self.n = 0
                self.search_name = input('输入音乐名：')
                self.search_music(page)
            elif op == 'quit':
                break
            else:
                print('输入错误')


class XiamiMusic(object):

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
        self.song_list = None
        self.song_name = None
        self.album_name = None
        self.artist_name = None
        self.search_name = None
        self.n = None

    def search_music(self, page):
        url = 'http://api.xiami.com/web'
        params = {
            'v': '2.0',
            'app_key': '1',
            'key': self.search_name,
            'page': page,
            'limit': 30,
            'r': 'search/songs'
        }
        self.song_list = requests.get(url=url, params=params, headers=self.headers).json()['data']['songs']
        print(self.song_list[19])
        for i in self.song_list:
            self.n += 1
            print(f'{self.n}. {i["song_name"]}\t{i["artist_name"]}\t{i["album_name"]}')

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

    def song_info_insert(self, name):
        with open('cover.jpg', 'rb') as f:
            pic_data = f.read()
        info = {
            'picData': pic_data,
            'title': self.song_name,
            'artist': self.artist_name,
            'album': self.album_name
        }
        filepath = name + '.mp3'
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
        os.remove('cover.jpg')

    def run(self):
        page = 1
        while True:
            op = input()
            if op == 'down':
                page += 1
                self.search_music(page)
            elif op.isdigit():
                self.song_name = self.song_list[int(op) - 1]['song_name']
                self.artist_name = self.song_list[int(op) - 1]['artist_name']
                self.album_name = self.song_list[int(op) - 1]["album_name"]
                img_url = self.song_list[int(op) - 1]['album_logo']
                download_url = self.song_list[int(op) - 1]["listen_file"]
                # print(download_url)
                lyric_url = self.song_list[int(op) - 1]['lyric']
                file_name = self.song_name + ' - ' + self.artist_name
                self.download_music(download_url, file_name)
                self.cover_download(img_url)
                self.song_info_insert(file_name)
                self.get_lyric(lyric_url, file_name)
            elif op == 'search':
                self.n = 0
                self.search_name = input('输入音乐名：')
                self.search_music(page)
            elif op == 'quit':
                break
            else:
                print('输入错误')
