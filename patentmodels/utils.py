# -*- coding: utf-8 -*-
from nltk.corpus import stopwords


def check_list(listvar):
    """Turns single items into a list of 1."""
    if not isinstance(listvar, list):
        listvar = [listvar]
    return listvar


ENG_STOPWORDS = stopwords.words('english')
