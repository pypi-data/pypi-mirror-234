import setuptools

setuptools.setup(
    name = 'qsvin', 
    packages = ['qsvin'],
    version='0.0.10',
    author='Yaroslav Mavliutov',
    author_email='yaroslavm@questarauto.com',
    description = 'Package provides functionality for decoding vin data',
    url='https://github.com/saferide-tech/QuestarVin',
    license='MIT',
    keywords = ['vin'],
    install_requires=[
        'databricks-sql-connector',
        'requests',
        'vininfo',
        'openpyxl'
      ],
)