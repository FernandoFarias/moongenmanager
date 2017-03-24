from setuptools import setup, find_packages

setup(
    name='moongenmanager',
    version='0.1',
    packages=['moongenmanager'],
    install_requires=['Click'],
    include_package_data=True,
    url='',
    entry_points='''
        [console_scripts]
        moongenmanager=moongenmanager:cli
    ''',
    license='Apache 2.0',
    author='Fernando Farias',
    author_email='fernnf@gmail.com',
    description=''
)
