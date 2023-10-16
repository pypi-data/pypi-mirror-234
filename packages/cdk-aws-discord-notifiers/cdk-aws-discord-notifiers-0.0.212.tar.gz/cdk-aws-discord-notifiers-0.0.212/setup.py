import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-aws-discord-notifiers",
    "version": "0.0.212",
    "description": "A package that vends constructs to notify about AWS resources via discord",
    "license": "Apache-2.0",
    "url": "https://github.com/awlsring/cdk-aws-discord-notifiers.git",
    "long_description_content_type": "text/markdown",
    "author": "awlsring<mattcanemail@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awlsring/cdk-aws-discord-notifiers.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_aws-discord-notifiers",
        "cdk_aws-discord-notifiers._jsii"
    ],
    "package_data": {
        "cdk_aws-discord-notifiers._jsii": [
            "cdk-aws-discord-notifiers@0.0.212.jsii.tgz"
        ],
        "cdk_aws-discord-notifiers": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.55.0, <3.0.0",
        "constructs>=10.1.52, <11.0.0",
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
