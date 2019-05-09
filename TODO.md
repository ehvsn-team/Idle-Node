# TO-DO list
## Information
This document is used as a list of TO-DOs and other plans.

 [X] _IN DEVELOPMENT_ +++Implement the login panel.
  ^       ^            ^           ^
  |       |            |           |
  |       |            | Description of the plan.
  |       | If the description has three plus symbols (`+`), it is prioritized.
  |      Must be _On Hold_, _In Development_, or _Finished_.
  |
  ``X`` if the feature is done.





## General
- [X] _Finished_ +++Develop the Main Module.
- [X] _Finished_ Settings/Customization Panel.
- [X] _Finished_ When you choose no in first run wizard, there is no DDNS keys in the config file.
- [X] _Finished_ Use hash to store passwords.
- [X] _Finished_ What if the user's IP is version 6? How will the logger check it?
- [X] _Finished_ Why hide passwords when it is in plaintext when setting a new one?
- [X] _Finished_ Randomized greeting and when user will logout
- [X] _Finished_ Refactor
- [ ] _In Development_ Contacts list.
- [ ] _On Hold_ Multi-user (Multi-account) Mode
- [ ] _On Hold_ Encrypt config file and contacts list with the user's password.
- [ ] _On Hold_ Peer-to-Peer Chat.
- [ ] _On Hold_ Group Chat / Conference Room.
- [ ] _On Hold_ Update loggers and docstrings.
- [ ] _On Hold_ All changed settings will be discarded when `*` option is supplied.
- [ ] _On Hold_ config_handler.py processes even when value is not string (e.g.: OSError)
- [ ] _On Hold_ Crashing when config file is not encoded and config_handler.py uses it.
- [ ] _On Hold_ Fix CI Emulator.
- [ ] _On Hold_ Support IPv6 Addresses.
- [ ] _On Hold_ Support custom ciphers.
- [ ] _On Hold_ Support Tor/Proxy connections
- [ ] _On Hold_ Benchmarking of encryption algorithms