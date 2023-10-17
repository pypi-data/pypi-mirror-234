#!/usr/bin/env python3

from setuptools import setup, find_packages
import versioneer

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

dependencies = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        dependencies.append(line.strip())

setup(
    name='teamconnector',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Provides the default template for creating Python Package.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Singh Lab',
    author_email='singhlab@nygenome.org',
    url='https://github.com/tjsinghlab/connector',
    license='MIT license',
    python_requires='>=3.7',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'tc = connector.cli:main',
            'tcinit = connector.init_conda_env:main'
        ],
    }
)
