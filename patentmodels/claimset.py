# -*- coding: utf-8 -*-

import nltk
from patentmodels.basemodels import BaseTextSet

# Import nltk stopwords - (swap with our own list with patent stopwords)
eng_stopwords = nltk.corpus.stopwords.words('english')


class Claimset(BaseTextSet):
    """ Object to model a claim set. """

    # Map claims onto units
    def __getattr__(self, name):
        if name == "claims":
            return self.units

    def get_claim(self, number):
        """ Return claim having the passed number. """
        return super(Claimset, self).get_unit(number)

    def claim_tf_idf(self, number):
        """ Calculate term frequency - inverse document frequency statistic
        for claim 'number' when compared to whole claimset. """
        claim = self.get_claim(number)

        # Need to remove punctuation, numbers and normal english stopwords?

        # Calculate term frequencies and normalise
        word_freqs = claim.get_word_freq(normalize=True)

        # Calculate IDF > log(total claims / no. of claims term appears in)
        tf_idf = [{
            'term': key,
            'tf': word_freqs[key],
            'tf_idf': word_freqs[key]*len(self.appears_in(key))
            }
            for key in word_freqs]
        # Sort list by tf_idf
        tf_idf = sorted(tf_idf, key=lambda k: k['tf_idf'], reverse=True)

        return tf_idf

    def independent_claims(self):
        """ Return independent claims. """
        return [c for c in self.claims if c.dependency == 0]

    def get_dependent_claims(self, claim):
        """ Return all claims that ultimately depend on 'claim'."""
        # claim_number = claim.number
        pass

    def get_root_claim_parent(self, claim_number):
        """ If claim is dependent, get independent claim it depends on. """
        claim = self.get_claim(claim_number)
        if claim.dependency == 0:
            return claim.number
        else:
            return self.get_root_claim_parent(claim.dependency)

    def print_dependencies(self):
        """ Output dependencies."""
        for c in self.claims:
            print(c.number, c.dependency)

    def get_dependency_groups(self):
        """ Return a list of sublists, where each sublist is a group
        of claims with common dependency, the independent claim
        being first in the set. """
        # Or a tree structure? - this will be recursive for chains of
        # dependencies
        # First level will be all claims with dependency = 0 then recursively
        # navigate dependencies
        root_list = [
            (claim.number, self.get_root_claim_parent(claim.number))
            for claim in self.claims
            ]
        claim_groups = {}
        for n, d in root_list:
            if d not in claim_groups.keys():
                claim_groups[d] = []
            else:
                claim_groups[d].append(n)
        return claim_groups

    # to print
    # for k in sorted(claim_groups.keys()):
    #   print(k, claim_groups[k])

    def get_entities(self):
        """ Determine a set of unique noun phrases over the claimset."""
        # Do we actually want to do this for sets of claims with common
        # dependencies?
        for claim in self.claims:
            # Build an initial dictionary
            pass

    def extract_claims(self, text):
        """ Attempts to extract claims as a list from a large text string.
        param string text: string containing several claims
        """
        sent_list = nltk.tokenize.sent_tokenize(text)
        # On a test string this returned a list with the claim number
        # and then the claim text as separate items
        claims_list = [
            " ".join(sent_list[i:i+2])
            for i in xrange(0, len(sent_list), 2)
            ]
        return claims_list

    @classmethod
    def clean_data(cls, claim_data):
        """
        Cleans and checks claim_data.

        claim_data may be a list of strings or a giant string
        """

        # If claims_data is a single string attempt to split into a list
        """if not isinstance(claim_data, list):
            claim_data = extract_claims(claim_data)

        claims = [get_number(claim) for claim in claims_list]

        for claim_no in range(1, len(claims)):
            if claims[claim_no-1][0] != claim_no:
                pass"""

        # Checks
        # - len(claims) = claims[-1] number
        # -
        pass
