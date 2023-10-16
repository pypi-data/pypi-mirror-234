from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'qtc/version.py'), 'r') as f:
    exec(f.read())


setup(
    name='qtc',
    version=__version__,
    url='',
    license='',
    author='Andrew Hu',
    author_email='AndrewWeiHu@gmail.com',
    description='Quant Trading',
    packages=find_packages(exclude=['backup']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'pandas>=1.4.3',
        'joblib',
        'sqlalchemy',
        # 'pymssql',
        'psycopg2',
        'pyarrow',
        'datatable',
        'pyyaml',
    ],
    tests_require=[
        'pytest'
    ],
)
