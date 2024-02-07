print('')
import os
from os import environ as env
import subprocess
import sys


from dotenv import load_dotenv # type: ignore
import tomllib
import httpx

import shutil


def main():
	if os.path.exists('.env'):
		load_dotenv(override=True)

	assert os.system("npx wrangler -v") == 0, "Install Wrangler! \n npm install wrangler --global"

	os.system("rm -rf ./build/")
	with open("pyproject.toml", 'rb') as f:
		config = tomllib.load(f)

	with open("MeowerBot/_version.py", "w") as f:
		f.write(f"__version__ = '{config["tool"]["poetry"]["version"]}'\n")

	os.chdir("docs")
	print("Building docs...")
	proc = os.system("bash build.sh")
	if proc != 0:
		return

	print("Uploading docs...")
	os.system("npx wrangler pages deploy ./build/html --project-name meowerbot --commit-dirty=true --branch=master")


	print("Building MB.py...")

	os.system("poetry build")

main()
