import numpy as np
from collections import Counter

# for read and save files
def preprocess_input(inpt):
    if ('/' in inpt) or ('\\' in inpt):
        plaintext = read_file(inpt)
        return plaintext.lower().replace(" ", "")
    else:
        return inpt.lower().replace(" ", "")


def read_file(file_path):
    text = ''
    with open(file_path, mode='r', encoding='utf-8') as f:
        content = f.readlines()
        for line in content:
            text += line
    return text


def save_text(text, file_name):
    with open(f'{file_name}.txt', mode='w', encoding='utf-8') as f:
        f.write(text)
    return True
