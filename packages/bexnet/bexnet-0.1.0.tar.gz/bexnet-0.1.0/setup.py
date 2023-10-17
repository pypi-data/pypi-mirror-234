from setuptools import setup, find_packages

setup(
    name='bexnet',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'typing; python_version < "3.5"'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
