from mutagen import id3
import os


class SongInfoInsert(object):

    @staticmethod
    def song_info_insert(filepath, song_name, artist_name, album_name):
        with open('cover.jpg', 'rb') as f:
            pic_data = f.read()
        info = {
            'picData': pic_data,
            'title': song_name,
            'artist': artist_name,
            'album': album_name
        }
        filepath += '.mp3'
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
