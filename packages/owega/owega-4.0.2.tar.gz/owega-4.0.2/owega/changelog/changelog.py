from .changelogEntry import ChangelogEntry
from .version import Version


class Changelog:
	def __init__(self):
		self.logs = []
		self.log = ""
		self.version = Version(0, 0, 0)
		self.initLogs()
		self.genLog()

	def initLogs(self):
		self.logs.append(
			ChangelogEntry(2, 0, 0)
			.addLine("WTFPL license")
		)
		self.logs.append(
			ChangelogEntry(2, 0, 1)
			.addLine("added genconf command")
		)

		self.logs.append(
			ChangelogEntry(2, 1, 0)
			.addLine("added file_input command")
		)
		self.logs.append(
			ChangelogEntry(2, 1, 1)
			.addLine("added file_input in help command")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 0)
			.addLine("added context command to change GPT's definition")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 1)
			.addLine("added license and version info in command line (-l and -v)")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 2)
			.addLine("stripped user input (remove trailing spaces/tabs/newlines)")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 3)
			.addLine("genconf now saves the current conf instead of a blank template")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 4)
			.addLine("automatic temp file save")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 0)
			.addLine("added context command to change GPT's definition")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 1)
			.addLine("added license and version info in command line (-l and -v)")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 2)
			.addLine("stripped user input (remove trailing spaces/tabs/newlines)")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 3)
			.addLine("genconf now saves the current conf instead of a blank template")
		)
		self.logs.append(
			ChangelogEntry(2, 2, 4)
			.addLine("automatic temp file save")
		)
		self.logs.append(
			ChangelogEntry(3, 0, 0)
			.addLine("changed conversation save from pickle to json")
		)
		self.logs.append(
			ChangelogEntry(3, 0, 1)
			.addLine("added changelog")
		)
		self.logs.append(
			ChangelogEntry(3, 0, 2)
			.addLine("added conversion script")
		)
		self.logs.append(
			ChangelogEntry(3, 0, 3)
			.addLine("quitting with EOF will now discard the temp file (^C will still keep it)")
		)
		self.logs.append(
			ChangelogEntry(3, 1, 0)
			.addLine("BMU (Better Module Update)!")
			.addLine("modified MSGS:")
			.addLine("  - added last_question()")
			.addLine("  - changed last_answer()")
			.addLine("modified ask() to allow for blank prompt,")
			.addLine("  which will reuse the last question")
		)
		self.logs.append(
			ChangelogEntry(3, 1, 1)
			.addLine("now handling the service unavailable error")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 0)
			.addLine("FUNCTION CALLING UPDATE:")
			.addLine("added function calling, now openchat is able to run commands")
			.addLine("on your computer, as long as you allow it to")
			.addLine("(you will be prompted on each time it tries to run a command)")
			.addLine("!!! only available on -0613 models (gpt-3.5-turbo-0613, gpt-4-0613) !!!")
			.addLine("will be available on all gpt models from 2023-06-27, with the latest")
			.addLine("openchat 3.2.X patch")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 1)
			.addLine("fixed a space missing in openchat's function calling")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 2)
			.addLine("fixed openchat sometimes not detecting the command has been ran")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 3)
			.addLine("added create_file as a function OpenAI can call")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 4)
			.addLine("fixed variables and ~ not expanding when executing a command")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 4, "fix1")
			.addLine("fixed a missing parenthesis")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 5)
			.addLine("now handling non-zero exit status when running a command")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 6)
			.addLine("reversed the changelog order, fixed function calling chains")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 7)
			.addLine("fixed json sometimes not correctly formatted when writing multiple lines")
			.addLine("files")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 8)
			.addLine("fixed command execution stderr handling")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 9)
			.addLine("changed execute's subprocess call to shell=True, now handling pipes...")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 10)
			.addLine("added a command line option for specifying the config file")
		)
		self.logs.append(
			ChangelogEntry(3, 2, 11)
			.addLine("now, the default gpt models implement function calling, no need for")
			.addLine("0613 anymore")
		)
		self.logs.append(
			ChangelogEntry(3, 3, 0)
			.addLine("implemented prompt_toolkit, for better prompt handling, newlines with")
			.addLine("control+n")
		)
		self.logs.append(
			ChangelogEntry(3, 3, 1)
			.addLine("added tokens command, to change the amount of requested tokens")
		)
		self.logs.append(
			ChangelogEntry(3, 4, 0)
			.addLine("CLI update:")
			.addLine("  - added command-line options to change input/output files")
			.addLine("  - added command-line option to ask a question from command line")
		)
		self.logs.append(
			ChangelogEntry(3, 5, 0)
			.addLine("WEB update: now added a flask app, switched repos to its own")
		)
		self.logs.append(
			ChangelogEntry(3, 5, 1)
			.addLine('added "commands" command, to enable/disable command execution')
		)
		self.logs.append(
			ChangelogEntry(3, 5, 2)
			.addLine("added infos on bottom bar")
		)
		self.logs.append(
			ChangelogEntry(3, 6, 0)
			.addLine("PREFIX update:")
			.addLine("  - added prefixes for command (changeable in the config)")
			.addLine("  - reformatted most of the main loop code to split it in handlers")
		)
		self.logs.append(
			ChangelogEntry(3, 7, 0)
			.addLine("DIRECT CONTEXT COMMANDS update:")
			.addLine("  - now, you can use commands in one line, instead of waiting for prompt")
			.addLine("      example: /save hello.json")
			.addLine("      (instead of typing /save, then enter, then typing hello.json")
			.addLine("       works on all commands, the only specific case being file_input.)")
			.addLine("  - file_input as a direct command takes only one argument: the file")
			.addLine("      to load (e.g. /load ./src/main.c). The pre-prompt will be asked")
			.addLine("      directly instead of having to do it in three steps")
			.addLine("        (/load, then filename, then pre-prompt)")
			.addLine("  - also, fixed /tokens splitting the prompt instead of the user input")
		)
		self.logs.append(
			ChangelogEntry(3, 8, 0)
			.addLine("WEB download update")
			.addLine("  - added a get_page function for openchat to get pages without the need")
			.addLine("      for curl")
		)
		self.logs.append(
			ChangelogEntry(3, 8, 1)
			.addLine("added a debug option for devs")
		)
		self.logs.append(
			ChangelogEntry(3, 9, 0)
			.addLine("Windows update")
			.addLine("  - Do I really need to explain that update?")
		)
		self.logs.append(
			ChangelogEntry(3, 9, 1)
			.addLine("fixed an issue when the openai api key does not exist anywhere")
		)
		self.logs.append(
			ChangelogEntry(3, 9, 2)
			.addLine("changed the temp file creation method for non-unix systems")
		)
		self.logs.append(
			ChangelogEntry(3, 9, 3)
			.addLine("fixed api key not saving with /genconf")
		)
		self.logs.append(
			ChangelogEntry(3, 9, 4)
			.addLine("changed default values")
		)

		self.logs.append(
			ChangelogEntry(4, 0, 0)
			.addLine("LTS: Long-Term-Souvenirs")
			.addLine("The AI now have long-term memory!!!")
			.addLine("Huge update: full refactoring, the code is now readable!")
			.addLine("Also, the name is now Owega (it's written with unicode characters though)")
			.addLine("You can see the new code here: https://git.pyrokinesis.fr/darkgeem/owega")
			.addLine("Also, the project is now available on PyPI so, just go pip install owega!")
		)

		self.logs.append(
			ChangelogEntry(4, 0, 1)
			.addLine("oops, forgot to change the setup.py and now I messed up my 4.0.0! >:C")
		)

		self.logs.append(
			ChangelogEntry(4, 0, 2)
			.addLine("Fixed a typo where owega wouldn't send the memory")
		)

	def genLog(self):
		self.logs.sort()
		self.version = self.logs[-1].version
		self.version_str = str(self.logs[-1].version)
		self.log = f"OWEGA v{self.version_str} CHANGELOG:"
		for entry in self.logs:
			ver = entry.version
			if (not ver.status) and ver.patch == 0:
				self.log += '\n'
				if ver.minor == 0:
					self.log += '\n'
			self.log += '\n'
			if 'rc' in ver.status:
				self.log += '\033[91m'
			self.log += str(entry)
			if 'rc' in ver.status:
				self.log += '\033[m'


OwegaChangelog = Changelog()
