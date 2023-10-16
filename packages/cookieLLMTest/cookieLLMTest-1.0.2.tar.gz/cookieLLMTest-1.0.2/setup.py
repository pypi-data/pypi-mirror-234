import os
import setuptools


def requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), encoding='utf-8') as f:
        return f.read().splitlines()


setuptools.setup(
    name="cookieLLMTest",
    version="1.0.2",
    license='MIT',
    author="sjang01",
    author_email="sjang01@naver.com",
    description="LLM Processing test",
    long_description=open('README.md').read(),
    url="https://github.com/sjang01/cookieLLMTest",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        'cookieLLMTest.nlpbook.classification': ['*.html'],
        'cookieLLMTest.nlpbook.ner': ['*.html'],
        'cookieLLMTest.nlpbook.qa': ['*.html'],
        'cookieLLMTest.nlpbook.paircls': ['*.html'],
        'cookieLLMTest.nlpbook.generation': ['*.html'],
    },
    install_requires=requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)