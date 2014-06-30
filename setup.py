from distutils.core import setup

setup(
    name='python-frontynium',
    version='0.1.0',
    author='Cyril Thomas',
    author_email='ketouem@gmail.com',
    packages=['frontynium'],
    license='LICENSE',
    description='Implementation of the PageObject paradigm to use with selenium-webdriver.',
    long_description=open('README.md').read(),
    install_requires=["selenium"],
)
