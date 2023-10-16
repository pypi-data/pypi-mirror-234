from setuptools import setup, find_packages

setup(
    name="cosmicfrog",
    
    include_package_data=True,

    version="0.3.16",
    description='Helpful utilities for working with Cosmic Frog models',
    url='https://cosmicfrog.com',
    author='Optilogic',
    packages=['cosmicfrog'],
    package_data={
        'cosmicfrog': ['anura/table_definitions/*.json',
                        'anura/table_masterlists/*.json'
                       ],
    },
    license='MIT',
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=2.0.0',
        'psycopg2-binary>=2.9.6',
        'sqlalchemy',
        'opencensus-ext-azure>=1.1.7',
        'openpyxl',
        'optilogic>=2.5',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
