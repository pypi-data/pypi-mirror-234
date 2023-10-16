from setuptools import setup

setup(
    name='companion_template',
    version='0.1.4',
    packages=["companion_template"],
    package_dir={'companion_template': 'companion_template'},
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
    install_requires=[
        'toml',
    ],
)
