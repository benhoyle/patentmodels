# -*- coding: utf-8 -*-

import re
import nltk
from patentmodels.basemodels import BaseTextBlock

# Import nltk stopwords - (swap with our own list with patent stopwords)
eng_stopwords = nltk.corpus.stopwords.words('english')


def ends_with(s1, s2):
    """See if s1 ends with s2."""
    pattern = re.compile(r'(' + re.escape(s2) + ')$')
    located = pattern.search(s1)
    if located:
        return True
    else:
        return False


class Claim(BaseTextBlock):
    """ Object to model a patent claim."""

    def __init__(self, text, number=None, dependency=None):
        """ Initiate claim object with string containing claim text."""
        # Have a 'lazy' flag on this to load some of information when needed?

        # Check for and extract claim number
        parsed_number, text = self.get_number(text)
        if number:
            number = number
            if number != parsed_number:
                print(
                    """Warning: detected claim number
                    does not equal passed claim number."""
                    )
        else:
            number = parsed_number

        super(Claim, self).__init__(text, number)

        # Get category
        self.category = self.detect_category()

        # Get dependency
        parsed_dependency = self.detect_dependency()
        if dependency:
            self.dependency = dependency
            if dependency != parsed_dependency:
                # print(
                #    "Warning: detected dependency does "
                #    "not equal passed dependency."
                #    )
                # Quick check - parsed dependency likely to be correct
                # if passed dependency >= claim number
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

    def get_number(self, text):
        """Extracts the claim number from the text."""
        p = re.compile('\d+\.')
        located = p.search(text)
        if located:
            # Set claim number as digit before fullstop
            number = int(located.group()[:-1])
            text = text[located.end():].strip()
        else:
            number = 0
            text = text
        return number, text

    def detect_category(self):
        """
        Attempts to determine and return a string containing the
        claim category.
        """
        p = re.compile('(A|An|The)\s([\w-]+\s)*(method|process)\s(of|for)?')
        located = p.search(self.text)
        # Or store as part of claim object property?
        if located:
            return "method"
        else:
            return "system"

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

    def detect_dependency(self):
        """
        Attempts to determine if the claim set out in text is dependent
        - if it is dependency is returned - if claim is deemed independent
        0 is returned as dependency
        """
        p = re.compile(
            '(of|to|with|in)?\s(C|c)laims?\s\d+'
            '((\sto\s\d+)|(\sor\s(C|c)laim\s\d+))?(,\swherein)?'
        )
        located = p.search(self.text)
        if located:
            num = re.compile('\d+')
            dependency = int(num.search(located.group()).group())
        else:
            # Also check for "preceding claims" or "previous claims" = claim 1
            pre = re.compile(
                '\s(preceding|previous)\s(C|c)laims?(,\swherein)?'
            )
            located = pre.search(self.text)
            if located:
                dependency = 1
            else:
                dependency = 0
        # Or store as part of claim object property?
        return dependency

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
