from setuptools import setup, find_packages

setup(
    name='utsav',
    version='0.2.5',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'scikit-learn'
    ],
    author='Utsav Lamichhane',
    author_email='utsav.lamichhane@gmail.com',
    description='Created to work with big microbiome data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://www.utsavlamichhane.com',
)
