## Vigenère Cipher
Code for encrypting and decrypting texts using Vigenere Cipher

### To install requirements with pip and python3:
* ```pip install -r requirements.txt```

### How to Run?
* To encrypt a plaintext
  * ```python vigenere_cipher.py --pt <path_or_text> --key <key> ```
* To decrypt a plaintext
  * ```python vigenere_cipher.py --ct <path_or_text> ```
* To set an output directory and name for the output file:
  * ```python vigenere_cipher.py --ct <path_or_text> --output_dir <dir> --file_name <output_file_name>```
* Example of full command:
  * ```python vigenere_cipher.py --ct cipher1.txt --output_dir ./ --file_name cipher1-output.txt```

### TODO:
* text decryption is strongly influenced by key limit size
* is it possible to remove check_key_integrity()?
* change some names and terms