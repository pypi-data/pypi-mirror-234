#!/usr/bin/python
# -*- coding:utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rabbitmq-request-response",
    version="0.0.2",
    author="mengzengshan",
    author_email="378077287@qq.com",
    description="Common python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/starview/pulsar-request-response",
    packages=["rabbitmq_request_response"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "elasticsearch==7.12.0",
        "pika",
        "tornado",
    ],
)
