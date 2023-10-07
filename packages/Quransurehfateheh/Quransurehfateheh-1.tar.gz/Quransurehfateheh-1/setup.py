from setuptools import setup, find_packages

VERSION = '1'
DESCRIPTION = 'Quransurehfateheh'
LONG_DESCRIPTION = 'Quran_package'

# Setting up
setup(
    name="Quransurehfateheh",
    version=VERSION,
    author="Masoud Shafiei",
    author_email="masoudshafiei89@yahoo.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['quran', 'sureh','fateheh'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)