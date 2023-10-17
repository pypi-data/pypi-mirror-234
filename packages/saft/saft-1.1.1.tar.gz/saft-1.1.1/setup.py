from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='saft',
    version='1.1.1',
    packages=['saft'],
    install_requires=[
        'torch',
        'torchvision',
        'timm',
        'avalanche-lib'
    ],
    description='SAFT: Self-Attention Factor-Tuning for Parameter-Efficient Fine-Tuning',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Use 'text/x-rst' for reStructuredText
)
