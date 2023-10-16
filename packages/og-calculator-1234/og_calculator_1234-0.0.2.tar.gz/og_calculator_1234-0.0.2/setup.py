from setuptools import setup, find_packages

setup(
    name='og_calculator_1234',
    version='0.0.2',

    packages=find_packages(),

    # Metadata
    author='Oliver',
    description='A calculator with +, -, *, /, nth root operaters',
    url='https://github.com/your-username/your-repository',
    license='MIT',

    # Dependencies
    install_requires=[
        # List your package dependencies here
        'pip',
    ],

    # Entry points
    entry_points={
        'console_scripts': [
            'calculator = CALCULATOR_PACKAGE.calculator:main',
        ],
    },

    # Other configurations
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)