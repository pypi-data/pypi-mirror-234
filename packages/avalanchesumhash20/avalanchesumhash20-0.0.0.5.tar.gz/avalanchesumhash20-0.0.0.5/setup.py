from setuptools import setup, find_packages

setup(
    name='avalanchesumhash20',
    version='0.0.0.5',
    packages=find_packages(),
    install_requires=[
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'ash=avalanchesumhash20.avalanchesumhash20:run',
        ],
    },
    author='Joshua Dean Pond',
    author_email='joshua.pond11@gmail.com',
    description='ASH-20 Hashfunktion',
    license='MIT',
)
