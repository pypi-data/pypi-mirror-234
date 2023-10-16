from setuptools import setup

setup(
	name='owega',
	version='4.0.2',
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
)
