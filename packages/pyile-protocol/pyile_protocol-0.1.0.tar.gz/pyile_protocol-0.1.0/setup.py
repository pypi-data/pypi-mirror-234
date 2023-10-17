from setuptools import setup, find_packages

setup(
    name='pyile_protocol',
    version='0.1.0',
    description='Protocol library for p2p messaging and authentication.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Noah Burnette',
    author_email='nburnet1@duck.com',
    packages=find_packages(),
    install_requires=[
        "pyile_protocol",
    ],
    url='https://github.com/nburnet1/pyile-protocol'
)
