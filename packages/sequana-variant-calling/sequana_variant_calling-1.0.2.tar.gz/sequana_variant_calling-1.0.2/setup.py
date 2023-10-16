# License: 3-clause BSD
from setuptools import setup, find_namespace_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

_MAJOR               = 1
_MINOR               = 0
_MICRO               = 2

version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {"main": ("cokelaer", "thomas.cokelaer@pasteur.fr")},
    'version': version,
    'license' : 'new BSD',
    'url' : "http://github.com/sequana/",
    'description': "A variant calling pipeline to analyse sequencing Illumina data" ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ['snakemake', "sequana", "NGS", "freebayes", "variant calling"],
    'classifiers' : [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics']
    }

NAME = "variant_calling"


setup(
    name             = "sequana_{}".format(NAME),
    version          = version,
    maintainer       = metainfo['authors']['main'][0],
    maintainer_email = metainfo['authors']['main'][1],
    author           = metainfo['authors']['main'][0],
    author_email     = metainfo['authors']['main'][1],
    long_description = open("README.rst").read(),
    keywords         = metainfo['keywords'],
    description      = metainfo['description'],
    license          = metainfo['license'],
    long_description_content_type = "text/x-rst",
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    packages = ["sequana_pipelines.variant_calling"],

    install_requires = open("requirements.txt").read(),
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
            "pytest-xdist",
            "pytest-mock",
            "pytest-timeout",
            "pytest-runner",
            "coveralls",
        ],
    },
    # This is recursive include of data files
    exclude_package_data = {"": ["__pycache__"]},
    package_data = {
        '': ['*.yaml', "*.rules", "*json", "requirements.txt", "*png"],
        'sequana_pipelines.variant_calling.fastqc.data' : ['*.*'], 
        },

    zip_safe=False,

    entry_points = {'console_scripts':[
        'sequana_variant_calling=sequana_pipelines.variant_calling.main:main']
    }

)
