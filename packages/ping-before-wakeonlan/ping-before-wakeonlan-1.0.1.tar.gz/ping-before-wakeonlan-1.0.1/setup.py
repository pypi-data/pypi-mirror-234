from setuptools import setup, find_packages
import os
import re
import pathlib

CWD = pathlib.Path(__file__).parent.resolve()

VERSION = '1.0.0' 
with open(os.path.join(CWD, 'ping_before_wakeonlan', '__init__.py'), 'r') as f:
    re_version_pattern = re.compile(r"=[\s]*['\"]([0-9\.]+)['\"]")
    for line in f:
        line = line.strip()
        if line.find('version') >= 0:
            extractVersionInfo = re_version_pattern.search(line)
            if extractVersionInfo:
                VERSION = extractVersionInfo.group(1)

PYTHON_REQUIRES = ">=3.10"
URL = "https://github.com/changyy/ping-before-wakeonlan"
DOWNLOAD_URL = "https://pypi.org/project/ping-before-wakeonlan/"
DESCRIPTION = 'Meet this Python Wake-on-LAN (WOL) Tool! It smartly checks your device status with integrated ping before sending the magic packet, ensuring efficiency. Set max wake devices, prevent power surges.'
LONG_DESCRIPTION = DESCRIPTION
LONG_DESCRIPTION_TYPE = 'text/plain'
try:
    with open(os.path.join(CWD, "README.md"), 'r') as f:
        data = f.read()
        if len(data) > 10:
            LONG_DESCRIPTION = data
            LONG_DESCRIPTION_TYPE = 'text/markdown'
except Exception as e:
    pass


INSTALL_REQUIRES = []
try:
    with open(os.path.join(CWD, "requirements.txt"), 'r') as f:
        INSTALL_REQUIRES = [s.strip() for s in f.read().split("\n")]
except Exception as e:
    pass

setup(
    name="ping-before-wakeonlan", 
    version=VERSION,
    author="Yuan-Yi Chang",
    author_email="<changyy.csie@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    keywords=['python', 'ping', 'wol'],
    python_requires=PYTHON_REQUIRES,
    url=URL,
    download_url=DOWNLOAD_URL,
    entry_points={
        'console_scripts': [
            'ping-before-wakeonlan = ping_before_wakeonlan.cmd:main',
        ],
    },
    classifiers= [
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)
