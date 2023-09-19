from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    readme = f.read()

    setup(
        name='ocds-reader',
        version='0.0.1',
        description='Command line OCDS reader util',
        long_description=readme,
        author='Harry Carpio S.',
        author_email='harry@ojo-seco.co',
        packages=find_packages('src'),
        package_data={'': ['*'],},
        package_dir={'': 'src'},
        install_requires=[
            "pymongo==4.4.0",
            "Requests==2.31.0",
            "setuptools==68.0.0",
            "psycopg2-binary==2.9.7"
        ],
        entry_points={
            'console_scripts': 'ocds-reader=ocds_reader.cli:main',
        },
    )