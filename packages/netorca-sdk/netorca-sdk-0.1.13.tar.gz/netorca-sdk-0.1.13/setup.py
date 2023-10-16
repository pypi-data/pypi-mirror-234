from distutils.core import setup

setup(
    name="netorca-sdk",
    packages=["netorca_sdk"],
    version="0.1.13",
    license="MIT",
    description="A package for interacting with the NetOrca API",
    long_description=open("README.rst").read(),
    author="Scott Rowlandson",
    author_email="scott@netautomate.org",
    url="https://gitlab.com/netorca_public/netorca_sdk/",
    keywords=["netorca", "orchestration", "netautomate"],
    install_requires=[
        "beautifultable",
        "pyyaml",
        "requests",
        "gitpython",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
