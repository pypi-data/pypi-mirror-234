#setup.py The packaging script that specifies how your CLI should be distributed.
from setuptools import setup, find_packages

setup(
    name='briefnewscli',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'typer',  # Add any other dependencies your CLI uses
        'python-decouple',
        'requests',
        'typer',
        'torch',
        'transformers'
    ],
    entry_points='''
        [console_scripts]
        briefnewscli=briefnewscli.cli:app
    ''',
)

# Package Your CLI
# python setup.py sdist bdist_wheel

# Upload to PyPI:
# pip install twine
# twine upload dist/* --verbose

# Installation by Users:v
# pip install briefnewscli
