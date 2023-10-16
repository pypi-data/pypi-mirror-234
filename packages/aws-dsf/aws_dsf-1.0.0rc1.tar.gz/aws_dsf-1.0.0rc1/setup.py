import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws_dsf",
    "version": "1.0.0.rc1",
    "description": "L3 CDK Constructs used to build data solutions with AWS",
    "license": "MIT-0",
    "url": "https://awslabs.github.io/aws-data-solutions-framework/",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-data-solutions-framework.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_dsf",
        "aws_dsf._jsii"
    ],
    "package_data": {
        "aws_dsf._jsii": [
            "aws-dsf@1.0.0-rc.1.jsii.tgz"
        ],
        "aws_dsf": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.94.0, <3.0.0",
        "aws-cdk.lambda-layer-kubectl-v27>=2.0.0, <3.0.0",
        "constructs>=10.2.55, <11.0.0",
        "jsii>=1.88.0, <2.0.0",
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
