# -*- coding: utf-8 -*-
from nltk.tokenize import sent_tokenize
import re
from patentmodels.claim import check_claim_class
from patentmodels.lib.utils_claim import (
    get_number, detect_dependency, detect_category
)


def nltk_extract_claims(text):
    """
    Attempts to extract claims as a list from a large text string.
    Uses nltk sent_tokenize function in tokenize library
    param string text: string containing several claims
    """
    sent_list = sent_tokenize(text)
    # On a test string this returned a list with the claim number
    # and then the claim text as separate items
    claims_list = [
        (int(sent_list[i]), sent_list[i+1])
        for i in xrange(0, len(sent_list), 2)
        ]
    return claims_list


def regex_extract_claims(text):
    """
    Uses regex to attempt to extract claims from a large string
    of text.

    :param text: Large string for claimset
    :type text: str
    :return: list of tuples (claim_number, claim_text)
    """
    claim_r = r'((\d+)\s*\.[ |\t])?([A-Z].*?[\.])\s*\n'
    matches = re.finditer(claim_r, text, re.DOTALL)
    claimset_list = []
    match_num = 0
    for match in enumerate(matches):
        match_num = match_num + 1
        claim_text = match.group(3)
        if match.group(2):
            number = match.group(2)
        else:
            number = match_num
        claimset_list.append((number, claim_text))
    return claimset_list


def score_claimset(claimset_list):
    """
    Applies checks and generates a score indicating fitness.

    :param claimset_list: set of (number, text) tuples for claims.
    :type claimset_list: tuples (int, str)
    :return: score normalised between 0 and 1
    """
    score = 0
    # Score total = number of checks
    score_total = 4
    # Tests
    if check_first(claimset_list):
        score = score + 1
    if check_last(claimset_list):
        score = score + 1
    if check_consecutive(claimset_list):
        score = score + 1
    if check_dependencies(claimset_list):
        score = score + 1

    return round((score / score_total), 2)


def check_consecutive(claimset_list):
    """
    Checks claims are numbered consecutively.

    :param claimset_list: set of (number, text) tuples for claims.
    :type claimset_list: tuples (int, str)
    :return: true for consecutive; false if check fails
    """
    previous_number = 0
    try:
        for number, claim in claimset_list:
            if number == (previous_number + 1):
                previous_number = previous_number + 1
            else:
                return False
        return True
    except:
        return False


def check_first(claimset_list):
    """
    Checks claims begin at 1.

    :param claimset_list: set of (number, text) tuples for claims.
    :type claimset_list: tuples (int, str)
    :return: true if first claim = 1; false if check fails
    """
    try:
        if claimset_list[0][0] == 1:
            return True
        else:
            return False
    except:
        return False


def check_last(claimset_list):
    """
    Checks claims end with a claim number = length of list.

    :param claimset_list: set of (number, text) tuples for claims.
    :type claimset_list: tuples (int, str)
    :return: true if last claim = length of claims; false if not
    """
    try:
        if claimset_list[-1][0] == len(claimset_list):
            return True
        else:
            return False
    except:
        return False


def check_for_number(claimset_data):
    """
    Checks if claimset_data contains tuples with an integer entry.

    :param claimset_data: list of tuples or strings.
    :type claimset_data: list of tuples or strings
    :return: true if tuples with numbers; false if not
    """
    try:
        for entry in claimset_data:
            if len(entry) <= 1:
                return False
            else:
                if not isinstance(entry[0], int):
                    return False
        return True
    except:
        return False


def check_set_claims(potential_claimset):
    """ Checks if a passed object is a set of Claim objects. """
    claimset_flag = True
    if isinstance(potential_claimset, list):
        for potential_claim in potential_claimset:
            if not check_claim_class(potential_claim):
                claimset_flag = False
    else:
        claimset_flag = False
    return claimset_flag


def get_numbers(claimset_data):
    """
    Gets claim numbers using regex.

    :param claimset_data: list of strings.
    :type claimset_data: list of tuples or strings
    :return: claimset_list_out list of (number, text) tuples
    """
    claimset_list_out = []
    for entry in claimset_data:
        number, text = get_number(entry)
        claimset_list_out.append((number, text))
    return claimset_list_out


def check_dependencies(claimset_data):
    """
    Checks for dependency consistency.

    :param claimset_data: list of tuples or strings.
    :type claimset_data: list of tuples or strings
    :return: true if dependencies are consistent; false if not
    """
    category = {}
    try:
        for number, text in claimset_data:
            dependency = detect_dependency(text)
            category[number] = detect_category(text)
            # Check dependency is less than current claim number
            if dependency >= number:
                return False
            # Check categories of parent claims match
            if dependency != 0:
                if category[number] != category[dependency]:
                    return False
        return True
    except:
        return False
