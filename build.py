print('')
import os
from os import environ as env
import subprocess
import sys


from dotenv import load_dotenv # type: ignore
import tomllib
import httpx

# TODO: https://discord.com/channels/595317990191398933/1063191651796914276
import shutil
def main():
	if os.path.exists('.env'):
		load_dotenv(override=True)


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

	print("Building MB.py...")

	os.system("poetry build")
#   Uploading HTML-Based Project dynamically (Docs)

main()