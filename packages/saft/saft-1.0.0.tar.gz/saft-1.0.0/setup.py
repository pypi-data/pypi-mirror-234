from setuptools import setup, find_packages

setup(
    name='saft',
    version='1.0.0',
    packages=['saft'],
    install_requires=[
        'torch',
        'torchvision',
        'timm',
        'avalanche-lib'
    ],
)
