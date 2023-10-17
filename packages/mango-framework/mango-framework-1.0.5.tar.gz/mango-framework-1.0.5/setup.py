from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='mango-framework',
    version='1.0.5',
    author='Mohammed',
    author_email='fdlnaal@gmail.com',
    description='A lightweight and highly customizable Python framework for building web applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/momo-AUX1/mango',
    packages=['.'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
