import argparse
import json
import string
from typing import List, Dict, Optional, Union
from collections import Counter

TABULA_RECTA = string.ascii_lowercase
NUMBER_OF_DECRYPTIONS = 26


class Cipher:
    slov: Dict[int, List[str]] = {}
    etalon: Dict[str, float] = {}

    def encrypt_caesar(self, text: str, s: int) -> str:
        res = ""
        for char in text:
            if char not in TABULA_RECTA:
                res += char
            else:
                if char.isupper():
                    res += chr((ord(char) + s - ord('A')) % len(TABULA_RECTA)
                               + ord('A'))
                else:
                    res += chr((ord(char) + s - ord('a')) % len(TABULA_RECTA) +
                               ord('a'))
        return res

    def encrypt_vigenere(self, key: str, text: str) -> str:
        res = ''
        result: List[str] = []
        space = 0
        for index, ch in enumerate(text):
            if ch not in TABULA_RECTA:
                space += 1
                result.append(ch)
            else:
                mj = TABULA_RECTA.index(ch.lower())
                kj = TABULA_RECTA.index(key[(index - space) % len(key)])
                cj = (mj + kj) % len(TABULA_RECTA)
                if ch.isupper():
                    result.append(TABULA_RECTA[cj].upper())
                else:
                    result.append(TABULA_RECTA[cj])
        return res.join(result)

    def train(self, tslov: str) -> Dict[str, float]:
        self.etalon = self.dict_of_letter_frequency(tslov.lower())
        return self.etalon

    def hack(self, textc: str, tslov: Dict[str,
             float]) -> Dict[int, Optional[List[str]]]:
        pt = ''
        for i in range(NUMBER_OF_DECRYPTIONS):
            pt = self.decrypt_caesar(textc, i)
            self.slov.setdefault(i, []).append(pt)
        sum: Dict[int, List[float]] = {}
        for key, value in self.slov.items():
            txt_r = str(value).lower()
            perevod = self.dict_of_letter_frequency(txt_r)
            sum.setdefault(key, []).append(self.sum_of_squares(tslov,
                                           perevod))
        max_keys = sorted(sum, key=sum.get, reverse=False)
        all_pop = {}
        all_pop[max_keys[0]] = self.slov.get(max_keys[0])
        return all_pop

    def sum_of_squares(self, frequency_text: Dict[str, float],
                       frequency_cipher: Dict[str, float]) -> float:
        sumh: float = 0.0
        for key in frequency_cipher:
            if key in frequency_text:
                sumh += (frequency_text[key] - frequency_cipher[key])**2
        return sumh

    def dict_of_letter_frequency(self, s: str) -> Dict[str, float]:
        set_for_text = set(s)
        counter = Counter(s)
        length = len(s)
        dict_of_letters = {}
        for symbol in set_for_text:
            if symbol.isalpha() and length > 0:
                dict_of_letters[symbol] = round(counter[symbol] / length, 5)
        return dict_of_letters

    def decrypt_caesar(self, text: str, s: int) -> str:
        s = -s
        return self.encrypt_caesar(text, s)

    def decrypt_vegenere(self, key: str, text: str) -> str:
        res = ''
        result: List[str] = []
        space = 0
        for index, ch in enumerate(text):
            if ch not in TABULA_RECTA:
                space += 1
                result.append(ch)
            else:
                cj = TABULA_RECTA.index(ch.lower())
                kj = TABULA_RECTA.index(key[(index - space) % len(key)])
                mj = (cj - kj) % len(TABULA_RECTA)
                if ch.isupper():
                    result.append(TABULA_RECTA[mj].upper())
                else:
                    result.append(TABULA_RECTA[mj])
        return res.join(result)


def main() -> None:
    obj = Cipher()
    # Check the above function
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('action', type=str, help='{enc|dec|train|hack}')
    parser.add_argument('--cipher', type=str, help='{caesar|vigenere}')
    parser.add_argument('--key', default='0', help='type int|word')
    parser.add_argument('--input_file', help='type int|word')
    parser.add_argument('--output_file', help='type int|word')
    parser.add_argument('--model_file', nargs='?', help='type int|word')
    args = parser.parse_args()
    action = args.action
    tcipr = args.cipher
    if args.key.isalpha():
        sp = str(args.key)
    else:
        try:
            float(args.key)
            sp_int = int(args.key)
            sp_int = sp_int % NUMBER_OF_DECRYPTIONS
        except ValueError:
            print("Please enter a number or word for key")
            return
    textp = ''
    if args.input_file is None:
        textp = input("Enter text: ")
    else:
        with open(str(args.input_file)) as f:
            textp = f.read()
    maincharacter: Union[str, int, Dict[int, Optional[List[str]]]] = 0
    try:
        if action in ('encode', 'decode', 'hack'):
            try:
                if action == 'encode':
                    if tcipr == 'caesar':
                        maincharacter = obj.encrypt_caesar(textp, sp_int)
                    elif tcipr == 'vigenere':
                        maincharacter = obj.encrypt_vigenere(sp, textp)
                    else:
                        raise SyntaxError
                if action == 'decode':
                    if tcipr == 'caesar':
                        maincharacter = obj.decrypt_caesar(textp, sp_int)
                    elif tcipr == 'vigenere':
                        maincharacter = obj.decrypt_vegenere(sp, textp)
                    else:
                        raise SyntaxError
            except Exception:
                print("Entered wrong cipher or key")
                return
            if action == 'hack':
                with open(str(args.model_file), 'r') as w:
                    txt: Dict[str, float] = json.loads(w.read())
                maincharacter = obj.hack(textp, txt)
            if args.output_file is None:
                print(maincharacter)
            else:
                with open(str(args.output_file), 'w') as w:
                    json.dump(maincharacter, w)
        elif action == 'train':
            text_train = obj.train(textp)
            with open(str(args.model_file), 'w') as w:
                json.dump(text_train, w)
        else:
            raise ValueError
    except ValueError:
        print("The action does not exist")


if __name__ == '__main__':
    main()
