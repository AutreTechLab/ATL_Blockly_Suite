##  AutreTechLab Blockly Suite for Educational Robotics
<img src="https://github.com/AutreTechLab/ATL_Blockly_Suite/raw/master/gallery/ATL-Suite2.jpg" width="400"/></a>

Our goal is to introduce children and young people between the ages of 8 and 18 to the world of technology and coding through the use of robotics.

While most of the students quickly understand the different mechanical parts of a robot, understanding the underlying software is something that takes quite a bit of effort. Most robots have they own development environment, programming language and simulation platforms.

* How can we reduce the "coding skills" entry barrier and be creative and have fun from day one? 
* How can we experiment with different robot platforms without having to dive deep into the corresponding development environments and coding languages?

AutreTechLab Blockly Suite provides programming environment that supports a classroom environment and allows our students to experiment with all our educational robots and experimental setups. 

It is based on the fork of maxosprojects/cozmo-blockly, which was the foundation for this development.

## How to install
1. Check out this repository with "git", or download it as a zip archive and unpack
2. Install prerequisites:
	* `pip3 install --user cozmo[camera]`
	* `pip3 install --user tornado ws4py`
	* it is highly recommended to install Node.js as described in [Security considerations](#security-considerations) section
3. Go to `server` folder
4. Start the server: `python3 server.py` (additionally, `-n <the future programmer's name>` can be supplied to set the default filename when saving/reloading programs - convenient on mobile devices)
5. Point your browser to `http://localhost:9090/`, which will display the welcome screen with more information on how to use the application. 

## Security considerations
There are two modes of code execution: `secure` and `non-secure`.

`secure` mode requires installation of [Node.js](https://nodejs.org).
In that mode the code you create with Blockly and execute with the `play` button is sent as Blockly XML AST to the server and there translated to an actual Python code and executed.

After you download and install NodeJS go to the `nodejs` folder and run `npm install`. That would install all the modules that are required for that additional service.

`non-secure` mode doesn't require Node.js. In that mode your program is traslated into Python code and is sent to the server for execution.
This mode is intended for contained environments (e.g. in a home network).
The risk here is that the server accepts arbitrary code from the network for execution.
If you are not sure your local home network is secure, or if you're planning to let people with potentially malicious intentions program your Cozmo, or you're running `server.py` not in your local home network, it is highly recommended to run `server.py` in `secure` mode.

By default `server.py` runs in `secure` mode. To run it in `non-secure` mode use `--nonsecure` command argument.
