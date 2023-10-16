from setuptools import setup, find_packages

setup(
    name='coin-infra',
    version='4.1.1',
    description='infra of coin projects',
    author='Yi Te',
    author_email='coastq22889@icloud.com',
    packages=['general'],
    install_requires=[
        'pymongo',
        'redis',
        'requests',
        'websockets',
        'binance-futures-connector',
        'python-okx',
        'influxdb-client'
    ],
)


