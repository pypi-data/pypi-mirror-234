from setuptools import setup, find_packages
from pathlib import Path


setup(
    name="Webscreaper-Chrome-Blaze",
    version=1.1,
    description="Este pacote loga no site da blazer e varre realizando um screaper limpo e sem trabalho algum do double",
    long_description=Path("README.md").read_text(),
    author="Auto Dev",
    author_email="ramonma31@gmail.com",
    keywords=["blaze", "casino", "webscreaper", "selenium", "sala de sinais"],
    packages=find_packages(),
)
