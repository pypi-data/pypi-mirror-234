from setuptools import setup, find_packages

setup(
    name='redapyx',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'selenium==4.12','rarfile==4.1','requests==2.31'
    ],
)