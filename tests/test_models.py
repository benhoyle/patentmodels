from patentmodels import (
    PatentDoc, Description, Figures, Claimset, Claim, Classification
)


class TestGeneral(object):
    """ General set of tests."""

    def test_claims(self):
        """ Test Claim objects. """
        claim = Claim("Claim 1 has an x.", 1)
        assert claim.number == 1
        assert "has an x" in claim.text

    def test_description(self):
        """ Test Description objects. """
        desc = Description(["one", "two", "three"])
        assert "two" in desc.get_paragraph(2).text

    def test_claimset(self):
        """ Test Claimset objects. """
        claims = [
            "{0}. Claim {0} has an x.".format(num)
            for num in range(1, 11)
            ]
        claimset = Claimset(claims)

        assert claimset.count == 10
        assert "Claim 5 has an x" in claimset.get_claim(5).text
        assert isinstance(claimset.claims[2], Claim)

    def test_init(self):
        """ Test all objects initialise. """
        claims = [
            Claim("Claim {0} has an x.".format(num), num)
            for num in range(1, 10)
            ]
        claimset = Claimset(claims)
        desc = Description(["one", "two", "three"])
        fig = Figures()
        classification = Classification("A")

        pd1 = PatentDoc(claimset)
        pd2 = PatentDoc(
            claimset,
            desc,
            fig,
            "Title",
            classification,
            "20010101010"
            )

        assert "has an x" in pd1.text
        assert "has an x" in pd2.text
        assert "three" in pd2.text
        assert pd1.reading_time() > 0 and \
            pd1.reading_time() < pd2.reading_time()

class TestDescription(object):
    """ Test description functions. """
    def test_init(self):
        pass

    def test_paragraphs(self):
        pass

    def test_bag_of_words(self):
        pass
