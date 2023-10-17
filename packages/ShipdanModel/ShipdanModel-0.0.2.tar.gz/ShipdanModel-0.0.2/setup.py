from setuptools import setup, find_packages

setup(
    name='ShipdanModel',
    version='0.0.2',
    description='app_model package for shipdan business written by Bunkerkids Tech',
    author='bunkerkids',
    author_email='development@bunkerkids.net',
    url='https://github.com/bunkerkids/shipdan_model',
    install_requires=['django',],
    packages=find_packages(exclude=['shipdan_model.shipdan_model', 'shipdan_model.shipdan_apps']),
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
