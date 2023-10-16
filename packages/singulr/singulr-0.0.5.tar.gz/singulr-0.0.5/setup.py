# Created by msinghal at 04/10/23
from setuptools import setup, find_packages

setup(
    name='singulr',
    version='0.0.5',
    description='Package to trace generative apps and guard them',
    url='',
    author='Abhijit Sharma',
    author_email='abhijit@singulr.com',
    license='MIT',  # Choose an appropriate license

    # Specify the packages to include
    packages=find_packages(),

    # Define package dependencies
    install_requires=[
        'langchain'
        # List your dependencies here
    ],
)