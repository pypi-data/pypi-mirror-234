from setuptools import setup, find_packages

setup(
    name='f-ck',
    version='0.0.7',
    license='Apache 2.0',
    author='Zeio Nara',
    author_email='zeionara@gmail.com',
    packages=find_packages(),
    package_data={'*': ['foo.txt']},
    description='A tiny program for uncensoring russian texts',
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
    install_requires = ['pymorphy3', 'tqdm']
)
