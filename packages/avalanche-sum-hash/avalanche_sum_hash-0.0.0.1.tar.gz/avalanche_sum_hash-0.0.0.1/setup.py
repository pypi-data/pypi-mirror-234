from setuptools import setup, find_packages

setup(
    name='avalanche_sum_hash',
    version='0.0.0.1',
    packages=find_packages(),
    install_requires=[
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'avalanche_sum_hash_cli=avalanche_sum_hash.avalanche_sum_hash:main',
        ],
    },
)
