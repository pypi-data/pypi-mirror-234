# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

#from sphinx.setup_command import BuildDoc
#commands["build_sphinx"] = BuildDoc


with open("README.md", "rt", encoding='UTF8') as fh:
    long_description = fh.read()
setup(
    name='xython',
    version='1.14.1',
    url='https://github.com/sjpark/xython',
    download_url='https://github.com/sjpark/xython/archive/v1.14.1.tar.gz',
    author='sjpark',
    author_email='sjpkorea@yahoo.com',
    description='Functional Programming for Excel, Word, Outlook, Color, Etc with Python',
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "xython": ["*.*"],
        },
    long_description_content_type="text/markdown",
    long_description=open('README.md', "r", encoding='UTF8').read(),
    install_requires=[''],
    python_requires='>=3.8',
    zip_safe=False,
    classifiers=['License :: OSI Approved :: MIT License'],
    project_urls = {
      'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
      'Link 1': 'https://xython.co.kr',
      'Link 2': 'https://halmoney.com'
    }
    )

