filename = "01. INSIDE IDENTITY.lrc"

try:
    with open(filename, "r") as file:
        lines = file.readlines()
except UnicodeDecodeError:
    # open file with encoding="gbk"
    with open(filename, 'r', encoding="gbk") as f:
        lines = file.readlines()

result = []
for line in lines:
    parts = line.split("]")
    time = parts[0] + "]"
    text = parts[1].strip()
    result.append(time + text + "\t")

filename = "01.lrc"
with open(filename, "w") as file:
    file.write("\n".join(result))