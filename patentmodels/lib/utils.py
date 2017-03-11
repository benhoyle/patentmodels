# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
from re import sub
from nltk.stem.porter import * 

# Extend these stopwords to include patent stopwords
ENG_STOPWORDS = stopwords.words('english')


def check_list(listvar):
    """Turns single items into a list of 1."""
    if not isinstance(listvar, list):
        listvar = [listvar]
    return listvar


def safeget(dct, *keys):
    """ Recursive function to safely access nested dicts or return None.
    param dict dct: dictionary to process
    param string keys: one or more keys"""
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def remove_non_words(text):
    """ Remove digits and punctuation from text. """
    # translate has Python 2-3 issues - better to use re.sub
    return sub('\W+', '', text)


def remove_stopwords(tokens):
    """ Remove stopwords from tokens. """
    return [w for w in tokens if not w in ENG_STOPWORDS]


def stem(tokens): 
    """ Stem passed text tokens. """
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def lemmatise(tokens_with_pos):
    """ Lemmatise tokens using pos data. """
    pass

    


