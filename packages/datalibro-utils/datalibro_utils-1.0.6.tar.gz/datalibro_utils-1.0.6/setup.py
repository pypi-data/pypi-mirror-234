from setuptools import setup, find_packages

setup(
    name='datalibro_utils',
    version='1.0.6',
    packages=find_packages(),
    install_requires=[
        'tablemaster',
        'pandas'
    ],
    author='DesignLibro',
    author_email='livid.su@gmail.com',
    description='For Datalibro.',
    url='https://github.com/DesignLibro/datalibro_utils'
)