# -*- coding: utf-8 -*-

import re
import nltk
from patentmodels.basemodels import BaseTextBlock
from patentmodels.lib.utils_claim import (
    ends_with, get_number, detect_dependency, detect_category
)
import warnings


def check_claim_class(potential_claim):
    """ Check if passed object is of type Claim. """
    return isinstance(potential_claim, Claim)


class Claim(BaseTextBlock):
    """ Object to model a patent claim."""

    def __init__(self, text, number=None, dependency=None):
        """ Initiate claim object with string containing claim text."""
        # Have a 'lazy' flag on this to load some of information when needed?

        # Check for and extract claim number
        parsed_number, text = get_number(text)
        if number:
            if number != parsed_number:
                warnings.warn(
                    """Detected claim number
                    does not equal passed claim number."""
                    )
        else:
            number = parsed_number

        self.text = text
        self.number = number

        # Get category
        self.category = detect_category(self.text)

        # Get dependency
        parsed_dependency = detect_dependency(self.text)
        if dependency:
            self.dependency = dependency
            if dependency != parsed_dependency:
                warnings.warn(
                    """Detected dependency does
                    not equal passed dependency."""
                    )

                if dependency >= self.number:
                    self.dependency = parsed_dependency
        else:
            self.dependency = parsed_dependency

        # Lazily compute the functions below when required

        # Determine word order
        # super(Claim, self).set_word_order()

        # Label parts of speech - uses averaged_perceptron_tagger as
        # downloaded above
        # super(Claim, self).set_pos()
        # Apply chunking into noun phrases
        # (self.word_data, self.mapping_dict) = self.label_nounphrases()

        # Split claim into features
        # self.features = self.split_into_features()

    def determine_entities(self):
        """ Determines noun entities within a patent claim.
        param: pos - list of tuples from nltk pos tagger"""
        # Define grammar for chunking
        grammar = '''
            NP: {<DT|PRP\$> <VBG> <NN.*>+}
                {<DT|PRP\$> <NN.*> <POS> <JJ>* <NN.*>+}
                {<DT|PRP\$>? <JJ>* <NN.*>+ }
            '''
        cp = nltk.RegexpParser(grammar)
        # Or store as part of claim object property?

        # Option: split into features / clauses, run over clauses and
        # then re-correlate
        return cp.parse(self.pos)

    def print_nps(self):
        # ent_tree = self.determine_entities(self.pos)
        # traverse(ent_tree)
        pass

    def split_into_features(self):
        """ Attempts to split a claim into features.
        param string text: the claim text as a string
        """
        featurelist = []
        startindex = 0
        # split_re = r'(.+;\s*(and)?)|(.+,.?(and)?\n)|(.+:\s*)|(.+\.\s*$)'
        split_expression = r'(;\s*(and)?)|(,.?(and)?\n)|(:\s*)|(\.\s*$)'
        p = re.compile(split_expression)
        for match in p.finditer(self.text):
            feature = {}
            feature['startindex'] = startindex
            endindex = match.end()
            feature['endindex'] = endindex
            feature['text'] = self.text[startindex:endindex]
            featurelist.append(feature)
            startindex = endindex
        # Try spliting on ';' or ',' followed by '\n' or ':'
        # splitlist = filter(None, re.split(r";|(,.?\n)|:", text))
        # This also removes the characters - we want to keep them
        # - back to search method?
        # Or store as part of claim object property?
        return featurelist

    def label_nounphrases(self):
        """ Label noun phrases in the output from pos chunking. """
        grammar = '''
            NP: {<DT|PRP\$> <VBG> <NN.*>+}
                {<DT|PRP\$> <NN.*> <POS> <JJ>* <NN.*>+}
                {<DT|PRP\$>? <JJ>* <NN.*>+ }
            '''

        cp = nltk.RegexpParser(grammar)
        result = cp.parse(self.pos)
        ptree = nltk.tree.ParentedTree.convert(result)
        subtrees = ptree.subtrees(filter=lambda x: x.label() == 'NP')

        # build up mapping dict - if not in dict add new entry id+1;
        # if in dict label using key
        mapping_dict = {}
        pos_to_np = {}
        for st in subtrees:
            np_string = " ".join(
                [
                    leaf[0] for leaf in st.leaves()
                    if leaf[1] != ("DT" or "PRP$")
                ]
            )
            np_id = mapping_dict.get(np_string, None)
            if not np_id:
                # put ends_with here
                nps = [i[0] for i in mapping_dict.items()]
                ends_with_list = [
                    np for np in nps if ends_with(np_string, np)
                ]
                if ends_with_list:
                    np_id = mapping_dict[ends_with_list[0]]
                else:
                    np_id = len(mapping_dict)+1
                    mapping_dict[np_string] = np_id
            pos_to_np[st.parent_index()] = np_id

        # Label Tree with entities
        flat_list = []
        for i in range(0, len(ptree)):
            # print(i)
            # Label
            if isinstance(ptree[i], nltk.tree.Tree):
                for leaf in ptree[i].leaves():
                    # Unpack leaf and add label as triple
                    flat_list.append((leaf[0], leaf[1], pos_to_np.get(i, "")))
            else:
                flat_list.append(
                    (ptree[i][0], ptree[i][1], pos_to_np.get(i, ""))
                )
        return (flat_list, mapping_dict)

    def json(self):
        """ Provide words as JSON. """
        # Add consecutive numbered ids for Reactgit
        # Words = [{"id": i, "word":word, "pos":part}
        # for i, (word, part) in list(enumerate(self.pos))]
        words = [
            {"id": i, "word": word, "pos": part, "np": np}
            for i, (word, part, np) in list(enumerate(self.word_data))
            ]
        return {"claim": {"words": words}}

    @classmethod
    def check_claim(cls, text, number=None):
        """
        Cleans and checks claim text.

        :param text: Claim text
        :type text: str
        :param number: Claim number
        :type text: integer
        :return: None
        """
        parsed_number, text = get_number(text)
        if number:
            if number != parsed_number:
                print(
                    """Warning: detected claim number
                    does not equal passed claim number."""
                    )
        else:
            number = parsed_number
