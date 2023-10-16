from setuptools import setup, find_packages

setup(
    name='PivotPal',
    version='0.0.5',  
    packages=find_packages(),
    description='A collection of utility functions for data analysis with pandas.',
    long_description_content_type="text/markdown", 
    author='Kyle Grattan',
    author_email='ktgcreative@gmail.com',
    url='https://github.com/ktgcreative/pivotpal',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'pandas', 
        'IPython' 
        
    ],
)
