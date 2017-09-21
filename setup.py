from setuptools import setup

setup(
    name='reader',
    version='0.1',
    install_requires=['pandas', 'numpy', 'py-flags', 'pytest'],
    packages=['plptn', 'plptn.reader'],
    namespace_packages=['plptn']
)
