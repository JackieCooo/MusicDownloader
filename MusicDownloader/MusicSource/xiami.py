import requests
from InfoInsert import SongInfoInsert


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
        self.song_list = None

    def search_music(self, search_name, page, n):
        search_result = []
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
        self.song_list = res
        for i in res:
            n += 1
            # print(f'{n}. {i["song_name"]} {i["artist_name"]} {i["album_name"]}')
            info = [i["song_name"], i["artist_name"], i["album_name"]]
            search_result.append(info)
        # print(search_result)
        return n, search_result

    @staticmethod
    def download_music(url, filepath):
        res = requests.get(url=url, stream=True).content
        filepath += '.mp3'
        with open(filepath, 'wb') as f:
            f.write(res)

    @staticmethod
    def cover_download(url):
        res = requests.get(url=url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    @staticmethod
    def get_lyric(url, filepath, lyric_format):
        # if file_name == '':
        #     return 'No lyric'
        # filepath = file_name + '.txt'
        if lyric_format == 0:
            filepath += '.lrc'
        else:
            filepath += '.txt'
        res = requests.get(url=url).text
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(res)

    def get_song_info(self, op, filename_type, lyric_format, directory):
        song_name = self.song_list[int(op) - 1]['song_name']
        artist_name = self.song_list[int(op) - 1]['artist_name']
        album_name = self.song_list[int(op) - 1]["album_name"]
        img_url = self.song_list[int(op) - 1]['album_logo']
        download_url = self.song_list[int(op) - 1]["listen_file"]
        lyric_url = self.song_list[int(op) - 1]['lyric']
        # file_name = song_name + ' - ' + artist_name
        if filename_type == 0:
            filename = song_name + ' - ' + artist_name
        elif filename_type == 1:
            filename = artist_name + ' - ' + song_name
        else:
            filename = song_name
        filepath = directory + filename
        self.download_music(download_url, filepath)
        self.cover_download(img_url)
        info = SongInfoInsert()
        info.song_info_insert(filepath, song_name, artist_name, album_name)
        self.get_lyric(lyric_url, filepath, lyric_format)

