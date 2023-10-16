from owega.utils import command_text
from owega.config import debug_print
from .functions import Functions
import subprocess
import prompt_toolkit as pt
import json
import requests

Utility = Functions()


# executes a given string, if bypass is true, do not ask for confirmation
# def __execute(command: str, bypass: bool = False):
def __execute(*args, **kwargs):
	command = ""
	bypass = False
	if len(args) > 0:
		command = args[0]
		if len(args) > 1:
			command = args[1]
	command = kwargs.get("command", command)
	bypass = kwargs.get("bypass", bypass)
	rdict = {}
	if not bypass:
		print()
		print(command_text("Owega wants to execute the following command:"))
		print(command_text(command))
		user_input = pt.prompt(pt.ANSI(
			command_text("Do you want to run it? (y/N): ")))
		user_input = user_input.lower().strip()
		if (user_input) == "y":
			bypass = True
	if bypass:
		pipes = subprocess.Popen(
			command,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			shell=True
		)
		std_out, std_err = pipes.communicate()
		rdict["command_stdout"] = std_out.decode('utf8')
		rdict["command_stderr"] = std_err.decode('utf8')
		rdict["command_status"] = "EXECUTED"
		rdict["return_code"] = pipes.returncode
	else:
		rdict["command_stdout"] = "FAIL: User denied running this command.\n"
		rdict["command_stderr"] = "FAIL: User denied running this command.\n"
		rdict["command_status"] = "FAILED"
		rdict["return_code"] = -1
	return json.dumps(rdict)


__execute_desc = {
	"name": "execute",
	"description": "executes a command on the user's linux computer and returns its output",
	"parameters": {
		"type": "object",
		"properties": {
			"command": {
				"type": "string",
				"description": "the command to run, as a string"
			}
		},
		"required": ["command"],
	},
}


Utility.addFunction(__execute, __execute_desc)


# gets page
def __get_page(*args, **kwargs):
	url = "https://example.com"
	if len(args) > 0:
		url = args[0]
	url = kwargs.get("url", url)
	print()
	print(command_text(f"getting page: {url}"))
	rdict = {}
	rdict["status"] = "error"
	rdict["page"] = ""
	try:
		page = requests.get(url).text
		rdict["status"] = "success"
		rdict["page"] = page
	except Exception:
		rdict = {}
		rdict["status"] = "error"
		rdict["page"] = ""
		pass
	return json.dumps(rdict)


__get_page_desc = {
	"name": "get_page",
	"description": "gets the requested page as an HTML string",
	"parameters": {
		"type": "object",
		"properties": {
			"url": {
				"type": "string",
				"description": "the url to get"
			}
		},
		"required": ["url"],
	},
}


Utility.addFunction(__get_page, __get_page_desc)


# creates a file and fill it with contents
# def __create_file(filename: str, content: str, bypass: bool = False):
def __create_file(*args, **kwargs):
	filename = ""
	content = ""
	bypass = False
	if len(args) > 0:
		filename = args[0]
		if len(args) > 1:
			content = args[1]
			if len(args) > 2:
				bypass = args[2]
	filename = kwargs.get("filename", filename)
	content = kwargs.get("content", content)
	bypass = kwargs.get("bypass", bypass)
	rdict = {}
	if not filename:
		rdict["status"] = "FAILURE"
		rdict["exception"] = "FAIL: No filename provided.\n"
		return json.dumps(rdict)
	if not bypass:
		print()
		print(command_text(
			f"Owega wants to create {filename} with the following content:"
		))
		print(content)
		user_input = pt.prompt(pt.ANSI(
			command_text("Do you want to allow it? (y/N): ")))
		user_input = user_input.lower().strip()
		if (user_input) == "y":
			bypass = True
	if bypass:
		try:
			with open(filename, "w") as f:
				f.write(content)
			rdict["status"] = "SUCCESS"
		except Exception as e:
			rdict["status"] = "FAILURE"
			rdict["exception"] = str(e)
	else:
		rdict["status"] = "FAILURE"
		rdict["exception"] = "FAIL: User denied creating this file.\n"
	return json.dumps(rdict)


# add create_file(filename, content) to owega's available functions
__create_file_desc = {
	"name": "create_file",
	"description": "creates a file and writes the given content in it",
	"parameters": {
		"type": "object",
		"properties": {
			"filename": {
				"type": "string",
				"description": "the name of the file to create"
			},
			"content": {
				"type": "string",
				"description": "the content to put in the file, as a string"
			},
		},
		"required": ["filename", "content"],
	},
}


Utility.addFunction(__get_page, __get_page_desc)


Utility.addGroup("utility.user", ["get_page"])
Utility.addGroup("utility.system", ["execute", "create_file"])
Utility.enableGroup("utility.user")
Utility.disableGroup("utility.system")
