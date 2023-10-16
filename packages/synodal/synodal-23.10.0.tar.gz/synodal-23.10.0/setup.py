from setuptools import setup
from pathlib import Path

SETUP_INFO = dict(
    name='synodal',
    version='23.10.0',
    install_requires=[],
    # scripts=['synodal.py'],
    py_modules=['synodal'],
    description="Metadata about the Synodalsoft project",
    license="GNU Affero General Public License v3",
    license_files=['COPYING'],
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org')

SETUP_INFO.update(classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU Affero General Public License v3
Natural Language :: English
Operating System :: OS Independent""".splitlines())

# SETUP_INFO.update(long_description=__doc__.strip())
readme = (Path(__name__).parent / "README.rst").absolute()
SETUP_INFO.update(long_description=readme.read_text())

if __name__ == '__main__':
    setup(**SETUP_INFO)
