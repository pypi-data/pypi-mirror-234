from setuptools import setup, find_packages

setup(
    name='katakasar_machine',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'pandas',
        'nltk',
    ],
)
