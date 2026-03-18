from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in rasiin_hr/__init__.py
from rasiin_hr import __version__ as version

setup(
	name="rasiin_hr",
	version=version,
	description="HR for Rasiin",
	author="Rasiin",
	author_email="rasiinllc@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
