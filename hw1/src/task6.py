## File Handling
## Nathan Schluessler
def count_words(file_name):
    file_path = str('/home/student/cs4300/hw1/src/' + file_name)
    with open(file_path, 'r') as file:
        file_text = file.read()
        return len(file_text.split())

