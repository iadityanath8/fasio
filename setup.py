from setuptools import setup, find_packages

setup(
    name='fasio',
    version='0.2.0', 
    author='Nemesis',
    author_email='iadityanath8@gmail.com',
    description='A fast asynchronous coroutine executor for asynchronous programming and fast I/O.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iadityanath8/Fasio',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
    install_requires=[

    ],
)
