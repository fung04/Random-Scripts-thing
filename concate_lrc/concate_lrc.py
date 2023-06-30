import re
import os

concated_lyrics = str()
lrc_dict = {}
error_list = []

#prompt user for directory
rootdir = input("Enter directory: ")
rootdir = r"{}".format(rootdir)

for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        if filename.endswith('.lrc'):
            filepath = os.path.join(parent, filename)
            try:
                with open(filepath, 'r', encoding="utf-8") as f:
                    input_lrc = f.read()  
            except UnicodeDecodeError:
                # open file with encoding="gbk"
                with open(filepath, 'r', encoding="gbk") as f:
                    input_lrc = f.read()
            
            parse_lrc = input_lrc.split("\n")
            for line in parse_lrc:
                lrc_regex = re.search(r'\[(.*)\](.*)', line)

                if lrc_regex:
                    lrc_timestamp = lrc_regex.group(1)
                    lrc_string = lrc_regex.group(2)

                    # store key value pair to lrc_dict
                    if lrc_timestamp in lrc_dict:
                        lrc_dict[lrc_timestamp] += f' {lrc_string}'
                    else:
                        lrc_dict[lrc_timestamp] = lrc_string

            for key, value in lrc_dict.items():
                # export to file
                concated_lyrics += f'[{key}]{value}\n'
                print(f'[{key}]{value}\n')

            with open(filepath, "w", encoding="utf-8") as f:
                    f.write(concated_lyrics)
            print(filepath)
