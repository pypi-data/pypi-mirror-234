from setuptools import setup, find_packages


VERSION = '0.1.0'
DESCRIPTION = 'A multi wrapper api project'
LONG_DESCRIPTION = 'Multi wrapper with download and search with tags on e621, rule34, gelbooru API'

# Setting up
setup(
    name="MultiWrapperProject",
    version=VERSION,
    author="philou404",
    author_email="<philouerror404@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests >= 2.27.0'],
    keywords=['python', 'wrapper', 'e621', 'furry', 'yiff','hentai','rule34','gelbooru'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)