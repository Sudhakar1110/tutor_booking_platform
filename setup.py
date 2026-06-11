# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\
")

# get version from __version__ variable in tutor_booking_platform/__init__.py
from tutor_booking_platform import __version__ as version

setup(
    name="tutor_booking_platform",
    version=version,
    description="A production-ready Tutor Booking Platform similar to UrbanPro, built on Frappe v15 and ERPNext v15",
    author="Antigravity",
    author_email="info@antigravity.dev",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)