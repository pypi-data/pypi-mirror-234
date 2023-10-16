import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "gammarer.aws-secure-frontend-web-app-cloudfront-distribution",
    "version": "0.10.3",
    "description": "AWS CloudFront distribution for frontend web app (spa) optimized.",
    "license": "Apache-2.0",
    "url": "https://github.com/gammarer/aws-secure-frontend-web-app-cloudfront-distribution.git",
    "long_description_content_type": "text/markdown",
    "author": "yicr<yicr@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gammarer/aws-secure-frontend-web-app-cloudfront-distribution.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "gammarer.aws_secure_frontend_web_app_cloudfront_distribution",
        "gammarer.aws_secure_frontend_web_app_cloudfront_distribution._jsii"
    ],
    "package_data": {
        "gammarer.aws_secure_frontend_web_app_cloudfront_distribution._jsii": [
            "aws-secure-frontend-web-app-cloudfront-distribution@0.10.3.jsii.tgz"
        ],
        "gammarer.aws_secure_frontend_web_app_cloudfront_distribution": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.80.0, <3.0.0",
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
