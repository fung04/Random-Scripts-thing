import os
from os.path import relpath
import music_tag

print("Select a root directory")
rootdir = input()

# rootdir = r"C:\Users\Chan\Desktop\New folder (2)"

extensions = ['flac', 'wav','dsf']
exclude = set(['Single', 'Music Download', 'Ed Sheeran - Divide WAV', 'WAV', 'DSD','Oldies'])

for subdir, dirs, files in os.walk(rootdir):
    dirs[:] = [d for d in dirs if d not in exclude]
    play_list = "#EXTM3U\n"

    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')
        # Generate a playlist file path
        playlist_name_path = f"{os.path.join(subdir,os.path.basename(subdir))}.m3u8"
        
        # Generate relative path of song
        #relative_path_song = f"{relpath(subdir)}\{file}"

        if file_extension in extensions:
            #print(relative_path_song)
            music_file = music_tag.load_file(os.path.join(subdir,file))
            file_name = f"{music_file['artist']} - {music_file['tracktitle']}"

            play_list+= f"#EXTINF:{file_name}\n{file}\n"

            with open(playlist_name_path, 'w', encoding='utf_8') as f:
                f.write(play_list)
            print(os.path.basename(subdir))
        


            
