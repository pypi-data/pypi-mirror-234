from setuptools import setup, find_packages

setup(
    name='avalanchesumhash20',
    version='0.0.0.4',
    packages=find_packages(),
    install_requires=[
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'ash = avalanchesumhash20.avalanchesumhash20:run',
        ],
    },
)
