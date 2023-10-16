import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-github-actions",
    "version": "0.0.264",
    "description": "@awlsring/cdktf-github-actions",
    "license": "Apache-2.0",
    "url": "https://github.com/awlsring/cdktf-github-actions.git",
    "long_description_content_type": "text/markdown",
    "author": "awlsring<mattcanemail@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awlsring/cdktf-github-actions.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_github-actions",
        "cdktf_github-actions._jsii"
    ],
    "package_data": {
        "cdktf_github-actions._jsii": [
            "cdktf-github-actions@0.0.264.jsii.tgz"
        ],
        "cdktf_github-actions": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf-cdktf-provider-github>=5.0.0, <6.0.0",
        "cdktf>=0.14.0, <0.15.0",
        "constructs>=10.0.25, <11.0.0",
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
