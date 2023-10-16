from setuptools import setup, find_packages
from sklearn.base import ClassifierMixin

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
]

setup(
    name='pysili',
    version='0.0.3',
    description='Basic utlilitis for scRNA',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://www.metapriyansh.com/',
    author='Priyansh Srivastava',
    author_email='spriyansh29@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='single-cell',
    packages=find_packages(),
    install_requires=[''] 
)