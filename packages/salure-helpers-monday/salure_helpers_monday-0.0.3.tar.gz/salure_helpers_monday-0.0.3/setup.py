from setuptools import setup

setup(
    name='salure_helpers_monday',
    version='0.0.3',
    description='Monday.com wrapper from Salure',
    long_description='Monday.com wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.monday"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1'
    ],
    zip_safe=False,
)
