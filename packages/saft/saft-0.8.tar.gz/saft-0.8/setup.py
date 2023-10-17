from setuptools import setup, find_packages

setup(
    name='saft',
    version='0.8',
    packages=['saft', 'saft.utils'],
    install_requires=[
        'torch',
        'torchvision',
        'timm',
        'avalanche-lib'
    ],
)
