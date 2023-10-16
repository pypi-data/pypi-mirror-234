from setuptools import setup, find_packages

setup(
    name="reach_commons",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "requests==2.31.0"
    ],
    author="Wilson Moraes",
    author_email="wmoraes@getreach.ai",
    description="Uma descrição curta da sua biblioteca",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
