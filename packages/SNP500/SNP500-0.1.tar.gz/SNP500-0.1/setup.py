from setuptools import setup

setup(
    name='SNP500',
    version='0.1',
    py_modules=['snp500'],
    install_requires=[
        'pandas'
    ],
    author='Aung Si',
    author_email='aungsi.as99@gmail.com',
    description='Fetch S&P 500 tickers from Wikipedia'
)
