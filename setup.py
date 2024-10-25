from setuptools import setup, find_packages

setup(
    name='fasio',
    version='0.1.0',  # Update the version as needed
    author='Your Name',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    description='A fast asynchronous coroutine executor for asynchronous programming and fast I/O.',
    long_description=open('README.md').read(),  # Ensure you have a README.md for a detailed description
    long_description_content_type='text/markdown',
    url='https://github.com/iadityanath8/Fasio',  # Replace with your project's URL
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
    install_requires=[
        # Add your project dependencies here
        # Example: 'requests', 'numpy', etc.
    ],
)
