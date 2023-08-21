import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]

starting_number = int(input("Enter starting number: "))

for file in files:
    file_extension = os.path.splitext(file)[1].replace('.', '')
    if file_extension != "py":
        starting_number +=1

        os.rename(file, f"{starting_number}.{file_extension}")


    


