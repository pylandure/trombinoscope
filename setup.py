"""Trombinoscope package setup.py file.
   """
from distutils.core import setup

setup(
    name="Trombinoscope",
    version="0.1dev",
    description="A simple facebook for Simplon",
    author="Pierre-Yves Landuré, Kevin BOUCLY",
    author_email="pierre-yves.landure@isen-ouest.yncrea.fr, kevin.boucly@isen-ouest.yncrea.fr",
    packages=["trombinoscope"],
    license="GPLv3",
    long_description=open("README.md").read(),
)
