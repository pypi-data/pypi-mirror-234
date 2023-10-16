from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="sharingiscaring",
    version="0.3.18",
    author="Sander de Ruiter",
    author_email="sdr@concordium-explorer.nl",
    description="Shared code for Concordium Explorer (Bot)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sderuiter/sharingiscaring",
    project_urls={},
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "rich",
        "python-dateutil",
        "base58",
        "eth-hash",
        "pycryptodome",
        "pytest",
        "leb128",
        "pydantic",
        "pymongo",
        "motor",
        "requests",
        "apprise",
        "py-graphql-client",
        "chardet",
    ],
)
