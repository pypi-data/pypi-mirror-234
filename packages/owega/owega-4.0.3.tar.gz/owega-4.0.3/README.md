# ΦωΦ (pronounced owega)
ΦωΦ is a command-line interface for conversing with GPT models (from OpenAI)


## Features
ΦωΦ has quite a lot of features!

These include:
- Saving/loading conversation to disk as json files.
- Autocompletion for commands, file search, etc...
- History management.
- Temp files to save every message, so that you can get back the conversation
  if you ever have to force-quit ΦωΦ.
- Config file to keep settings like api key, preferred model, command execution
  status...
- Command execution: if enabled, allows ΦωΦ to execute commands on your system
  and interpret the results.
- File creation: if commands are enabled, also allows ΦωΦ to create files on
  your system and fill them with desired contents.
- GET requests: allows ΦωΦ to get informations from online pages, through
  http(s) GET requests.
- Long-term memory: allows for ΦωΦ to store memories, which will not be deleted
  as the older messages are, to keep requests under the available tokens per
  request.
- Context management: allows to set the AI context prompt (example: "you are a
  cat. cats don't talk. you can only communicate by meowing, purring, and
  actions between asterisks" will transform ΦωΦ into a cat!!)
- Meow.
- Meow meow.
- MEOW MEOW MEOW MEOW!!!!


## Installation
Just do ``pip install --upgrade owega`` to get the latest version


## Command-line arguments
Do you really need me to do ``owega --help`` for you?

```
usage: owega [-h] [-d] [-c] [-l] [-v] [-f CONFIG_FILE] [-i HISTORY]
                   [-a ASK] [-o OUTPUT]

Owega main application

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug output
  -c, --changelog       Display changelog and exit
  -l, --license         Display license and exit
  -v, --version         Display version and exit
  -f CONFIG_FILE, --config-file CONFIG_FILE
                        Specify path to config file
  -i HISTORY, --history HISTORY
                        Specify the history file to import
  -a ASK, --ask ASK     Asks a question directly from the command line
  -o OUTPUT, --output OUTPUT
                        Saves the history to the specified file
```

## Showcase
See ΦωΦ in action!

[![asciicast](https://asciinema.org/a/613143.png)](https://asciinema.org/a/613143)
