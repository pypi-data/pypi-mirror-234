from setuptools import setup, find_packages

setup(
    name='katakasar-machine',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'pandas',
        'nltk',
    ],
)
