from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='capbypasswrapped',
    version='0.1.2',
    packages=['CapBypassWrapped'],
    install_requires=[
        'requests',
        'logging'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',

)