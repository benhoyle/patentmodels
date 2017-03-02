# -*- coding: utf-8 -*-
import nltk
from patentmodels.basemodels import BaseTextSet, BaseTextBlock

# Import nltk stopwords - (swap with our own list with patent stopwords)
eng_stopwords = nltk.corpus.stopwords.words('english')


class PatentDoc:
    """ Object to model a patent document. """
    def __init__(
            self,
            claimset,
            description=None,
            figures=None,
            title=None,
            classifications=None,
            number=None
    ):
        """ description, claimset and figures are objects as below. """
        self.description = description
        self.claimset = claimset
        self.figures = figures
        self.title = title
        self.classifications = classifications
        self.number = number

    def text(self):
        """  Get text of patent document as string. """
        return "\n\n".join([self.description.text(), self.claimset.text()])

    def reading_time(self, reading_rate=100):
        """ Return estimate for time to read. """
        # Words per minute = between 100 and 200
        return len(nltk.word_tokenize(self.text())) / reading_rate


class Paragraph(BaseTextBlock):
    """ Object to model a paragraph of a patent description. """
    pass


class Description(BaseTextSet):
    """ Object to model a patent description. """

    def __getattr__(self, name):
        if name == "paragraphs":
            return self.units

    def get_paragraph(self, number):
        """ Return paragraph having the passed number. """
        return super(Description, self).get_unit(number)


class Figures:
    """ Object to model a set of patent figures. """
    pass
