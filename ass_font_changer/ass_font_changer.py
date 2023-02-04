import os
import shutil

import ass

rootdir = r"D:\Download\New folder\Yosuga no Sora"

extensions = ['cht', 'tc']
print(rootdir)

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')
        if file_extension == 'ass':
            file_name = os.path.splitext(file)[0]

            old_subtitle_path = subdir
            subtitle_file_path = subdir + f'\\{file}'

            if "old_subtitles" not in subdir:
                old_subtitle_path = subdir + '\.old_subtitles'
                if not os.path.isdir(old_subtitle_path):
                    os.makedirs(old_subtitle_path)

            if not any(x in file_name for x in extensions):
                print(file_name)

                try:
                    with open(subtitle_file_path, encoding='utf_8_sig') as f:
                        subtitle = ass.parse(f)
                except UnicodeDecodeError:
                    with open(subtitle_file_path, encoding='utf_16') as f:
                        subtitle = ass.parse(f)

                if str(subtitle.styles[0].fontname) != 'Resource Han Rounded CN Regular':
                    try:
                        shutil.copy2(subtitle_file_path, old_subtitle_path + f'\\{file}')
                    except shutil.SameFileError:
                        pass
                    else:
                        for i in range(len(subtitle.styles)):
                            subtitle.styles[i].fontname = 'Resource Han Rounded CN Regular'
                        
                        with open(subtitle_file_path, 'w', encoding='utf_8_sig') as f:
                            subtitle.dump_file(f)
                else:
                    continue


