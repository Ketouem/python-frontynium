from distutils.core import setup

setup(
    name='python-frontynium',
    version='0.1.0',
    author='Cyril Thomas',
    author_email='ketouem@example.com',
    packages=['frontynium'],
    license='LICENSE',
    description='Useful towel-related stuff.',
    long_description=open('README.md').read(),
    install_requires=["selenium"],
)