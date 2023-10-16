from setuptools import setup, find_packages

setup(
    name='drymerge',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Samuel Brashears',
    author_email='sam@drymerge.com',
    description='DryMerge Client SDK.',
)

