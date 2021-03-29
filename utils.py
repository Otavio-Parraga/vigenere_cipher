import numpy as np
from collections import Counter


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


def find_index_of_coincidence(text):
    frequencies = frequency_analysis(text)
    dividend = np.sum([x * (x - 1) for x in frequencies.values()])
    divisor = len(text) * (len(text) - 1)
    return dividend / divisor


def frequency_analysis(text):
    count = Counter(text)
    return count


def check_key_integrity(possible_key):
    i = (possible_key + possible_key).find(possible_key, 1, -1)
    return possible_key if i == -1 else possible_key[:i]


def get_most_similar_value(list_of_lists, factor=0.0001):
    list_of_avgs = [np.mean(x) - (factor * i) for i,x in enumerate(list_of_lists) if len(x) != 0]
    return np.argmax(list_of_avgs) + 1
