import os
import re

# get folder name from current working directory
folder_name = os.path.basename(os.getcwd())
input_user = input(f"Is the folder name '{folder_name}' the series name? (y/n) ")

if input_user.lower() == 'n':
    # prompt user for input series name
    input_series_name = input("Enter series name: ")
else:
    input_series_name = folder_name

# prompt user for season number
input_season_number = input("Enter season number: ")

# regex pattern to capture series number https://regex101.com/r/aLIUSo/1
pattern_digit = re.compile(r'\[?(?P<series_number_1>\d{1,2})[a-zA-Z]+\d{1,2}\]?|\b(?P<series_number_2>\d{2})\b|EP(?P<series_number_3>\d{1,2})')

# regex pattern caputure square bracket and inner content https://regex101.com/r/P2pVH9/1
pattern_first_bracket = re.compile(r'^\[(.+?)\]\[?')

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
    file_extension = re.search(pattern_extension, file)
    file_extension = file_extension.group(1)
    if file_extension in ['nfo', 'srt', 'ass', 'mp4', 'mkv']:
        file_name = os.path.splitext(file)[0]
        
        # capture series number
        series_number = re.finditer(pattern_digit, file_name)
        series_number_found = False
        for sn in series_number:
            if sn.group("series_number_1") or sn.group("series_number_2") or sn.group("series_number_3"):
                series_number = sn.group("series_number_1") or sn.group("series_number_2") or sn.group("series_number_3") or sn
                series_number_found = True
                break
        
        if not series_number_found:
            print(f"Warning: No series number found for file: {file}")
            continue  # Skip to the next file
        
        # capture string after period
        subtitle_lang = re.sub(pattern_bracket, "", file_name)
        subtitle_lang = re.search(pattern_period, subtitle_lang)
        if subtitle_lang:             
            subtitle_lang = subtitle_lang.group(1).lower().replace(" ","")
            if 'sc' in subtitle_lang or 'chs' in subtitle_lang or 'scjp' in subtitle_lang:
                subtitle_lang = '.chs'
            elif 'tc' in subtitle_lang or 'cht' in subtitle_lang or 'scjp' in subtitle_lang:
                subtitle_lang = '.cht'
            else:
                subtitle_lang = ''
        else:
            subtitle_lang = ''
        
        new_file_name = f"Episode S{int(input_season_number):02d}E{int(series_number):02d} {input_series_name}{subtitle_lang}.{file_extension}"
        
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
    print("Changing ASS Font style (if any)")
    os.system(f"ass_font_changer.py \"{os.getcwd()}\"")
else:
    print("No files have been renamed!")
    
input("Press Enter to exit...")