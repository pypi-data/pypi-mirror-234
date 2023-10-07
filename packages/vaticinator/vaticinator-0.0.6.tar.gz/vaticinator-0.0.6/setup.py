#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py."""
from __future__ import absolute_import, print_function

# import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read description files."""
    path = join(dirname(__file__), *names)
    with open(path, encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


# previous approach used to ignored badges in PyPI long description
# long_description = '{}\n{}'.format(
#     re.compile(
#         '^.. start-badges.*^.. end-badges',
#         re.M | re.S,
#         ).sub(
#             '',
#             read('README.rst'),
#             ),
#     re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read(join('docs', 'CHANGELOG.rst')))
#     )

long_description = read('README.rst')


setup(
    name='vaticinator',
    version='0.0.6',
    description='Yet another Python fortune implementation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Matt Barry',
    author_email='matt@hazelmollusk.org',
    url='https://github.com/hazelmollusk/vaticinator',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.11',
        'Topic :: Games/Entertainment :: Fortune Cookies',
        ],
    project_urls={
        'webpage': 'https://github.com/hazelmollusk/vaticinator',
        'Documentation': 'https://vaticinator.readthedocs.io/en/latest/',
        'Changelog': 'https://github.com/hazelmollusk/vaticinator/blob/main/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/hazelmollusk/vaticinator/issues',
        'Discussion Forum': 'https://github.com/hazelmollusk/vaticinator/discussions',
        },
    keywords=[
        'fortune', 'games'
        ],
    python_requires='>=3.11, <4',
    install_requires=[
        # https://stackoverflow.com/questions/14399534
        ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
        },
    setup_requires=[
        #   'pytest-runner',
        #   'setuptools_scm>=3.3.1',
        ],
    entry_points={
        'console_scripts': [
            'vaticinator = vaticinator.cli:main'
            ]
        },
    # cmdclass={'build_ext': optional_build_ext},
    # ext_modules=[
    #    Extension(
    #        splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
    #        sources=[path],
    #        include_dirs=[dirname(path)]
    #    )
    #    for root, _, _ in os.walk('src')
    #    for path in glob(join(root, '*.c'))
    # ],
    )
