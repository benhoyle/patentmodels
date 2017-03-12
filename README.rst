Patent Models
=============

Functions and datamodels for patent data.

Usage
--------------
``from patentmodels import PatentDoc, Description, Claimset, Claims, Classification``

Getting a bag of words from a patent description.

::
    text = [("Lorem ipsum dolor sit amet, consectetur "
            "adipiscing elit. Integer nec odio. \n"),
            ("Praesent libero 100. Sed cursus 102 ante dapibus diam. "
            "Sed nisi. \n"),
            ("Sed, dignissim lacinia, <nunc>. Curabitur tortor 2."
            "Pellentesque nibh. \n"),
            "Quisque volutpat 554 condimentum velit."]
    desc = Description(text)
    desc.bag_of_words()

Provides:
::
    ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consecteturadipisc', 'elit',
    'integ', 'nec', 'odio', 'praesent', 'libero', 'sed', 'cursu', 'ant', 'dapibu',
    'nisi', 'sed', 'dignissim', 'lacinia', 'nunc', 'curabitur', 'tortor', 'nibh',
    'quisqu', 'volutpat', 'condimentum', 'velit']

For a complete patent document:
::
    claims = [
                Claim("Claim {0} has an x.".format(num), num)
                for num in range(1, 10)
                ]
    claimset = Claimset(claims)
    desc = Description(["one", "two", "three"])
    fig = Figures()
    classification = Classification("A")
    pd = PatentDoc(
                claimset,
                desc,
                fig,
                "Title",
                classification,
                "20010101010"
                )
    pd.reading_time()
    pd.claimset.get_claim(5).text



