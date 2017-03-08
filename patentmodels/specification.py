# -*- coding: utf-8 -*-
from nltk import word_tokenize
from patentmodels.basemodels import BaseTextSet, BaseTextBlock
from patentmodels.lib.utils import check_list

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

    @property
    def text(self):
        """  Get text of patent document as string. """
        if self.description:
            desc_text = self.description.text
        else:
            desc_text = ""
        return "\n\n".join([desc_text, self.claimset.text])

    def reading_time(self, reading_rate=100):
        """ Return estimate for time to read. """
        # Words per minute = between 100 and 200
        return len(word_tokenize(self.text)) / reading_rate


class Paragraph(BaseTextBlock):
    """ Object to model a paragraph of a patent description. """
    pass


class Description(BaseTextSet):
    """ Object to model a patent description. """

    def __init__(self, initial_input):
        """ Initialise object.

        :param initial_input: Set of Paragraph objects, str or list
        of strings
        :type initial_input: list of Paragraph/str or str
        :return: None
        """
        input_list = check_list(initial_input)
        para_list = []
        for para in input_list:
            if not isinstance(para, Paragraph):
                para_object = Paragraph(para)
            else:
                para_object = para
            para_list.append(para_object)

        # self.units = para_list
        # self.count = len(self.units)
        super(Description, self).__init__(para_list)

    def __getattr__(self, name):
        if name == "paragraphs":
            return self.units

    def get_paragraph(self, number):
        """ Return paragraph having the passed number. """
        return super(Description, self).get_unit(number)


class Figures:
    """ Object to model a set of patent figures. """
    pass
