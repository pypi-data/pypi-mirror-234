from setuptools import setup

setup(
    name='companion_template',
    version='0.1.2',
    packages=["template_engine"],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
    install_requires=[
        'toml',
    ],
)
