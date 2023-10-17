from setuptools import setup, find_packages

VERSION = '1.0.10'
DESCRIPTION = 'Shared support functions'
LONG_DESCRIPTION = 'Shared support functions'

setup(
    name="afgutils",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Araz Heydarov",
    author_email="araz.heydarov@asiafinancegroup.com",
    python_requires='>=3.10',
    license='copyright',
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'pyodbc==4.0.39',
        'pywin32==306',
        'python-dotenv==1.0.0',
        'boto3==1.27.0',
        'pandas==2.0.3']
)
