import requests
import time
import json
import random
import base64
from urllib.request import urlretrieve
from InfoInsert import SongInfoInsert


class QqMusic(object):  # QQ音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Referer': 'https: // y.qq.com / portal / player.html'
        }
        self.song_list = None
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
        self.song_list = res
        for i in res:
            temp = ''
            n += 1
            for j in i['singer']:
                temp += j['name'] + '/'
            second = int(i["interval"] % 60)
            if second < 10:
                second = '0' + str(second)
            # print(f'{n}. {i["name"]}\t{temp[:-1]}\t{i["album"]["name"]}\t{int(i["interval"]//60)}:{second}')
            info = [i["name"], temp[:-1], i["album"]["name"]]
            search_result.append(info)
            # print(search_result)
        return n, search_result

    @staticmethod
    def download_music(songmid, url_param, filepath):
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
        filepath += '.mp3'
        urlretrieve(url=url, filename=filepath)

    def get_lyric(self, songmid, filepath, lyric_format):
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
        # filepath = filename + '.txt'
        if lyric_format == 0:
            filepath += '.lrc'
        else:
            filepath += '.txt'
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

    def get_song_info(self, op, filename_type, lyric_format, directory):
        artist_name = ''
        song_name = self.song_list[int(op) - 1]['name']
        for i in self.song_list[int(op) - 1]['singer']:
            artist_name += i['name'] + '、'
        album_name = self.song_list[int(op) - 1]['album']['name']
        songmid = self.song_list[int(op) - 1]['mid']
        pmid = self.song_list[int(op) - 1]['album']['pmid']
        url_param = self.music_type[1][0] + songmid + self.music_type[1][1]
        # filename = song_name + ' - ' + artist_name[:-1]
        if filename_type == 0:
            filename = song_name + ' - ' + artist_name[:-1]
        elif filename_type == 1:
            filename = artist_name[:-1] + ' - ' + song_name
        else:
            filename = song_name
        filepath = directory + filename
        self.download_music(songmid, url_param, filepath)
        self.cover_download(pmid)
        info = SongInfoInsert()
        info.song_info_insert(filepath, song_name, artist_name, album_name)
        self.get_lyric(songmid, filepath, lyric_format)
