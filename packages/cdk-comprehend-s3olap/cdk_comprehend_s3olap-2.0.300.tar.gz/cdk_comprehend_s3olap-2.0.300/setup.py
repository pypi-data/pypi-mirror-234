import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk_comprehend_s3olap",
    "version": "2.0.300",
    "description": "A constrcut for PII and redaction scenarios with Amazon Comprehend and S3 Object Lambda",
    "license": "Apache-2.0",
    "url": "https://github.com/HsiehShuJeng/cdk-comprehend-s3olap.git",
    "long_description_content_type": "text/markdown",
    "author": "Shu-Jeng Hsieh",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/HsiehShuJeng/cdk-comprehend-s3olap.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_comprehend_s3olap",
        "cdk_comprehend_s3olap._jsii"
    ],
    "package_data": {
        "cdk_comprehend_s3olap._jsii": [
            "cdk-comprehend-s3olap@2.0.300.jsii.tgz"
        ],
        "cdk_comprehend_s3olap": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.27.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
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
