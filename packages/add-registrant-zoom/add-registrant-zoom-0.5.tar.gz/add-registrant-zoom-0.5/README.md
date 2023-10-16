# add-zoom-registrant

Project description

AddZoomRegistrant

A simple package to add Zoom Registrant from csv.

How to install

pip install zoom_registrant

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


MIT License

Copyright (c) [2023] [Mangesh]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
