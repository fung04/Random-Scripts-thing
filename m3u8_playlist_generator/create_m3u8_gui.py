import os
import re
import tkinter as tk
import music_tag
from tkinter import filedialog, messagebox
from ttkwidgets import CheckboxTreeview


def update_directory_tree(playlist_relative_path=None, playlist_folder_list=None):
    ext = ['flac', 'wav', 'dsf', 'ape', 'mp3']
    root_path = folder_var.get()
    
    directory_tree.delete(*directory_tree.get_children())
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            if dirpath == root_path:
                continue # skip checking root path
            
            if len(filenames) > 0 and any(f.split('.')[-1] in ext for f in filenames):
                parent = directory_tree.insert('', 'end', text=os.path.basename(dirpath), open=False)
            
            if playlist_folder_list and os.path.basename(dirpath) in playlist_folder_list:
                for f in filenames:    
                    file_relative_path = os.path.relpath(f'{dirpath}\{f}')
                    file_extension = f.split('.')[-1]
                    
                    if file_extension in ext:
                        music_file = int(music_tag.load_file(file_relative_path)['#length'])
                        file_duration = f"{int(music_file/60)}:{int(music_file%60):02d}"

                        if file_relative_path in playlist_relative_path:
                            directory_tree.change_state(parent, "checked") 
                        else:
                            directory_tree.change_state(parent, "unchecked")
                            directory_tree._tristate_parent(parent) 
                    
                        directory_tree.insert(parent, 'end', text=f, values=(file_duration, file_relative_path,))
            else:
                for f in filenames:    
                    file_relative_path = os.path.relpath(f'{dirpath}\{f}')
                    file_extension = f.split('.')[-1]
                    
                    if file_extension in ext:
                        music_file = int(music_tag.load_file(file_relative_path)['#length'])
                        file_duration = f"{int(music_file/60)}:{int(music_file%60):02d}"

                        directory_tree.insert(parent, 'end', text=f, values=(file_duration, file_relative_path,))

    except Exception as e:
        messagebox.showerror("Error", f"Error reading directory: {e}")


def browse_folder():
    root_path = filedialog.askdirectory()
    folder_var.set(root_path)
    update_directory_tree()


def browse_playlist():
    m3u8_playlist_file = filedialog.askopenfilename()
    playlist_var.set(m3u8_playlist_file)
    music_filenames_path = []
    music_folder_names = []

    with open(playlist_var.get(), 'r', encoding='utf_8') as f:
        for line in f:
            if not re.match(r'\#(.*)\n', line):
                music_filenames_path.append(line.strip())

    music_folder_names = set(os.path.basename(os.path.dirname(path)) for path in music_filenames_path)

    update_directory_tree(music_filenames_path, music_folder_names)


def create_playlist():
    play_list = "#EXTM3U\n"
    checked_items = directory_tree.get_checked()
    playlist_name = playlist_name_entry.get()

    for item in checked_items:
        file_relative_path = directory_tree.item(item, "values")[1]
        music_file = music_tag.load_file(file_relative_path)
        file_name = f"{music_file['artist']} - {music_file['tracktitle']}"

        play_list += f"#EXTINF:{file_name}\n{file_relative_path}\n"

    # prompt user to save playlist
    playlist_path = filedialog.asksaveasfilename(initialdir="/", title="Save Playlist", filetypes=(
        ("m3u8 filenames", "*.m3u8"), ("all filenames", "*.*")), defaultextension=".m3u8", initialfile=playlist_name)
    if playlist_path:
        with open(playlist_path, 'w', encoding='utf_8') as f:
            f.write(play_list)
        messagebox.showinfo(
            "Success", f"Playlist {playlist_name} created successfully!")


# Create the main window
root = tk.Tk()
root.title("Playlist Creator")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.TOP, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.TOP, padx=10, pady=10)

folder_label = tk.Label(left_frame, text="Select a folder:")
folder_label.pack()
folder_var = tk.StringVar()
folder_entry = tk.Entry(left_frame, textvariable=folder_var, width=50)
folder_entry.pack()
browse_button = tk.Button(
    left_frame, text="Browse Folder", command=browse_folder)
browse_button.pack()


playlist_label = tk.Label(right_frame, text="Select a Playlist:")
playlist_label.pack()
playlist_var = tk.StringVar()
playlist_entry = tk.Entry(right_frame, textvariable=playlist_var, width=50)
playlist_entry.pack()
browse_button = tk.Button(
    right_frame, text="Browse Playlist", command=browse_playlist)
browse_button.pack()


# Create and place a label for the directory tree
directory_label = tk.Label(root, text="Directory Contents:")
directory_label.pack()

# Create and place a Treeview widget to display the directory and filenames
directory_tree = CheckboxTreeview(root, columns=('Duration','Relative Path',))
directory_tree.heading('#0', text='Directory', anchor='w')
directory_tree.heading('Duration', text='Duration', anchor='w')
directory_tree.heading('Relative Path', text='Relative Path', anchor='w')
directory_tree.pack(fill="both", expand='1')

# Create and place a label for playlist name
playlist_name_label = tk.Label(root, text="Enter playlist name:")
playlist_name_label.pack()

# Create and place an entry field for playlist name
playlist_name_entry = tk.Entry(root, width=50)
playlist_name_entry.pack()

# Create and place a button to create the playlist
create_button = tk.Button(
    root, text="Create Playlist", command=create_playlist)
create_button.pack()

root.mainloop()
