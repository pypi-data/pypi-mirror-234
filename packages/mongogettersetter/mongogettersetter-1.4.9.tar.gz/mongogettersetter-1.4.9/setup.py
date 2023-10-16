from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    
setup(
    name='mongogettersetter',
    version='1.4.9',
    author='Sibidharan',
    author_email='sibi@selfmade.ninja',
    description='A clean way to handle MongoDB documents in Pythonic way',
    packages=find_packages(),
    url='https://git.selfmade.ninja/sibidharan/pymongogettersetter',
    install_requires=['pymongo'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    license="MIT",
    keywords="pymongo mongodb mongo mongogettersetter gettersetter getter setter",
)
