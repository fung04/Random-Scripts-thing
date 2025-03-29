import json
import os
import re

import music_tag
import pykakasi
from pypinyin import lazy_pinyin

class MusicTools:
    def __init__(self):
        
        # add music file extension to list if not exist here
        self.music_dict = {}
        self.music_extension = ['mp3', 'flac', 'ape', 'm4a', 'dsf', 'aif', 'aac']

        # regex pattern for japanese and chinese character
        self.japanese_pattern = re.compile(r'[\u3040-\u30ff]+')
        self.chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

    def chinese_to_pinyin(self):
        for file, file_extension, file_name in self.get_file_info():

            # identify chinese character in file name
            chinese_match = self.chinese_pattern.search(file_name)

            if chinese_match:
                # convert chinese to pinyin
                pinyin = ' '.join(lazy_pinyin(file_name)).title()
                pinyin = pinyin.replace("  ", " ")
                print(f"{file_name} -> {pinyin}.{file_extension}")

                # rename file
                os.rename(file, f'{pinyin}.{file_extension}')

                # rename lrc file if exist
                self.rename_lrc_file(file_name, pinyin)

                # save pinyin to dictionary as key
                self.music_dict[pinyin] = file_name
            else:
                print(f"{file_name} is unable to covert pinyin")

        # save original file name to json file
        self.save_to_json()
    
    def japanese_to_romanji(self):
        for file, file_extension, file_name in self.get_file_info():

            # identify japanese character in file name
            japanese_match = self.japanese_pattern.search(file_name)

            if not japanese_match:
                # identify chinese character in file name
                chinese_match = self.chinese_pattern.search(file_name)

                if chinese_match:
                    # There is a condition that japanese character is same as chinese character
                    # So need to prompt user to insit convert or not to convert
                    user_input = input(
                        f"\n\nDo you want to convert {file_name} insit? (y/n) ")
                    if user_input == "y":
                        chinese_match = chinese_match.group()
                else:
                    chinese_match = None

            if japanese_match or chinese_match:
                # Convert Japanese to Romanji
                kks = pykakasi.kakasi()
                convert_result_dict = kks.convert(file_name)
                romanji = ' '.join([item['hepburn'].strip()
                                    for item in convert_result_dict])
                romanji = romanji.replace("  ", " ").title()
                print(f"{file_name} -> {romanji}.{file_extension}")

                # rename file
                os.rename(file, f'{romanji}.{file_extension}')

                # save romanji to dictionary as key
                self.music_dict[romanji] = file_name

                # rename lrc file if exist
                self.rename_lrc_file(file_name, romanji)
            else:
                print(f"{file_name} is unable to convert romanji")

        # save original file name to json file
        self.save_to_json()

    def json_list_to_filename(self):
        with open("music_list.json", "r", encoding="utf8") as music_list:
            self.music_dict = json.load(music_list)

        for file, file_extension, file_name in self.get_file_info():
            try:
                os.rename(file, f'{self.music_dict[file_name]}.{file_extension}')
                self.rename_lrc_file(file_name, self.music_dict[file_name])
            except KeyError:
                print(f"{file_name} not found in music_list.json")
            except FileExistsError:
                print(f"{file_name} already exists")

    def tagname_to_filename(self):
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

        # ask user for album or single
        user_input = input("\n\nIs this album or single? (a/s) ")
        
        for file, file_extension, file_name in self.get_file_info():

            # get tag info from music file then rename file
            tag_info = music_tag.load_file(file)
            
            if user_input == "a":
                tag_name = f"{tag_info['title']}"
            elif user_input == "s":
                tag_name = f"{tag_info['artist']} - {tag_info['title']}"

            # idetify and replace Windows illegal character
            for i, j in illegal_character.items():
                tag_name = tag_name.replace(i, j)

            if tag_info['title']:
                print(f"{file_name} -> {tag_name}.{file_extension}")
                try:
                    # rename file
                    os.rename(file, f'{tag_name}.{file_extension}')
                except FileExistsError:
                    i = 0
                    i = i + 1
                    tag_name = f'{tag_name} ({i})'
                    os.rename(file, f'{tag_name}.{file_extension}')

                # rename lrc file if exist
                self.rename_lrc_file(file_name, tag_name)
            else:
                print(f"\n\nNo title for {file_name}\n\n")

    def trackno_to_filename(self):

        # get leading number from user
        print("Enter value 0 for no leading number")
        leading_number = input("Enter leading number: ")

        for file, file_extension, file_name in self.get_file_info():

            # get track number from music file
            tag_info = music_tag.load_file(file)

            # identify track number is not empty
            track_number = int(tag_info['tracknumber'])
            track_artist = str(tag_info['artist'])[0].upper()

            if track_number:
                if leading_number == "0" or leading_number == "":
                    file_with_track_number = f"{track_artist}{track_number:02d}. {file_name}"
                else:
                    file_with_track_number = f"{track_artist}{leading_number}.{track_number:02d}. {file_name}"
            else:
                file_with_track_number = f"{file_name}"

            print(f"{file_name} -> {file_with_track_number}.{file_extension}")

            # rename file
            os.rename(file, f'{file_with_track_number}.{file_extension}')

            # rename lrc file if exist
            self.rename_lrc_file(file_name, file_with_track_number)

    def remove_leading_number(self):
        for file, file_extension, file_name in self.get_file_info():

            # remove leading number with regex
            # removeable pattern are:  01 Song Title  (with or without space)
            #                          01. Song Title (with or without space)
            #                          01- Song Title (with or without space)
            #                          1.11 - Song Title (with or without space)
            #                          1.11 . Song Title (with or without space)

            new_file_name = re.sub('^\d*[-.]?\d*[-.\s]*', '', file_name)

            # get user confirmation before rename file
            print(f"{file_name}.{file_extension} -> {new_file_name}.{file_extension}")

            # rename file
            os.rename(file, f'{new_file_name}.{file_extension}')

            # rename lrc file if exist
            self.rename_lrc_file(file_name, new_file_name)

    def lyrics_to_lrc_tag(self):
        for file, file_extension, file_name in self.get_file_info():

            # get metadata from music file
            tag_info = music_tag.load_file(file)

            # check if lrc file exits
            if os.path.isfile(file_name + '.lrc'):
                with open(file_name + '.lrc', 'r', encoding='utf-8') as f:
                    if tag_info['lyrics']:
                        print("Conflict: lyrics already exist")
                        print(f"\n\n Lyric from metadata:\n {tag_info['lyrics']}")
                        print(f"\n\n Lyric from lrc file:\n {f.read()}")
                        user_input = input(
                            f"\n\nDo you want to overwrite lyrics? (y/n) ")
                        if user_input == "y":
                            tag_info['lyrics'] = f.read()
                            tag_info.save()
                        else:
                            print("Lyrics not overwritten")
                    else:
                        tag_info['lyrics'] = f.read()
                        tag_info.save()
                        print(f"The lyrics of ({file_name}) is embedded.")
            else:
                print(f"{file_name}.lrc not found")

    def filename_to_title_tag(self):
        for file, file_extension, file_name in self.get_file_info():

            # get metadata from music file
            tag_info = music_tag.load_file(file)

            if tag_info['title']:
                tag_info['comment'] = tag_info['title']
                
                tag_info['title'] = file_name
                print(f"Music Title: {file_name}")
                tag_info.save()
            else:
                print(f"\n\nNo title for {file_name}\n\n")
    
    def comment_to_title_tag(self):
        for file, file_extension, file_name in self.get_file_info():

            # get metadata from music file
            tag_info = music_tag.load_file(file)

            if tag_info['title']:
                tag_info['title'] = tag_info['comment']
                print(f"Music Title: {tag_info['title']}")
                tag_info.save()
            else:
                print(f"\n\nNo title for {file_name}\n\n")

    def music_tool_menu(self):
        options = {
            "1": self.tagname_to_filename,
            "2": self.chinese_to_pinyin,
            "3": self.japanese_to_romanji,
            "4": self.trackno_to_filename,
            "5": self.remove_leading_number,
            "6": self.lyrics_to_lrc_tag,
            "7": self.filename_to_title_tag,
            "8": self.comment_to_title_tag,
            "9": self.json_list_to_filename,
            "chinese": [
                self.chinese_to_pinyin,
                self.lyrics_to_lrc_tag,
                self.filename_to_title_tag
            ]
        }
        user_input = input(
            "\n\nSelect option: \n\n"
            "[1] Music tag info to File\n"
            "[2] Covert Chinese to Pinyin\n"
            "[3] Convert Japanese to Romanji\n"
            "[4] Add Track Number to File\n"
            "[5] Remove Leading Number\n"
            "[6] Embed Lyrics to Music lyric tag \n"
            "[7] Embed file name to Music title tag\n"
            "[8] Embed comment to Music title tag\n"
            "[9] music_list.json to File\n\n"
            "Enter option: "
        )

        if user_input in options:
            if isinstance(options[user_input], list):
                for option in options[user_input]:
                    option()
            else:
                options[user_input]()
        else:
            print("Invalid option")

    # helper function of music_tool at below
    def save_to_json(self):
        # save music_dict to json file
        with open("music_list.json", "w", encoding="utf8") as music_json:
            json.dump(self.music_dict, music_json, ensure_ascii=False)
    
    def rename_lrc_file(self, old_name, new_name):
        # After modify the music file name, rename lrc file to have same name
        if os.path.isfile(f"{old_name}.lrc"):
            os.rename(f"{old_name}.lrc", f"{new_name}.lrc")

    
    def get_file_info(self):
        # loop through file directory and return file, file name and file extension
        files = os.listdir()
        for file in files:
            file_extension = os.path.splitext(file)[1].replace('.', '')
            if file_extension in self.music_extension:
                file_name = os.path.splitext(file)[0]
                yield file, file_extension, file_name

if __name__ == "__main__":
    music_tool = MusicTools()
    while True:
        music_tool.music_tool_menu()

