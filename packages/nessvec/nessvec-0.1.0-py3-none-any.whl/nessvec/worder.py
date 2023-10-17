""" Brute force word creation, filtering on semantic and/or syntactic constraints

Define an arbitrary is_match function to filter by syntax or semantics or both.

>>> words = list(generate_words(['BAMRD', 'EDACS', 'SLR', 'TC', 'RSB', 'EMLDIS'], shuffle_char_lists=True))
>>> len(words)
1944000
"""
from itertools import product, permutations
from .spacy_language_model import nlp
from tqdm import tqdm
from math import factorial
from functools import cache


@cache
def generate_words(char_lists, shuffle_char_lists=False, is_match=None):
    """ Return a word generator based on the lists of allowed characters at each position

    Inputs
      char_lists (list of lists of chars, list of strs): product(list_of_chars) generates possible words
      is_match (function): arbitrary function that accepts 2 words to filter by syntax and/or semantics

    >>> list(generate_words(['abc', 'de']))
    ['ad', 'ae', 'bd', 'be', 'cd', 'ce']
    >>> list(generate_words(['abc', 'de'], shuffle_char_lists=True))
    ['ad', 'ae', 'bd', 'be', 'cd', 'ce', 'da', 'db', 'dc', 'ea', 'eb', 'ec']
    >>> list(generate_words(['abc', 'de'], shuffle_char_lists=True, is_match=lambda x: x[0] in 'bc'))
    ['bd', 'be', 'cd', 'ce']
    """
    if is_match is None:
        def is_match(x):
            return True
    if shuffle_char_lists:
        for chlists in tqdm(permutations(char_lists), total=factorial(len(char_lists))):
            # print(chlists)
            for word in generate_words(
                    chlists, shuffle_char_lists=False, is_match=is_match):
                yield word
    else:
        for chars in product(*char_lists):
            word = ''.join(chars)
            if is_match(word):
                yield word


@cache
def is_scrabble_word(s):
    return list(nlp(s))[0].pos_ not in {'PROPN'}


def is_pos(s, parts_of_speech={'PROPN'}):
    if isinstance(parts_of_speech, str):
        parts_of_speech = {parts_of_speech}
    return list(nlp(s))[0].pos_ in parts_of_speech


def not_pos(s, parts_of_speech={'PROPN'}):
    return not is_pos(s, parts_of_speech=parts_of_speech)


def generate_acronyms(word_lists, shuffle_word_lists=False, is_match=is_scrabble_word):
    """ Lists of words to form the ACRYNYM from 

    >>> list(generate_acronyms([['Axe', 'Bob', 'Cat'], ['Dog', 'Egg']]))
    ['AD', 'AE', 'BD', 'BE', 'CD', 'CE']
    """
    char_lists = [[word[0].upper() for word in word_list] for word_list in word_lists]
    return generate_words(char_lists, shuffle_char_lists=shuffle_word_lists,
                          is_match=is_match)
