from setuptools import setup

setup(
    name='geneplore_bare_api',
    version='3.3.0',
    install_requires=[
        'requests',
        'pandas',
        'tiktoken',
        'google-api-python-client',
        'google-api-core',
        'python-dotenv'
    ],
)