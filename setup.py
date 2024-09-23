from setuptools import setup, find_packages

setup(
    name='termipy',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # NA
    ],
    entry_points={
        'console_scripts': [
            'termipy = termipy.main:main',
        ],
    },
)
