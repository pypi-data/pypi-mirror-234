''' Functions for data management '''
import os

def fileName(path):
    ''' function that takes path as input and returns unique path if input
    path already exist (prevent data unique data overwrite) '''
    name, suffix = os.path.splitext(path)
    num = ""
    while True:
        new_path = f"{name}{num}{suffix}"
        if not os.path.exists(new_path):
            break
        if num == "":
            num = -1
        num += 1
    return new_path

def get_txt_content(block_name, file_path):
    ''' Function for reading block of code that returns name and text as dictionary,
    blocks of code has to have title in this type: "--- Block1 --- followed by text. '''
    with open(file_path, 'r') as file:
        content = ''
        block_started = False

        for line in file:
            line = line.strip()

            if line == f'--- {block_name} ---':
                block_started = True
            elif line.startswith('--- '):
                block_started = False

            if block_started and line != f'--- {block_name} ---':
                content += line + '\n'

        return {"title": block_name, "text": content.strip()}
