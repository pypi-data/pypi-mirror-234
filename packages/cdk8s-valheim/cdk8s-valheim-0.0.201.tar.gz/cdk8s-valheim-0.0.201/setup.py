import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-valheim",
    "version": "0.0.201",
    "description": "A package that vends a Valheim server chart.",
    "license": "Apache-2.0",
    "url": "https://github.com/awlsring/cdk8s-valheim.git",
    "long_description_content_type": "text/markdown",
    "author": "awlsring<mattcanemail@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awlsring/cdk8s-valheim.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_valheim",
        "cdk8s_valheim._jsii"
    ],
    "package_data": {
        "cdk8s_valheim._jsii": [
            "cdk8s-valheim@0.0.201.jsii.tgz"
        ],
        "cdk8s_valheim": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdk8s-plus-26==2.2.2",
        "cdk8s>=2.7.36, <3.0.0",
        "constructs>=10.1.281, <11.0.0",
        "jsii>=1.90.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
