# Accessing Thymio from Python 

## Prerequisites 
Aseba provides asebamedulla, a command-line utility that allows you to access an 
Aseba network through D-Bus. This permits the use of Aseba-enabled devices from 
third-party languages such as Python, Perl or any language that supports the D-Bus 
protocol. asebamedulla has only been tested under Linux.


`sudo dpkg -i aseba_1.6.1_amd64.deb`


Example using Thymio and Python

If you have a Thymio II, you can easily control it from Python using medulla. 
First start medulla connecting to the Thymio:

`asebamedulla "ser:name=Thymio-II"`


Then, start your python program (test-medulla.py) passing a suitable Aseba program 
(test-medulla.aesl) as parameter. This program will be responsible for calling 
native functions and doing other on-robot computations. These can be useful, 
for instance to do pre-processing to reduce communication bandwidth:

`python3 ./test-medulla.py <full path name>/test-medulla.aesl`

A small library to access Aseba in Python (hiding the D-Bus access from you) 
is available in the examples/clients/python-dbus directory in the source tree. 
In addition, you can see a more detailed example of Thymio and Raspberry PI 
integration on this page.