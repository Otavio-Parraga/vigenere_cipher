import argparse
import string
from utils import *
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--key', default=None)
parser.add_argument('--pt', default=None,
                    help='the plaintext or the path to it')
parser.add_argument('--ct', default=None,
                    help='the ciphertext or the path to it')
parser.add_argument('--output_dir', default=None,
                    help='dir to create an output.txt file')
parser.add_argument('--file_name', default='output',
                    help='name of the output file')
parser.add_argument('--key_limit', default=20, type=int,
                    help='max number of key size trial')

letter2idx = {a: i for i, a in enumerate(string.ascii_lowercase)}
idx2letter = {i: a for a, i in letter2idx.items()}
ALPHABET_SIZE = len(string.ascii_lowercase)

def find_key_size(full_text):
    values_of_coincidence_idx = [[] for x in range(KEY_LIMIT + 1)]

    for i in tqdm(range(1, KEY_LIMIT + 1), desc='Generating subtexts to discover the key size'):
        sub_texts = [[] for x in range(i)]
        for idx, char in enumerate(full_text):
            sub_texts[idx % i].append(char)
        for sub_text in sub_texts:
            values_of_coincidence_idx[i].append(find_index_of_coincidence(''.join(sub_text)))
    return get_most_similar_value(values_of_coincidence_idx)


def break_text_into_key_sizes(key_size, text):
    text_chunks = [text[i:i + key_size]
                   for i in tqdm(range(0, len(text), key_size), desc='Creating text chunks')]
    return text_chunks


def build_chunks_by_order(text_chunks):
    key_size = len(text_chunks[0])
    new_text_chunks = [[] for i in range(key_size)]

    for chunk in tqdm(text_chunks, desc='Creating ordered text chunks'):
        if len(chunk) == key_size:
            for i, char in enumerate(chunk):
                new_text_chunks[i].append(char)
    return [''.join(chunk) for chunk in new_text_chunks]


def cipher_text(key, plaintext):
    """
    Receives a key and a plaintext, as string, and 
    makes the encryption of the plaintext with
    the given key
    """
    encrypted_text = ''
    for i, letter in enumerate(plaintext):
        key_letter = key[i % len(key)]
        new_letter = idx2letter[(letter2idx[letter] + letter2idx[key_letter]) % ALPHABET_SIZE]
        encrypted_text += new_letter
    return encrypted_text


def decipher_text(ciphertext):
    # finds the possible key size
    possible_key_size = find_key_size(ciphertext)
    text_chunks = break_text_into_key_sizes(possible_key_size, ciphertext)
    text_chunks = build_chunks_by_order(text_chunks)

    key = ''

    for chunk in tqdm(text_chunks, desc='Discovering key'):
        frequencies = frequency_analysis(chunk)
        most_common_char = frequencies.most_common(1)[0][0]
        # since "e" is the most common letter in english
        key_char_in_position = (letter2idx[most_common_char] + 26 - letter2idx['e']) % ALPHABET_SIZE
        key += idx2letter[key_char_in_position]
        # check key integrity, so that some key like "abcabcabc" will become only "abc"
        key = check_key_integrity(key)

    print(f'Key Size: {len(key)}')
    print(f'Key: {key}')
    decrypted_text = []

    for i, char in tqdm(enumerate(ciphertext), desc='Decrypting text'):
        key_letter = key[i % len(key)]
        deciphered_char = idx2letter[(letter2idx[char] + 26 - letter2idx[key_letter]) % ALPHABET_SIZE]
        decrypted_text.append(deciphered_char)
    return ''.join(decrypted_text)


if __name__ == '__main__':
    args = parser.parse_args()

    KEY_LIMIT = args.key_limit

    if args.key and args.pt:
        print('Encrypt!')
        key = preprocess_input(args.key)
        plaintext = preprocess_input(args.pt)
        output = cipher_text(key, plaintext)

    elif args.ct:
        print('Decipher!')
        ciphertext = preprocess_input(args.ct)
        output = decipher_text(ciphertext)
    else:
        print('No parameters found.')
        exit()

    if args.output_dir:
        save_text(output, args.file_name)
    else:
        print(output)
