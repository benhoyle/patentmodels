from patentmodels import (
    PatentDoc, Description, Figures, Claimset, Claim, Classification
)


class TestGeneral(object):
    """ General set of tests."""

    def test_claims(self):
        """ Test claim objects. """
        claim = Claim("Claim 1 has an x.", 1)
        assert claim.number == 1
        assert "has an x" in claim.text

    def test_description(self):
        """ Test description objects. """
        desc = Description(["one", "two", "three"])
        assert "two" in desc.get_paragraph(2).text

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
