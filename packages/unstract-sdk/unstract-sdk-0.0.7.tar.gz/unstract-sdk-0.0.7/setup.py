import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="unstract-sdk",
    # The version of the unstract-sdk package is used at runtime to validate manifests. That validation must be
    # updated if our semver format changes such as using release candidate versions.
    version="0.0.7",
    description="A framework for writing Unstract Tools/Apps",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://unstract.com/sdk",
    author="Zipstack Inc",
    author_email="devsupport@zipstack.com",
    license="MIT",
    packages=["unstract_sdk"],
    include_package_data=True,
    install_requires=["llama-index~=0.8", "openai~=0.27", "tiktoken~=0.4.0"],
    classifiers=[
        # This information is used when browsing on PyPi.
        # Dev Status
        "Development Status :: 3 - Alpha",
        # Project Audience
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        # Python Version Support
        "Programming Language :: Python :: 3.9",
    ],
    keywords="unstract tools-development-kit apps -development-kit sdk",
    python_requires="<=3.11",
    scripts=["bin/unstract-tool-gen"],
)
