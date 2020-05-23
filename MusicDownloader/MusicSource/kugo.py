import requests
import time
from urllib.request import urlretrieve
from InfoInsert import SongInfoInsert


class KugoMusic(object):  # 酷狗音乐主程序
    '''
    版本：1.0
    '''

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.song_list = None

    def search_music(self, search_name, page, n):
        search_result = []
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
        self.song_list = res
        for i in res:
            n += 1
            second = int(i["Duration"] % 60)
            if second < 10:
                second = '0' + str(second)
            # print(f'{n}. {i["SongName"]}\t{i["SingerName"]}\t{i["AlbumName"]}\t{int(i["Duration"]//60)}:{second}')
            info = [i["SongName"], i["SingerName"], i["AlbumName"]]
            search_result.append(info)
            # print(search_result)
        return n, search_result

    @staticmethod
    def download_music(filename, lyric_format):
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
        # filepath = filename + '.txt'
        if lyric_format == 0:
            filepath = filename + '.lrc'
        else:
            filepath = filename + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(res['data']['lyrics'])

    def get_song_info(self, op, filename_type, lyric_format, directory):
        song_name = self.song_list[int(op) - 1]['SongName']
        artist_name = self.song_list[int(op) - 1]['SingerName']
        album_name = self.song_list[int(op) - 1]['AlbumName']
        # filename = song_name + ' - ' + artist_name
        if filename_type == 0:
            filename = song_name + ' - ' + artist_name
        elif filename_type == 1:
            filename = artist_name + ' - ' + song_name
        else:
            filename = song_name
        filepath = directory + filename
        self.download_music(filepath, lyric_format)
        info = SongInfoInsert()
        info.song_info_insert(filepath, song_name, artist_name, album_name)
