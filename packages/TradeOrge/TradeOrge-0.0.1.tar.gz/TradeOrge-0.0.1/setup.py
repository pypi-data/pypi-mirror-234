from setuptools import setup, find_packages

setup(
    name='TradeOrge',
    version='0.0.1',
    author='NullRien',
    author_email='me@nullrien.com',
    description='A API wrapper for tradeorge',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)