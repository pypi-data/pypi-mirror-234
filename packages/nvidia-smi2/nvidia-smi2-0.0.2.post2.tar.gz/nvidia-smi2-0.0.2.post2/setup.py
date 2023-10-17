from setuptools import setup, find_packages

setup(
    name='nvidia-smi2',
    version='0.0.2-2',
    install_requires=[
        'termcolor',
    ],
    scripts=[
        'bin/nvidia-smi2'
    ],
    packages=find_packages(),
    include_package_data=True,
)