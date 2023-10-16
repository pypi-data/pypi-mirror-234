from setuptools import setup


setup(
    name='salure_helpers_salureconnect',
    version='1.4.0',
    description='SalureConnect wrapper from Salure',
    long_description='SalureConnect wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.salureconnect"],
    license='Salure License',
    install_requires=[
        'requests>=2,<=3'
    ],
    zip_safe=False,
)
