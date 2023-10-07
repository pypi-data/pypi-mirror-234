import setuptools

from powerbot_client import __version__

setuptools.setup(
    name='powerbot_client',
    version=__version__,
    description='PowerBot client for sync operations',
    author="PowerBot GmbH",
    author_email="support@powerbot-trading.com",
    packages=['powerbot_client'],
    package_data={'powerbot_client': ['api/*', 'models/*']},
    python_requires='>=3.9',
    zip_safe=True,
    install_requires=['certifi', 'python-dateutil', 'urllib3', 'six']
)
