import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-surreal-backend",
    "version": "1.0.257",
    "description": "A package that vends a construct to setup the surreal backend in CDKTF",
    "license": "Apache-2.0",
    "url": "https://github.com/awlsring/cdktf-surreal-backend.git",
    "long_description_content_type": "text/markdown",
    "author": "awlsring<mattcanemail@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awlsring/cdktf-surreal-backend.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_surreal-backend",
        "cdktf_surreal-backend._jsii"
    ],
    "package_data": {
        "cdktf_surreal-backend._jsii": [
            "cdktf-surreal-backend@1.0.257.jsii.tgz"
        ],
        "cdktf_surreal-backend": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
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
