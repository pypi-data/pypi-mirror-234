import os
import setuptools


def requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), encoding='utf-8') as f:
        return f.read().splitlines()


setuptools.setup(
    name="cookienlp",
    version="1.0.1",
    license='MIT',
    author="sjang01",
    author_email="sjang01@naver.com",
    description="copy and test from ratsgo/ratsnlp (tools for Natural Language Processing)",
    long_description=open('README.md').read(),
    url="https://github.com/sjang01/cookienlp",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        'cookienlp.nlpbook.classification': ['*.html'],
        'cookienlp.nlpbook.ner': ['*.html'],
        'cookienlp.nlpbook.qa': ['*.html'],
        'cookienlp.nlpbook.paircls': ['*.html'],
        'cookienlp.nlpbook.generation': ['*.html'],
    },
    install_requires=requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)