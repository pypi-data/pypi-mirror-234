from setuptools import setup, find_packages

VERSION = "1.8"
DESCRIPTION = "CLI for downloading all gists from a specified user."
with open("README.md", "r") as file:
    LONG_DESCRIPTION = file.read()
AUTHOR = "NecRaul"

setup(
    name="gist_neko",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    author=AUTHOR,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=["python", "gists downloader", "downloader", "gists", "gist-neko", "kuroneko"],
    link="https://github.com/NecRaul/gist-neko",
    project_urls={
            'Documentation': 'https://github.com/NecRaul/gist-neko#readme',
            'Source': 'https://github.com/NecRaul/gist-neko',
        },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP"
    ],
    py_modules=["download", "environment"],
    entry_points={
        "console_scripts": [
            "gist-neko = gist_neko.__init__:main",
        ],
    },
)