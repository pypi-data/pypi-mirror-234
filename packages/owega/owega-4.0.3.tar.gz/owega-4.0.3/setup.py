#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

desc = open('README.md').read()

setup(
	name='owega',
	version='4.0.3',
	packages=[
		'owega',
		'owega.changelog',
		'owega.config',
		'owega.OwegaFun',
		'owega.conversation',
	],
	install_requires=[
		'openai>=0.27',
		'prompt_toolkit>=3.0',
		'requests>=2.0',
	],
	scripts=[
		'scripts/owega',
	],
	long_description=desc,
	long_description_content_type='text/markdown',
)
