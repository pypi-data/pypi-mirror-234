from codecs import (
    open,
)
from os import (
    path,
)

from setuptools import (
    find_packages,
    setup,
)


__version__ = '0.3.6'


here = path.abspath(path.dirname(__file__))

# Получение полного описание из README.md
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'CHANGES.md'), encoding='utf-8') as f:
    long_description += f.read()

# Получение зависимостей
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [
    x.strip()
    for x in all_reqs if
    'git+' not in x
]
dependency_links = [
    x.strip().replace('git+', '')
    for x in all_reqs if
    x.startswith('git+')
]

excluded_packages = (
    'docs',
)


setup(
    name='m3_db_utils',
    version=__version__,
    description='m3_db_utils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Alexander Danilenko',
    author_email='a.danilenko@bars.group',
    url='https://stash.bars-open.ru/projects/M3/repos/m3_db_utils/browse',
    download_url='http://nexus.budg.bars.group/#browse/browse:pypi-bars-private:m3-db-utils',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
    ],
    platforms=['Any'],
    packages=find_packages(exclude=excluded_packages),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    zip_safe=False,
)
