from setuptools import setup

setup(
	name='lastfm',
	version="0.0.1",
	description="a library for easy access to lastfm data for discord bots",
	long_description="...",
	long_description_content_type="text/markdown",
	author="spread1337",
	author_email="neon@flarebot.tech",
	url="https://github.com/spread1337/lastfm",
	packages=['lastfm'],
	install_requires=['aiohttp','discord','orjson'],
	python_requires=">=3.6"
)