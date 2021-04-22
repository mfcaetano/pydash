from setuptools import setup, find_packages

setup(
    name='pydash',
    packages=find_packages(),
    url='https://github.abc.com/abc/myabc',
    description='A Framework Based Educational Tool for Adaptive Streaming Video Algorithms Study',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy==1.20.2",
        "matplotlib==3.4.1",
        "scipy==1.6.2",
        "seaborn==0.11.1"
        ],
)
