import datetime

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def generate_version():
    now = datetime.datetime.now()
    return now.strftime('%y.%m.%d.%H')


setuptools.setup(
    name="codefast",
    version=generate_version(),
    author="Tommy",
    author_email="i@pm.me",
    description="A package for faster coding.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=[
        'colorlog', 'lxml', 'requests', 'tqdm', 'smart-open', 'bs4', 'arrow',
        'termcolor', 'pydub', 'pycryptodome', 'requests-toolbelt'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
