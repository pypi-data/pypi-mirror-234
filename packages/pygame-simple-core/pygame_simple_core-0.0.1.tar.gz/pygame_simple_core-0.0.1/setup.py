from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    readme = file.read()

setup(
    name='pygame_simple_core',
    version='0.0.1',
    license='MIT license',
    author='Vinicius Putti Morais',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='viniputtim@gmail.com',
    keywords='pygame',
    description='An simple core class for pygame.',
    packages=find_packages(),
    install_requires=['pygame']
)
