#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="unipress",
	version="1.1",
	author="Konrad Sakowski",
	description="This is a library developed by Institute of High Pressure Physics of Polish Academy of Sciences.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
	],
	platforms = ["any", ],
	python_requires='>=3.6',
	py_modules=["unipress"],
	install_requires=[
		"numpy",
		"scipy",
	]
)
