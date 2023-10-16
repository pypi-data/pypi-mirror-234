from setuptools import setup, find_packages

VERSION = '1'
DESCRIPTION = 'Quranerabdar'
LONG_DESCRIPTION = 'second Python Package'

# Setting up
setup(
    name="quranerabdar",
    version=VERSION,
    author="Masoud Shafiei",
    author_email="masoudshafiei89@yahoo.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['quran', 'sbu'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)