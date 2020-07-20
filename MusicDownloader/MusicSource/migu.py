import requests
from InfoInsert import SongInfoInsert


class MiguMusic(object):  # 咪咕音乐主程序
    '''
    版本：1.0
    '''

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

    def search_music(self, search_name, page, n):
        search_result = []
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
        self.song_list = res
        for i in res:
            temp = ''
            n += 1
            for j in i['singers']:
                temp += j['name'] + '/'
            try:
                # print(f'{n}. {i["name"]}\t{temp[:-1]}\t{i["albums"][0]["name"]}')
                info = [i["name"], i[temp[:-1]], i["albums"][0]["name"]]
            except KeyError:
                # print(f'{n}. {i["name"]}\t{temp[:-1]}\tUnknown')
                info = [i["name"], i[temp[:-1]], "Unknown"]
            search_result.append(info)
        print(search_result)
        return n, search_result

    def download_music(self, download_url, filepath):
        res = requests.get(url=download_url, headers=self.headers, stream=True).content
        filepath += '.mp3'
        with open(filepath, 'wb') as f:
            f.write(res)

    @staticmethod
    def cover_download(img_url):
        res = requests.get(url=img_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    @staticmethod
    def get_lyric(lyric_url, filepath, lyric_format):
        res = requests.get(url=lyric_url).text
        # filepath = filename + '.txt'
        if lyric_format == 0:
            filepath += '.lrc'
        else:
            filepath += '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(res)

    def download(self, op, filename_type, lyric_format, directory):
        artist_name = ''
        song_name = self.song_list[int(op) - 1]['name']
        for i in self.song_list[int(op) - 1]['singers']:
            artist_name += i['name'] + '、'
        album_name = self.song_list[int(op) - 1]["albums"][0]["name"]
        img_url = self.song_list[int(op) - 1]['imgItems'][1]['img']
        download_url = f"https://app.pd.nf.migu.cn/MIGUM3.0/v1.0/content/sub/listenSong.do?channel=mx&copyrightId={self.song_list[int(op) - 1]['copyrightId']}&contentId={self.song_list[int(op) - 1]['contentId']}&toneFlag=HQ&resourceType={self.song_list[int(op) - 1]['resourceType']}&userId=15548614588710179085069&netType=00"
        lyric_url = self.song_list[int(op) - 1]['lyricUrl']
        # filename = song_name + ' - ' + artist_name[:-1]
        if filename_type == 0:
            filename = song_name + ' - ' + artist_name[:-1]
        elif filename_type == 1:
            filename = artist_name[:-1] + ' - ' + song_name
        else:
            filename = song_name
        filepath = directory + filename
        self.download_music(download_url, filepath)
        self.cover_download(img_url)
        info = SongInfoInsert()
        info.song_info_insert(filepath, song_name, artist_name, album_name)
        self.get_lyric(lyric_url, filepath, lyric_format)

    def get_song_cover(self, op, filename_type, directory):
        artist_name = ''
        song_name = self.song_list[int(op) - 1]['name']
        for i in self.song_list[int(op) - 1]['singers']:
            artist_name += i['name'] + '、'
        img_url = self.song_list[int(op) - 1]['imgItems'][1]['img']
        if filename_type == 0:
            filename = song_name + ' - ' + artist_name[:-1] + '.jpg'
        elif filename_type == 1:
            filename = artist_name[:-1] + ' - ' + song_name + '.jpg'
        else:
            filename = song_name + '.jpg'
        filepath = directory + filename
        res = requests.get(url=img_url).content
        with open(filepath, 'wb') as f:
            f.write(res)

    def get_song_lyric(self, op, filename_type, lyric_format, directory):
        artist_name = ''
        song_name = self.song_list[int(op) - 1]['name']
        for i in self.song_list[int(op) - 1]['singers']:
            artist_name += i['name'] + '、'
        lyric_url = self.song_list[int(op) - 1]['lyricUrl']
        if filename_type == 0:
            filename = song_name + ' - ' + artist_name[:-1]
        elif filename_type == 1:
            filename = artist_name[:-1] + ' - ' + song_name
        else:
            filename = song_name
        filepath = directory + filename
        self.get_lyric(lyric_url, filepath, lyric_format)
