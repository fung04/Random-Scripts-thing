import json
import os
import re
import urllib.parse as parse
from urllib.request import urlopen

class LyricFetcher:
    def __init__(self):
        self.music_extension = ['mp3', 'flac', 'wav', 'ape']
        self.illegal_character = {
            "/": ", ",
            ":": "-",
            "|": ", ",
            "?": "",
            "*": "",
            "\"": "",
            "<": "(",
            ">": ")",
        }
        self.lyric_api_url = 'https://neteasecloudmusicapi.vercel.app/lyric?id='
        self.album_api_url = 'https://neteasecloudmusicapi.vercel.app/album?id='
        self.search_song_url = 'https://react-netease-cloud-music.vercel.app/search?s={}&type=1'

    def search_album(self, album_id):
        album_api_response = urlopen(self.album_api_url + str(album_id))
        album_json = json.loads(album_api_response.read())

        for song in album_json['songs']:
            index = album_json['songs'].index(song)
            song_id = song['id']
            song_name = f'{index + 1:02d}. {song["name"]}'
            self.search_lyric(song_id, song_name)

    def search_lyric(self, song_id, song_name=None):
        if song_id and song_id != '0':
            lyric_api_response = urlopen(self.lyric_api_url + str(song_id))
            lyric_json = json.loads(lyric_api_response.read())
            try:
                lyric = lyric_json['lrc']['lyric']
                tlyric = lyric_json['tlyric']['lyric']
                lyric = lyric + '\n' + tlyric
                self.export_lyric(lyric, song_name)
            except KeyError:
                print('\n\nNo lyric found\n')
        else:
            print(f'\n\nNo song id found for {song_name}, skipping this song\n\n')

    def export_lyric(self, lyric, song_name):
        for i, j in self.illegal_character.items():
            song_name = song_name.replace(i, j)
        
        for song, file_extension, file_name in self.get_song_list():
            track_no_pattern = r'(\d\d)\.'
            track_no_song_match = re.search(track_no_pattern, song_name)
            track_no_file_match = re.search(track_no_pattern, file_name)
            
            if track_no_song_match and track_no_file_match:
                track_no_song = track_no_song_match.group(1)
                track_no_file = track_no_file_match.group(1)
                
                if track_no_song == track_no_file:
                    song_name = file_name
                    break

        with open(f'{song_name}.lrc', 'wt', encoding='utf-8') as f:
            f.write(lyric)
            print(f'\nLyric has been exported to {song_name}.lrc\n')

    def get_song_list(self):
        files = os.listdir()
        for song in files:
            file_extension = os.path.splitext(song)[1].replace('.', '')
            if file_extension in self.music_extension:
                file_name = os.path.splitext(song)[0]
                yield song, file_extension, file_name

    def search_lyric_by_name(self):
        for song, file_extension, file_name in self.get_song_list():
            print(f'\nCurrent song is = {file_name}')
            if os.path.isfile(file_name + '.lrc'):
                with open(file_name + '.lrc', 'r', encoding='utf-8') as f:
                    print(f.read())
                print(f'\n\n{file_name}.lrc already exists\n\n')
                user_input = input('Do you still want to find lyrics for this song? (y/n) ')
                if user_input == 'y':
                    self.lookup_song(file_name)
                else:
                    print(f'\n{file_name} will be skipped\n')
            else:
                self.lookup_song(file_name)

    def lookup_song(self, song_name):
        song_name = parse.quote(song_name)
        cmd_command = f'powershell start """{self.search_song_url.format(song_name)}"""'
        os.system(cmd_command)
        song_name = parse.unquote(song_name)

        print('\nEnter song id = 0 to skip this song')
        song_id = input('Please input song id: ')
        self.search_lyric(song_id, song_name)

    def lyric_fetcher_menu(self):
        while True:
            user_input = input("\n\nSelect option:\n"
                               "[1] Search album by id\n"
                               "[2] Search lyric by id\n"
                               "[3] Search lyric by song name\n\n"
                               "Enter option: ")
            if user_input == '1':
                album_id = input('Enter album id: ')
                self.search_album(album_id)
            elif user_input == '2':
                song_id = input('Enter song id: ')
                self.search_lyric(song_id)
            elif user_input == '3':
                self.search_lyric_by_name()
            else:
                print('\n\nInvalid option, please try again')

if __name__ == '__main__':
    lyric_fetcher = LyricFetcher()
    lyric_fetcher.lyric_fetcher_menu()
