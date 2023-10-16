from setuptools import setup, find_packages

setup(
    name='katakasar_machine',
    version='0.7',
    packages=find_packages(),
    package_data={
        'katakasar_machine': ['model.pkl', 'tfidf_vectorizer.pkl'],
    },
    install_requires=[
        'scikit-learn',
        'pandas',
        'nltk',
    ],
)
