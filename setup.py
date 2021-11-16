from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpnext_oob/__init__.py
from erpnext_oob import __version__ as version

setup(
	name="erpnext_oob",
	version=version,
	description="ERPNext Out of Box",
	author="yuzelin",
	author_email="yuxinyong@163.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
