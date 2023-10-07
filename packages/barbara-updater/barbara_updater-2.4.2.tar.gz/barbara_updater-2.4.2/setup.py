from setuptools import setup

version_number = input("Input the new version number you are going to use: ")

setup(
    name='barbara_updater',
    version=version_number,
    author='santod',
    description='weather observer',
    py_modules=['barbara', 'launch_and_type']  # List of your Python files
)