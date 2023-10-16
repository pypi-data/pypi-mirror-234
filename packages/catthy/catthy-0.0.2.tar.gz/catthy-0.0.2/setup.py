from setuptools import setup, find_packages

META = {
    "name":"catthy",
    "version":"0.0.2",
    "description":"Functional Python library.",
    "long_description":"Functional Python library for playing around with functors.",
    "long_description_content_type":"text/markdown",
    "url":"https://github.com/joangq/catthy",
    "author":"Joan Gonzalez",
    "author_email":"jgquiroga@dc.uba.ar",
    "license":"LGPL-3.0",
    "packages":["catthy"],
    "keywords":"functor applicative function",
    "classifiers":["Development Status :: 1 - Planning"],
    "python_requires":">=3.7",
    "install_requires":[],
}

if __name__ == "__main__":
    setup(**META)
