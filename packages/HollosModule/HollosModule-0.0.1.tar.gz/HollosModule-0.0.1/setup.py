from setuptools import setup, find_packages

setup(
    name="HollosModule",
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'sty',
        'colorama',
        'requests',
    ],
    author='Hollo',
    author_email='hollo1234567890e@gmail.com',
    description='A collection of tools for various purposes.',
    url='https://github.com/Developer-Hollo/HollosModule',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)