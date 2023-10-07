
from setuptools import setup, find_packages
from pcli.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='periancli',
    version=VERSION,
    description='Perian Sky Job Platform CLI',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Perian',
    author_email='info@perian.io',
    url='https://perian.io',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'pcli': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        perian = pcli.main:main
    """,
    install_requires=[
        "cement==3.0.8",
        "jinja2==3.1.2",
        "pyyaml==6.0.1",
        "colorlog==6.7.0",
        "rich==13.4.2",
        "perian==0.1.20",
    ]
)
