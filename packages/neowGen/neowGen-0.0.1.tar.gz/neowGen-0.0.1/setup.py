import numpy
from setuptools import setup
import tqdm
with open('README.md', 'r') as f:
    l_description = f.read()
setup(
    name='neowGen',
    version='0.0.1',
    description='A HuggingFace LLM pipeline generator',
    package_dir={'': 'src'},
    py_modules=['neowGen'],   
    long_description = l_description,
    long_description_content_type ='text/markdown',
    url='https://github.com/pechaut78/neowGen',
    install_requires = [
            'pandas',
            'tqdm',
            'numpy',
            'huggingface_hub',
            'datasets'
    ],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author='Pierre-Emmanuel CHAUT',
    author_email='pe_chaut@hotmail.com'
)

