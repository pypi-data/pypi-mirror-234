from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

install_requires = [line for line in lines if line and not line.startswith('#')]

name = 'echobox'
version = '1.5.31'
author = 'kiuber'
author_email = 'kiuber.zhang@gmail.com'

setup(
    name=name,
    version=version,
    keywords=(name),
    description=name,
    license='',
    install_requires=install_requires,

    scripts=[],

    author=author,
    author_email=author_email,
    url='',

    packages=find_packages(),
    platforms='any',
)
