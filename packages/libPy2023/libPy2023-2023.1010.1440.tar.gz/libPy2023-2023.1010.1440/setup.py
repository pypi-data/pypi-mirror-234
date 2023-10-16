# setup.py
"""
Para compilar y subir usar en el Terminal:

        python3 -m pip install --upgrade setuptools wheel twine

luego cada vez que se actualice ...:

            rm -f dist/*.* && \
            python setup.py sdist bdist_wheel &&\
            python -m twine upload dist/* --user Dexsys --password Isijoa827@

o mejor aun correr en BASH :

            sh update.sh

para instalar usar:

pip3 install libPy2023 --upgrade

El Proyecto esta en
        https://pypi.org/manage/projects/
        https://github.com/Dexsys

"""

import setuptools
#import config
import libPy2023

with open('README.md','r',encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='libPy2023',
    version=libPy2023.__version__,
    author='Ludwig R. Corales Marti',
    author_email='dexsys@gmail.com',
    description='Librerías de propósito General',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Dexsys/libPy2023',
    #packages=setuptools.find_packages(exclude=['sphinx_docs', 'docs', 'tests']),
    python_requires='~=3.5',
    install_requires=[
        i.replace('\n', '')
        for i in open('requirements.txt', 'r').readlines()
    ],
    extras_require={
        'dev': ['setuptools', 'wheel', 'twine', 'Sphinx'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development',
        'License :: Free for non-commercial use',
        'Operating System :: OS Independent',
        'Natural Language :: Spanish'
    ],
)