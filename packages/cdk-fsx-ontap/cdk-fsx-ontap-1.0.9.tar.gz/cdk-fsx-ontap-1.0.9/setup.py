import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-fsx-ontap",
    "version": "1.0.9",
    "description": "CDK construct for Amazon FSx for Netapp ONTAP",
    "license": "MIT",
    "url": "https://rafalkrol.xyz",
    "long_description_content_type": "text/markdown",
    "author": "Rafal Krol<ameotoko1+github@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/rafalkrol-xyz/cdk-fsx-ontap"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_fsx_ontap",
        "cdk_fsx_ontap._jsii"
    ],
    "package_data": {
        "cdk_fsx_ontap._jsii": [
            "cdk-fsx-ontap@1.0.9.jsii.tgz"
        ],
        "cdk_fsx_ontap": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.85.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.89.0, <2.0.0",
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
