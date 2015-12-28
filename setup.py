from setuptools import setup, find_packages

setup(
    name='userlayers',
    version='1.0.0',
    packages=find_packages(),
    long_description=open('README.md').read(),
    install_requires=[
        'django-mutant == 0.2.0a',
        'django-tastypie >= 0.12.0',
        'transliterate == 1.7.3',
        'vectortools == 0.0.4',
        'shapeutils == 0.0.1',
    ],
    dependency_links = [
        'https://github.com/charettes/django-mutant/archive/83a09a6.zip#egg=django-mutant-0.2.0a',
        'https://bitbucket.org/lighter/shape-utils/get/eec0952.zip#egg=shapeutils-0.0.1',
    ],
)
