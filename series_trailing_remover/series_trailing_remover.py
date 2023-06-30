import os
import re

# prompt user for input series name
input_series_name = input("Enter series name: ")

# prompt user for season number
input_season_number = input("Enter season number: ")

# regex pattern to capture series number
pattern_digit = re.compile(r'\[(\d{2})([a-zA-Z]*\d*)\]|(\d{2}\b)')

# regex pattern caputure square bracket and inner content
pattern_bracket = re.compile(r'\[(.*?)\]')

# regex pattern capture string after period
pattern_period = re.compile(r'\.(.*)')

# regex patter capture file extension
pattern_extension = re.compile('[^\.]*\.([^\.]+)$')

# a list to store all the proposed new file names
rename_list = []

files = [entry.name for entry in os.scandir() if entry.is_file()]

for file in files:
    file_extension = re.search(pattern_extension,file)
    file_extension = file_extension.group(1)

    if file_extension in ['nfo', 'srt', 'ass', 'mp4', 'mkv']:

        file_name = os.path.splitext(file)[0]

        # capture series number
        series_number = re.findall(pattern_digit, file_name)
        # print(series_number)
        if series_number[0][0]:
            series_number = series_number[0][0]
        else:
            series_number = series_number[0][2]

        # capture string after period
        subtitle_lang = re.sub(pattern_bracket, "", file_name)
        subtitle_lang = re.search(pattern_period, subtitle_lang)
        if subtitle_lang:
            
            subtitle_lang = subtitle_lang.group(1).lower().replace(" ","")
            print(subtitle_lang)

            if 'sc' in subtitle_lang or 'chs' in subtitle_lang:
                subtitle_lang = '.chs'
            elif 'tc' in subtitle_lang or 'cht' in subtitle_lang:
                subtitle_lang = '.cht'
            else: 
                subtitle_lang = ''          
        else:
            subtitle_lang = ''

        new_file_name = f"Episode S{int(input_season_number):02d}E{series_number} {input_series_name}{subtitle_lang}.{file_extension}"

        # add the proposed new file name to the list
        rename_list.append((file, new_file_name))

# display the rename list to the user
for old_name, new_name in rename_list:
    print(f"{new_name}")

# prompt user to confirm the renaming
user_input = input("Rename all? (y/n) ")
if user_input.lower() == 'y':
    # rename all the files in the rename list
    for old_name, new_name in rename_list:
        os.rename(old_name, f"{new_name}")
    print("All files have been renamed!")
else:
    print("No files have been renamed!")