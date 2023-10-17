from setuptools import setup, find_packages

setup(
    name='saft',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchvision',
        'timm',
        'avalanche-lib'
    ],
)
