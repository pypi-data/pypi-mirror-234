import os

from setuptools import find_packages, setup

if __name__ == '__main__':
    setup(
        name='google-sheet-tables',
        version=os.getenv('PACKAGE_VERSION', '0.0.dev4'),
        package_dir={'': 'src'},
        packages=find_packages(
            'src', include=[
                'google_sheet_tables*'
            ]
        ),
        description="Библиотека для работы с гугл таблицами.",
        install_requires=[
            "gspread",
        ]
    )
