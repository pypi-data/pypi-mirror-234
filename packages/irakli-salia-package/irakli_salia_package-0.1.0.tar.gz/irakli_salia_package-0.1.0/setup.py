from setuptools import setup, find_packages

setup(
    name='irakli_salia_package',
    version='0.1.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package example',
    long_description=open('README.md').read(),
    install_requires=['numpy'], # add your dependencies
    author='Irakli Salia',
    author_email='irakli.salia854@gmail.com'
)