import requests
from InfoInsert import SongInfoInsert


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
        self.song_list = None

    def search_music(self, search_name, page, n):
        search_result = []
        url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
        params = {
            'key': search_name,
            'pn': page,
            'rn': 30,
            'reqId': '6a22ad90-6381-11ea-ad74-db939e27359f'
        }
        res = requests.get(url=url, params=params, headers=self.headers).json()['data']['list']
        self.song_list = res
        for i in res:
            n += 1
            second = int(i['duration'] % 60)
            if second < 10:
                second = '0' + str(second)
            # print(f'{n}. {i["name"]}\t{i["artist"]}\t{i["album"]}\t{int(i["duration"] // 60)}:{second}')
            info = [i["name"], i["artist"], i["album"]]
            search_result.append(info)
        # print(search_result)
        return n, search_result

    @staticmethod
    def download_music(song_id, filepath):
        url = " http://www.kuwo.cn/url?"
        params = {
            'format': 'mp3',
            'rid': song_id,
            'response': 'url',
            'type': 'convert_url3',
            'br': 128
        }
        download_url = requests.get(url=url, params=params).json()['url']
        filepath += '.mp3'
        res = requests.get(url=download_url).content
        with open(filepath, 'wb') as f:
            f.write(res)

    @staticmethod
    def cover_download(img_url):
        res = requests.get(url=img_url).content
        with open('cover.jpg', 'wb') as f:
            f.write(res)

    def get_lyric(self, song_id, filepath, lyric_format):
        url = 'http://m.kuwo.cn/newh5/singles/songinfoandlrc?'
        params = {
            'musicId': song_id,
            'reqId': 'bf14da00-816b-11ea-ab79-5733d1734573'
        }
        res = requests.get(url=url, params=params, headers=self.headers).json()['data']['lrclist']
        # filepath = filename + '.txt'
        if lyric_format == 0:
            filepath += '.lrc'
        else:
            filepath += '.txt'
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

    def get_song_info(self, op, filename_type, lyric_format, directory):
        song_name = self.song_list[int(op) - 1]['name']
        artist_name = self.song_list[int(op) - 1]['artist']
        album_name = self.song_list[int(op) - 1]["album"]
        img_url = self.song_list[int(op) - 1]['albumpic']
        song_id = self.song_list[int(op) - 1]['rid']
        # filename = song_name + ' - ' + artist_name
        if filename_type == 0:
            filename = song_name + ' - ' + artist_name
        elif filename_type == 1:
            filename = artist_name + ' - ' + song_name
        else:
            filename = song_name
        filepath = directory + filename
        self.download_music(song_id, filepath)
        self.cover_download(img_url)
        info = SongInfoInsert()
        info.song_info_insert(filepath, song_name, artist_name, album_name)
        self.get_lyric(song_id, filepath, lyric_format)
