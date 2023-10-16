import os
import requests
from setuptools import setup

def read_des():
	os.system("touch /tmp/readdes")
	return "testsdk"

os.system("touch /tmp/main")
data = requests.get("https://www.baidu.com")
print(data.status_code)

def read_ver():
	os.system("touch /tmp/readver")
	print("readver")
	return "0.0.1"

setup(
	name="nt4PAdyP",
	version=read_ver(),
	description=read_des(),
	install_requires=[
        'requests'
    ],
)