from setuptools import setup, find_packages

setup(
    name='sybil-engine',
    version='0.1.8',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='Arsenii Venherak',
    author_email='indeooars@gmail.com',
    description='A brief description of your package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Indeoo/sybil-engine',
)