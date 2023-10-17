import os
from setuptools import setup, find_packages

setup(
    name='f-ck',
    version='0.0.11',
    license='Apache 2.0',
    author='Zeio Nara',
    author_email='zeionara@gmail.com',
    packages=find_packages(),
    # package_data={'fuck': ['assets/profane-words.txt']},
    description='A tiny program for uncensoring russian texts',
    # data_files=[('', ['assets/profane-words.txt', 'foo.txt'])],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/zeionara/fuck',
    project_urls={
        'Documentation': 'https://github.com/zeionara/fuck#readme',
        'Bug Reports': 'https://github.com/zeionara/fuck/issues',
        'Source Code': 'https://github.com/zeionara/fuck'
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.11"
    ],
    install_requires = ['pymorphy3', 'tqdm'],

    package_data={
        '': [
            'profane-words.txt'
        ]
    },
    include_package_data=True
)
