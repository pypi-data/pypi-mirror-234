from setuptools import setup, find_packages

long_description = """
zoom_registrant is a Python package that allows you to interact with the Zoom API. 
It provides functions for managing Zoom meetings and registrants.

Project description

Add Zoom Registrant

A simple package to add Zoom Registrant from csv.

How to install

pip install add-registrant-zoom

Import

from myzoom.setting import configure
from myzoom.AddZoomRegistrant import add_registrants

meeting_id = input("Enter meeting id: ")
csv_path = input("Enter csv file path: ")
add_registrants(configure, meeting_id, csv_path)

Initialize the Package
We can either setup via the environment or by passing the credentials directly to the plugin.

client_id for the ClientId
client_secret for the ClientSecret
account_id for the AccountId

And then instantiate as shown below

settings = configure(client_id, client_secret, account_id)

NOTE

You don't need to explicitely pass client_id, client_secret, account_id.


csv_path = input("Enter csv file path: ")
add_registrants(settings, meeting_id, csv_path)


zoom.csv format must as below.

eg.

Id	FirstName	LastName	Email
1    ABC        PQR         abc.pqr@email.com

"""

setup(
    name="add-registrant-zoom",
    version="0.4",
    url='https://github.com/own-coder/add-zoom-registrant',
    description="A package for interacting with Zoom API",
    author="Mangesh Chavan",
    long_description=long_description,  
    long_description_content_type="text/plain",
    author_email="chavanmangesh245@gmail.com",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
    ]
    ,
    install_requires=[
        "requests",  # Add any dependencies your package requires
    ],
)
