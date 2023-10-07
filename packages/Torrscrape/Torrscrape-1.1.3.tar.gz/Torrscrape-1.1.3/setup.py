from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
Long_description = (this_directory / "README.md").read_text()
setup(
    author="Tanish",
    author_email="sharmatanish097654@gmail.com",
    description="Torrscraper is a command line tool to search and download torrents from the command line.",
    long_description_content_type='text/markdown',
    long_description=Long_description,
    name="Torrscrape",
    version="1.1.3",
    packages=find_packages(),
    install_requires=[
        "requests",
        "qbittorrent-api",
        "pandas",
        "tabulate",
        "click",
        "rich",        
    ],
    keywords=["python","torr","torrent","torrscrape","jackett","Torrscrape"],
    entry_points={
        "console_scripts": [
            "torrscrape=Torrscrape.main:main",
        ],
    },
)
