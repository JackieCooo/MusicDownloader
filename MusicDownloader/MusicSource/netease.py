import requests
import json
import os
import base64
from binascii import hexlify
from Crypto.Cipher import AES
from urllib.request import urlretrieve
from InfoInsert import SongInfoInsert


class NeteaseMusic(object):  # 网易云音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.ep = NeteaseEncrypyed()
        self.song_list = None

    def search_music(self, search_name, page, n):
        search_result = []
        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        text = {'s': search_name, 'type': 1, 'offset': page * 30, 'sub': 'false', 'limit': 30}
        data = self.ep.search(text)
        res = requests.post(url, data=data).json()['result']['songs']
        self.song_list = res
        for i in res:
            n += 1
            temp = ''
            for j in i['ar']:
                temp += j['name'] + '/'
            second = int(i['dt'] / 1000 % 60)
            if second < 10:
                second = '0' + str(second)
            # print(f'{n}. {i["name"]}\t{temp[:-1]}\t{i["al"]["name"]}\t{int(i["dt"]/1000//60)}:{second}')
            info = [i["name"], temp[:-1], i["al"]["name"]]
            search_result.append(info)
            # print(search_result)
        return n, search_result

    @staticmethod
    def download_music(song_id, filepath):
        song_url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'
        filepath += '.mp3'
        urlretrieve(song_url, filepath)

    @staticmethod
    def get_lyric(filepath, lyric_format):
        url = 'http://music.163.com/api/song/media?id=461518855'
        res = requests.get(url).json()['lyric']
        # filepath = filename + '.txt'
        if lyric_format == 0:
            filepath += '.lrc'
        else:
            filepath += '.txt'
        with open(filepath, 'w') as f:
            f.write(res)

    @staticmethod
    def cover_download(cover_url):
        res = requests.get(url=cover_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    def get_song_info(self, op, filename_type, lyric_format, directory):
        artist_name = ''
        song_name = self.song_list[int(op) - 1]['name']
        for i in self.song_list[int(op) - 1]['ar']:
            artist_name += i['name'] + '、'
        album_name = self.song_list[int(op) - 1]["al"]["name"]
        song_id = self.song_list[int(op) - 1]['id']
        img_url = self.song_list[int(op) - 1]['al']['picUrl']
        if filename_type == 0:
            filename = song_name + ' - ' + artist_name[:-1]
        elif filename_type == 1:
            filename = artist_name[:-1] + ' - ' + song_name
        else:
            filename = song_name
        filepath = directory + filename
        self.download_music(song_id, filepath)
        self.cover_download(img_url)
        info = SongInfoInsert()
        info.song_info_insert(filepath, song_name, artist_name[:-1], album_name)
        self.get_lyric(filepath, lyric_format)


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
