# Idle-Node v0.0.0.2
## Copyright (C) 2019 :: EHVSN (Ethical Hackers vs Noobs)
[Idle-Node](https://github.com/Catayao56/Idle-Node.git) is an open-source command-line messaging platform written in Python.

## What's new?
+ Fixed config_handler.py's save_config_file() method
    - Converting bytes to string before decoding,
      Resulting to decoding error.

+ Fixed config_handler.py's set() method
    - No arguments/parameters are supplied when calling
      save_config_file() method.

    - config data are not split into lines.

    - Too much newlines when writing to file.

+ Fixed idle-node.py when there is no internet connection.
    - Program now catches requests module exceptions.

+ New command: `update`
    - Manually update your current IP Address.

+ New option rules when setting a new value
    - When the string `pass` is in the option name,
      The program will now ask you to re-enter the value.

+ New option rules when showing all available option and their values.
    - When the string `pass` is in the option name,
      The value of the option will be hidden.

+ Now, you will never see the "Goodbye!" message.

## Full Feature List
+ Peer-to-Peer Messaging
    - Using secure methods, Idle-Node can connect to a peer and send messages.

## License and Copying

+ This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, either version 3 of the
  License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.

  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.

+ See LICENSE file.

## Credits

* Development Team
    + Developer: [Catayao56](https://github.com/Catayao56)
    + Security Researcher: [Steffan (Aeneas of Troy)](https://github.com/aeneasoftroy)

## Requirements
+ Internet Connection.
+ Python Interpreter version 3.6+.
+ Dependencies
	* Dependencies can be installed automatically in the program. (Needs Internet Connection)

## Installing & Running
------------------------
1.Questions? Feature requests? Bugs?
      
      -Just contact us and we'll respond as soon as possible.
      -You can also create a merge request on https://github.com/Idle-Node.git