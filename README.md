# Idle-Node v0.0.0.6

## Copyright (C) 2019 :: EHVSN (Ethical Hackers vs Noobs)

[Idle-Node](https://github.com/ehvsn-team/Idle-Node.git) is an open-source decentralized messaging platform written in Python.

## New features

* Configuration manager now raises an error if the new value type is not the same as the old value type.

* Updated Simple Library module.

* Config files updated.
  * Added port values.

* Removed TestCase() class.

* Logfiles and configuration files can now be set using the
`--config-file` and `--logfile` command-line arguments.

* New method (cleanup()) now runs when KeyboardInterrupt and proper exit is detected.

* User IDs are now generated on first run.
  * User IDs will be your "unique" identification.
  * If Alice and Bob has the same usernames, they are still distinguishable via their unique user IDs.

* Set timeout on requests.
* DuckDNS token input is now shown.
* New command `status`.
  * As the command implies, it shows the program status.

* Program now automatically loads the new configuration file after saving.
* Fixed possible security issue. (config file contents are written on to the logfile.)

* Cipher modules now in core/Ciphers Folder.

* Command-line arguments now functional.

* More goodbye messages!

* Removed manual module. (Will be back sooner or later)

* The most recent supported python version is `v3.4.4`.
  * Idle-Node will now just warn the user when using python version 3.4.4

* Fixed config_handler.py's save_config_file() method
  * Converting bytes to string before decoding,

* [WIP] Idle-Node TestCase() class for testing Idle-Node.

* [WIP] Contacts Manager (`contacts` and `cntcts` commands)

## Full Feature List

* Peer-to-Peer Messaging
  * Using secure (or optionally, insecure) methods,
      Idle-Node can connect to a peer and send messages.

* Server/Client Model for Conference and Group Chats
  * Users can also use their own computers to be a server!
  * Start a group chat. (also called conference.)
  * Use the server as a centralized server.

* Verify peer or server's identity
  * Use several methods to identify a peer/server, like TOFU (Trust on First Use),
      One-time passwords, and more. (See manual for more info)

* No conversation logs
  * By default, Idle-Node does not store conversations. So when both of you
      disconnects, no logs will be saved. No evidence are saved :p

* Open-Sourced
  * You can look and/or modify the source code to suit your needs.
      Make Idle-Node accept connections from specific IPs, support GUI, add more APIs,
      and more. (See manual for more info)

* Add custom ciphers
  * You can **add your own encryption method**! Just place the python file with
      encryption and decryption method in the IdleCipher() class into the
      core/Ciphers path.

* Documented Security Design
  * You want to know how Idle-Node works? Type `manual` in the main Idle-Node
      terminal and read the articles you need. You might have a new friend while
      searching for articles there...

* Multiplatform
  * As long as there is Internet connection, Python 3.6+, and dependencies in your
      machine, you can run Idle-Node!

* Lots of available interfaces
  * While other closed-source (or even open-sourced) programs offer only GUI or web
      interfaces, Idle-Node supports three (3) interfaces: CLI, GUI, and Web\*!
      (\*For servers only)

* WE ARE FOCUSED ON PRIVACY
  * **No logs are sent to anyone** (except if you send us the log for fixing bugs.)
  * **Immediately clear conversations** (The default option is set to ``True``.)
  * This software connects to the following:
  01. ``https://api.ipify.org`` (For getting machine's remote IP Address.)
  02. ``https://www.duckdns.org`` (If you use this as your DDNS provider, Idle-Node will contact DuckDNS.org's server.)
  03. ``https://www.noip.com`` (If you use this as your DDNS provider, Idle-Node will contact noip.com's server.)
  04. ``Your recipient/chatroom`` (Self-explanatory...)

## License and Copying

* This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, either version 3 of the
  License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.

  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.

* See LICENSE file.

## Credits

* Development Team
  * Developer: [Catayao56](https://github.com/Catayao56)
  * Developer: [Beyar Nahro](https://github.com/Beyarz)
  * Security Researcher: [Steffan (Aeneas of Troy)](https://github.com/aeneasoftroy)
  * The Ethical Hackers vs Noobs (EHVSN) Team

* Third-Party Modules
  * Multitasking Module: [Ran Aroussi](https://github.com/ranaroussi/multitasking)
  * no_ip_updater Module: [Kelvin Steiner](kelvinsteinersantos@gmail.com)
  * cowsay Module: [Jesse Chan-Norris](http://www.nog.net/~tony/warez/cowsay.shtml)
  * PyCryptodome Authors

* Miscellaneous
  * RealPython Community
  * The Python Organization

## Minimum Requirements

* Internet Connection
* Python Interpreter version 3.4.4
* Dependencies
  * requests
  * pycryptodome

## Recommended Requirements

* Internet Connection.
* Python Interpreter version 3.6.0+.
* Dependencies
  * requests
  * pycryptodome

## Installing & Running

1. Questions? Feature requests? Bugs?

      - Just contact us and we'll respond as soon as possible.
      - You can also create a merge request on https://github.com/ehvsn-team/Idle-Node.git

## Troubleshooting

* Idle-Node not accepting external connections
  * If you can connect from a different PC inside your private network,
    then there's nothing wrong with Idle-Node. It's almost certain that
    there's something wrong with your router or the port forwarding configuration.

    Make sure that you've re-reviewed your port forwarding settings and
    perhaps try restarting the router (be careful to verify your internally
    assigned IP addresses haven't changed if you go this route).