import json
import os
import urllib.parse as parse
from urllib.request import urlopen

music_extension = ['mp3', 'flac', 'wav', 'ape']
illegal_character = {
        "/": ", ",
        ":": "-",
        "|": ", ",
        "?": "",
        "*": "",
        "\"": "",
        "<": "(",
        ">": ")",
    }


# api url provide by https://github.com/Binaryify/NeteaseCloudMusicApi
#lyric_api_url = 'https://netease-cloud-music-api-binaryify-5fte1rlkx-binaryify.vercel.app/lyric?id='
#album_api_url = 'https://netease-cloud-music-api-binaryify-5fte1rlkx-binaryify.vercel.app/album?id='

# third party api provider
lyric_api_url = 'https://autumnfish.cn/lyric?id='
album_api_url = 'https://autumnfish.cn/album?id='

search_song_url = 'https://music.163.com/#/search/m/?s='

# search album by id
def search_album(album_id):
    album_api_response = urlopen(album_api_url + str(album_id))
    album_json = json.loads(album_api_response.read())

    for song in album_json['songs']:
        # get index value of this loop
        index = album_json['songs'].index(song)

        song_id = song['id']
        # 01. song_name.lrc
        song_name = f'{index + 1:02d}. {song["name"]}'
        search_lyric(song_id, song_name)


# search lyric by id
def search_lyric(song_id, song_name=None):

    if song_id and song_id != '0':
        lyric_api_response = urlopen(lyric_api_url + str(song_id))
        lyric_json = json.loads(lyric_api_response.read())

        try:
            # get lyric
            lyric = lyric_json['lrc']['lyric']
            # get tlyric
            tlyric = lyric_json['tlyric']['lyric']
            # combine lyric and tlyric
            lyric = lyric + '\n' + tlyric

            # export lyric
            export_lyric(lyric, song_name)
        except KeyError:
            print('\n\nNo lyric found\n')
        
    else:
        print(f'\n\nNo song id found for {song_name}, will skip this song\n\n')


# export lyric to file
def export_lyric(lyric, song_name):

    for i, j in illegal_character.items():
        song_name = song_name.replace(i, j)
        
    file_name = song_name + '.lrc'
    with open(file_name, 'wt', encoding='utf-8') as f:
        f.write(lyric)
    print(f'\n\nLyric for has been exported to {file_name}\n\n')


# read song in directory
def get_song_list():
    files = os.listdir()
    for song in files:
        file_extension = os.path.splitext(song)[1].replace('.', '')
        if file_extension in music_extension:
                file_name = os.path.splitext(song)[0]
                print(f'\nCurrent song is = {file_name}')

                # check if lrc file exits
                if os.path.isfile(file_name + '.lrc'):
                    
                    # display lyric
                    with open(file_name + '.lrc', 'r', encoding='utf-8') as f:
                        print(f.read())
                    
                    print(f'\n\n{file_name}.lrc already exist\n\n')

                    # ask user if he want to continue
                    user_input = input(
                        'Do you still want to find lyric for this song? (y/n) ')
                    if user_input == 'y':
                        search_song(file_name)
                    else:
                        print(f'\n{file_name} will be skip\n')
                else:
                    search_song(file_name)


# search song by name
def search_song(song_name):
    # parse song name
    song_name = parse.quote(song_name)
    # search song by open search page
    cmd_command = f'powershell start "{search_song_url}{song_name}"'
    os.system(cmd_command)

    # revert the parse result
    song_name = parse.unquote(song_name)
    # search lyric
    print(f'\nEnter song id = 0 to skip this song')
    song_id = input('Please input song id: ')
    search_lyric(song_id, song_name)


def lyric_fetcher_menu():
    user_input = input("\n\nSelect option: \n\n"
                    "[1] Search album by id\n"
                    "[2] Search lyric by id\n"
                    "[3] Search lyric by song name\n\n"
                    "Enter option: ")
    if user_input == '1':
        album_id = input('Enter album id: ')
        search_album(album_id)
    elif user_input == '2':
        song_id = input('Enter song id: ')
        search_lyric(song_id)        
    elif user_input == '3':
        get_song_list()
    else:
        print('\n\nInvalid option, please try again')


if __name__ == '__main__':
    while True:
        lyric_fetcher_menu()
