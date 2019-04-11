from setuptools import setup, find_packages

PACKAGENAME='pyrsa'

setup(
    name=PACKAGENAME,
    version='0.1.0',
    description='Simple RSA Decrypter for n up to 100,000',
    author='Joshua Alexander',
    author_email='itzjoshy8@gmail.com',
    url='',
    install_requires = [
    ],
    packages=find_packages(),
    test_suite='tests',
    tests_require=['pytest'],
)
