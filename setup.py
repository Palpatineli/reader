from setuptools import setup, find_packages

setup(
    name='reader',
    version='0.1',
    install_requires=['pandas', 'numpy', 'py-flags', 'pytest'],
    packages=find_packages(),
)
