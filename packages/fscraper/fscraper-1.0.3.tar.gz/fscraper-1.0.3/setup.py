from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='fscraper',
    version='1.0.3',
    description='Financial Data Web Scraper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='er-ri',
    author_email='724chen@gmail.com',
    url='https://github.com/er-ri/fscraper',
    packages=['fscraper'],
    classifiers=[
        "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
    install_requires=[
        'pandas>=1.5.2',
        'numpy>=1.23.5',
        'requests>=2.28.1',
        'beautifulsoup4>=4.12.2',
        'lxml>=4.9.2',
    ],
)
