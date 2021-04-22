from setuptools import setup, find_packages

setup(
    name='pydash',
    packages=find_packages(),
    url='https://github.com/mfcaetano/pydash',
    description='A Framework Based Educational Tool for Adaptive Streaming Video Algorithms Study',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "seaborn"
        ],
)
