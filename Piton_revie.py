import argparse
import string
import json
from typing import List, Dict, Optional, Union

tabula_recta = 'abcdefghijklmnopqrstuvwxyz'

try:
    def encrypt(text: str, s: int) -> str:
        result = ""
        for i in range(len(text)):
            char = text[i]
            if char in string.punctuation or char == ' ' or char == "\n":
                result += char
            else:
                if char.isupper():
                    result += chr((ord(char) + s - 65) % 26 + 65)
                else:
                    result += chr((ord(char) + s - 97) % 26 + 97)
        return result

    def encrypt1(key: str, text: str) -> str:
        result = []
        space = 0
        for index, ch in enumerate(text):
            if ch in string.punctuation or ch == "\n" or ch == ' ':
                space += 1
                result.append(ch)
            else:
                mj = tabula_recta.index(ch.lower())
                kj = tabula_recta.index(key[(index - space) % len(key)])
                cj = (mj + kj) % len(tabula_recta)
                if ch.isupper() is True:
                    result.append(tabula_recta[cj].upper())
                else:
                    result.append(tabula_recta[cj])
        return ''.join(result)

    slov: Dict[int, List[str]] = {}
    etalon: Dict[str, float] = {}

    def train(tslov: str) -> Dict[str, float]:
        etalon = dict_of_letter_frequency(tslov.lower())
        return etalon

    def hack(textc: str, tslov: Dict[str, float]) -> Dict[int, Optional
                                                          [List[str]]]:
        pt = ''
        for i in range(26):
            pt = decrypt(textc, i)
            slov.setdefault(i, []).append(pt)
        sum: Dict[int, List[float]] = {}
        for key, value in slov.items():
            txt_r = str(value).lower()
            perevod = dict_of_letter_frequency(txt_r)
            sum.setdefault(key, []).append(sumk(tslov, perevod))
        max_keys = sorted(sum, key=sum.get, reverse=False)
        all_pop = {}
        all_pop[max_keys[0]] = slov.get(max_keys[0])
        return all_pop

    def sumk(frequency_text: Dict[str, float], frequency_cipher: Dict
             [str, float]) -> float:
        sumh: float = 0.0
        for key in frequency_cipher.keys():
            if key in frequency_text.keys():
                sumh = sumh + (frequency_text[key] - frequency_cipher[key])**2
        return sumh

    def dict_of_letter_frequency(s: str) -> Dict[str, float]:
        set_for_text = set(s)
        lenght = len(s)
        dict_of_letters = {}
        for symbol in set_for_text:
            if symbol.isalpha() is True:
                dict_of_letters[symbol] = round(s.count(symbol) / lenght, 5)
        # print(dict_of_letters)
        return dict_of_letters

    def decrypt(text: str, s: int) -> str:
        result = ""
        for i in range(len(text)):
            char = text[i]
            if char in string.punctuation or char == ' ' or char == "\n":
                result += char
            else:
                if char.isupper():
                    result += chr((ord(char) - s - 65) % 26 + 65)
                else:
                    result += chr((ord(char) - s - 97) % 26 + 97)
        return result

    def decrypt1(key: str, text: str) -> str:
        result = []
        space = 0
        for index, ch in enumerate(text):
            if ch in string.punctuation or ch == "\n" or ch == ' ':
                space += 1
                result.append(ch)
            else:
                cj = tabula_recta.index(ch.lower())
                kj = tabula_recta.index(key[(index - space) % len(key)])
                mj = (cj - kj) % len(tabula_recta)
                if ch.isupper() is True:
                    result.append(tabula_recta[mj].upper())
                else:
                    result.append(tabula_recta[mj])
        return ''.join(result)

    # Check the above function
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('oper', type=str, help='type{encode|dec|train|desh}')
    parser.add_argument('--cipher', type=str, help='type{caesar|vigenere}')
    parser.add_argument('--key', default='0', help='type int|word')
    parser.add_argument('--input_file', help='type int|word')
    parser.add_argument('--output_file', help='type int|word')
    parser.add_argument('--model_file', nargs='?', help='type int|word')
    args = parser.parse_args()
    oper = args.oper
    tcipr = args.cipher
    if args.key.isalpha() is True:
        sp = str(args.key)
    else:
        sp_int = int(args.key)
        if sp_int > 25:
            sp_int = sp_int % 26
    textp = ''
    if args.input_file is None:
        textp = str(input("Enter text: "))
    else:
        with open(str(args.input_file)) as f:
            for line in f:
                textp += line
            f.close()
    c: Union[str, int, Dict[int, Optional[List[str]]]] = 0
    if oper == 'encode'or oper == 'decode' or oper == 'hack':
        if oper == 'encode':
            if tcipr == 'caesar':
                c = encrypt(textp, sp_int)
            else:
                c = encrypt1(sp, textp)
        if oper == 'decode':
            if tcipr == 'caesar':
                c = decrypt(textp, sp_int)
            else:
                c = decrypt1(sp, textp)
        if oper == 'hack':
            with open(str(args.model_file), 'r') as w:
                txt: Dict[str, float] = json.loads(w.read())
                w.close()
            c = hack(textp, txt)
        if args.output_file is None:
            print(c)
        else:
            with open(str(args.output_file), 'w') as w:
                json.dump(c, w)
                w.close()
    if oper == 'train':
        k = train(textp)
        with open(str(args.model_file), 'w') as w:
            json.dump(k, w)
            w.close()
except Exception:
    print("Error")
