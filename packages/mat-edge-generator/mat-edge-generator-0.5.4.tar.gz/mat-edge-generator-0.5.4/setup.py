from setuptools import setup, find_packages

setup(
    name='mat-edge-generator',
    version='0.5.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pyyaml"
    ],
    author='Filippo Ghelfi',
    author_email='f.ghelfi@40-factory.com',
    description='This library is used for creating a MAT edge starting from a simple configuration file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
