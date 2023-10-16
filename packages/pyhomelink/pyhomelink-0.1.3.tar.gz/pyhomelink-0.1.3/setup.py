"""Setup skyq_hub package."""
from setuptools import setup, find_namespace_packages
from pyhomelink.version import __version__ as version
from os import path

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Home Automation',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.11',
    'Operating System :: OS Independent',
]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyhomelink',
    version=version,
    author='Roger Selwyn',
    author_email='roger.selwyn@users.noreply.github.com',
    classifiers=CLASSIFIERS,
    description='Library for AICO HomeLINK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    maintainer='RogerSelwyn',
    maintainer_email='roger.selwyn@users.noreply.github.com',
    url='https://github.com/RogerSelwyn/python_homelink',
    license='MIT',
    packages=find_namespace_packages(exclude=['tests','manage']),
    install_requires=['aiohttp>=3.8.5'],
    keywords='AICO HomeLINK',
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.11',
    setup_requires=["wheel"]
)
