
# 
# A Message For You!
If you have done something in Azure which is repeated at least semi-often, do consider adding it as a function to this repo!

Just make sure you're not including any secret keys or sensitive information, as the code goes onto the open internet



# Overview
In-progress repo for functions for working with Azure in HMT. You can copy and paste the code from the repo, or load the functions with pip (pip version not currently working - Adam, October 2023).


# Putting into PyPi

This is in progress as of October 2023 (Adam). 

**Skynet note** twine can be slow or not work when you're using a proxy, which SkyNet does. I couldn't get the package to upload to pypi from SkyNet. To make it work I cloned the repo onto an ML Studio notebook and did the below steps in the ML Studio terminal. 

Process to put package in pypi:
1. Create pypi login, inc 2FA and API key
2. Build package `python setup.py sdist bdist_wheel`. Install wheel if you don't have it prior to this `pip install wheel`
3. Install twine `pip install twine`. Twine is used to connect and upload to pypi from your machine.
4. Upload package using your pipy API key `twine upload -u __token__ -p pypi-Ag_**full_long_key** dist/*`


# Use the package

`pip install hmt-azure-funcs`

See the version: `pip show hmt-azure-funcs`

Load a function in python: `from hmt_azure_funcs import upload_string`


# Issues

On an m1 macbook: hard a hardware issue I don't understand when importing. Could be a discrepency between the hardware the code was compiled on and the actual. Fernet may have some dependencies which makes this harder. 




# Uploading new version to PyPi

Go to code in terminal and delete folders used in build: `rm -rf dist hmt_azure_funcs.egg-info`

Update version in setup.py. Without this pypi won't accept the upload.

Build and upload with Twine, as per steps 2 and 3 in the section above. 


# Future improvements

Some testing for functions that are added. 



