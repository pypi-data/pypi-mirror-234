import setuptools

from powerbot_asyncio_client import __version__

setuptools.setup(
    name='powerbot_asyncio_client',
    version=__version__,
    description='PowerBot client for async operations',
    author="PowerBot GmbH",
    author_email="support@powerbot-trading.com",
    packages=['powerbot_asyncio_client'],
    package_data={'powerbot_asyncio_client': ['api/*', 'models/*']},
    python_requires='>=3.9',
    zip_safe=True,
    install_requires=['certifi', 'python-dateutil', 'aiohttp', 'urllib3', 'six']
)
