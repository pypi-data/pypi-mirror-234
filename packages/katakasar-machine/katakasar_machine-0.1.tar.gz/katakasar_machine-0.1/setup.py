from setuptools import setup, find_packages

setup(
    name='katakasar_machine',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'streamlit',  # Sesuaikan dengan dependensi Anda
        'scikit-learn',
        'pandas',
        'nltk',
    ],
)
