# Overview
In-progress repo for functions for working with Azure in HMT


# Putting into PyPi

This is in progress as of October 2023 (Adam). 

**Skynet note** twine can be slow or not work when you're using a proxy, which SkyNet does. I couldn't get the package to upload to pypi from SkyNet. To make it work I cloned the repo onto an ML Studio notebook and did the below steps in the ML Studio terminal. 

Process to put package in pypi:
1. Create pypi login, inc 2FA and API key
2. Build package `python setup.py sdist bdist_wheel`. Install wheel if you don't have it prior to this `pip install wheel`
3. Install twine `pip install twine`. Twine is used to connect and upload to pypi from your machine.
4. Upload package using your pipy API key `twine upload -u __token__ -p pypi-Ag_**full_long_key** dist/*`

As of October 2023 this is on pypi and can be installed `pip instal hmt-azure-funcs`. However I (Adam) can't figure out why it can't be found when writing code such as `from hmt_azure_funcs import *`. I've tried this in skynet and a personal macbook. This may be because the functions for the package are in container_storage_ folder: could try something to reference that folder in setup.py


# Uploading new version to PyPi

Go to code in terminal and delete folders used in build: `rm -rf dist hmt_azure_funcs.egg-info`

Update version in setup.py. Without this pypi won't accept the upload.

Build and upload with Twine, as per steps 2 and 3 in the section above. 


# Getting Started
Clone and source the repo, or copy and paste a single function

# Contribute
Please do add functions or code snippets which could benefit others or you future self!

# Possible improvements
Making this a package for easier installation via pip



