
with open("task6_read_me.txt", "r") as file:
    file_text = file.read
    count = len(file_text.split())
    print(count)

