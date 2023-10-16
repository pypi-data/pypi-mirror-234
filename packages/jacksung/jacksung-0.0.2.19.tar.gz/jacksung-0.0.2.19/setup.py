from setuptools import setup, find_packages

setup(
    name='jacksung',
    version='0.0.2.19',
    author='Zijiang Song',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'pymysql',
        'pytz',
        'selenium'
    ],
)
