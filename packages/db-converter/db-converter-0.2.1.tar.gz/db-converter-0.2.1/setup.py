from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.1'
DESCRIPTION = 'Data migration. MongoDB to MySQL - MySQL to MongoDB'
#LONG_DESCRIPTION = 'A package that allows to migrate your data.'

# Setting up
setup(
    name="db-converter",
    version=VERSION,
    author="dilsizyazilimci (Mert Celikan)",
    author_email="celikanmert@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[  # Gerekli bağımlılıklar
        'numpy',
        'pandas',
        'pymongo',
        'PyMySQL',
        'python-dateutil',
        'pytz',
        'six',
        'dnspython'
    ],
    keywords=['python', 'mongodb', 'mysql', 'database', 'MySQL to MongoDB', 'MongoDB to MySQL', 'data migration'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)