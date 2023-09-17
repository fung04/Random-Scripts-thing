import os
from natsort import natsorted

files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = natsorted(files)  # Perform natural sort on filenames

starting_number = int(input("Enter starting number: "))

for file in files:
    file_extension = os.path.splitext(file)[1].replace('.', '')
    if file_extension != "py":
        starting_number += 1
        new_filename = f"{starting_number}.{file_extension}"
        os.rename(file, new_filename)
        print(f"Renamed '{file}' to '{new_filename}'")
