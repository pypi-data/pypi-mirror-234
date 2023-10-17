from setuptools import setup, find_packages

setup(
    name='saft',
    version='0.7',
    packages=['saft'],
    install_requires=[
        'torch',
        'torchvision',
        'timm',
        'avalanche-lib'
    ],
)
