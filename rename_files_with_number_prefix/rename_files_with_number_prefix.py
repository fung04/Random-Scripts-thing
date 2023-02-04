import os

files = os.listdir()

starting_number = int(input("Enter starting number: "))

for file in files:
    file_extension = os.path.splitext(file)[1].replace('.', '')
    starting_number +=1

    os.rename(file, f"{starting_number}.{file_extension}")


    


