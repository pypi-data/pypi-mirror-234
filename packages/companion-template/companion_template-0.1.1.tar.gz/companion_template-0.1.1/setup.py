from setuptools import setup, find_packages

setup(
    name='companion_template',
    version='0.1.1',
    packages=find_packages(include=['.', './*']),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
    install_requires=[
        'toml',
    ],
)
