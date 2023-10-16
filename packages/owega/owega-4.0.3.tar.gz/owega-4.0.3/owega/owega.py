#!/usr/bin/env python3
# Import the necessary modules
import openai
import os
import json
import getpass
import sys
import time
import re
import argparse
import prompt_toolkit as pt
from .changelog import OwegaChangelog
from .license import OwegaLicense
from .config import baseConf, get_conf, debug_print, list_models
from .OwegaFun import existingFunctions, connectLTS
from .utils import (
	get_home_dir,
	get_temp_file,
	command_text,
	info_print,
	do_quit,
	success_msg,
	clrtxt,
	print_help,
)
from .conversation import Conversation


# prints an Conversation history
# TODO: move it as an Conversation method
def print_history(m: Conversation):
	for message in m.get_messages():
		if message['role'] == 'system':
			print("[ \033[92mSYSTEM\033[0m ]\033[92m")
		elif message['role'] == 'user':
			print("[ \033[96mUSER\033[0m ]\033[96m")
		elif message['role'] == 'assistant':
			print("[ \033[95mASSISTANT\033[0m ]\033[95m")
		else:
			print("[ \033[95mFUNCTION\033[0m ]\033[95m")
		print(message['content'])
		print("\033[0m")


# sometimes, GPT will give back invalid json.
# this function tries to make it valid
def convert_invalid_json(invalid_json):
	def replace_content(match):
		content = match.group(1)
		content = (
			content
			.replace('"', '\\"')
			.replace("\n", "\\n")
		)
		return f'"{content}"'
	valid_json = re.sub(r'`([^`]+)`', replace_content, invalid_json)
	return valid_json


# get a copy of owega's config
def get_oc_conf():
	return baseConf.copy()


# ask openAI a question
# TODO: comment a lot more
def ask(
	prompt: str = "",
	messages: Conversation = Conversation(),
	model=baseConf.get("model", ""),
	temperature=baseConf.get("temperature", 0.8),
	max_tokens=baseConf.get("max_tokens", 3000),
	function_call="auto",
	temp_api_key=""
):
	connectLTS(messages.add_memory, messages.remove_memory, messages.edit_memory)
	old_api_key = openai.api_key
	if (prompt):
		messages.add_question(prompt)
	else:
		prompt = messages.last_question()
	if isinstance(function_call, bool):
		if function_call:
			function_call = "auto"
		else:
			function_call = "none"
	response = False
	while (not response):
		try:
			if (temp_api_key):
				openai.api_key = temp_api_key
			response = openai.ChatCompletion.create(
				model=model,
				temperature=temperature,
				max_tokens=max_tokens,
				top_p=1.0,
				frequency_penalty=0.0,
				presence_penalty=0.0,
				messages=messages.get_messages(),
				functions=existingFunctions.getEnabled(),
				function_call=function_call,
			)
			if (temp_api_key):
				openai.api_key = old_api_key
		except openai.error.InvalidRequestError:
			messages.shorten()
		except openai.error.ServiceUnavailableError:
			print("[Owega] Service unavailable...", end="")
			time.sleep(1)
			print(" Retrying now...")
	# do something with the response
	message = response["choices"][0]["message"]
	while message.get("function_call"):
		try:
			messages.messages.append(message)
			function_name = message["function_call"]["name"]
			try:
				kwargs = json.loads(message["function_call"]["arguments"])
			except json.decoder.JSONDecodeError:
				unfixed = message["function_call"]["arguments"]
				fixed = convert_invalid_json(unfixed)
				kwargs = json.loads(fixed)
			function_response = existingFunctions.getFunction(function_name)(
				**kwargs
			)
			messages.add_function(function_name, function_response)
			response2 = False
			while not (response2):
				try:
					if (temp_api_key):
						openai.api_key = temp_api_key
					response2 = openai.ChatCompletion.create(
						model=model,
						temperature=temperature,
						max_tokens=max_tokens,
						top_p=1.0,
						frequency_penalty=0.0,
						presence_penalty=0.0,
						messages=messages.messages,
						functions=existingFunctions.getEnabled(),
						function_call=function_call,
					)
					if (temp_api_key):
						openai.api_key = old_api_key
				except openai.error.InvalidRequestError:
					messages.shorten()
				except openai.error.ServiceUnavailableError:
					print("[Owega] Service unavailable...", end="")
					time.sleep(1)
					print(" Retrying now...")
				message = response2["choices"][0]["message"]
		except Exception as e:
			print("Exception: " + str(e))
			print(message["function_call"]["arguments"])
			break
	try:
		messages.add_answer(message["content"].strip())
	except Exception as e:
		print("Exception: " + str(e))
	return messages


# generates the config file if it doesn't exist already
def genconfig(conf_path=""):
	if not conf_path:
		conf_path = get_home_dir() + "/.owega.json"
	is_blank = True
	if (os.path.exists(conf_path)):
		is_blank = False
		with open(conf_path, "r") as f:
			if len(f.read()) < 2:
				is_blank = True
	if is_blank:
		with open(conf_path, "w") as f:
			f.write(json.dumps(baseConf, indent='\t'))
		info_print(f"generated config file at {conf_path}!")
	else:
		info_print(f"sorry, {conf_path} already exists, delete it to regenerate")


######################
# directive handlers #
######################

# quits the program, deleting temp_file
def handle_quit(temp_file, messages, ps, given=""):
	do_quit(success_msg(), temp_file=temp_file)
	return messages


# prints help
def handle_help(temp_file, messages, ps, given=""):
	print_help()
	return messages


# generates config file
def handle_genconf(temp_file, messages, ps, given=""):
	genconfig()
	return messages


# shows chat history
def handle_history(temp_file, messages, ps, given=""):
	print_history(messages)
	return messages


# enables/disables command execution
def handle_commands(temp_file, messages, ps, given=""):
	if given.lower() in ["on", "true", "enable", "enabled"]:
		baseConf["commands"] = True
		existingFunctions.enableGroup("utility.system")
		info_print("Command execution enabled.")
		return messages

	if given.lower() in ["off", "false", "disable", "disabled"]:
		baseConf["commands"] = False
		existingFunctions.disableGroup("utility.system")
		info_print("Command execution disabled.")
		return messages

	baseConf["commands"] = (not baseConf.get("commands", False))
	if baseConf.get("commands", False):
		existingFunctions.enableGroup("utility.system")
		info_print("Command execution enabled.")
	else:
		existingFunctions.disableGroup("utility.system")
		info_print("Command execution disabled.")
	return messages


# change requested tokens amount
def handle_tokens(temp_file, messages, ps, given=""):
	given = given.strip()
	if given.isdigit():
		baseConf["max_tokens"] = int(given)
		info_print(f'Set requested tokens to {baseConf.get("max_tokens", 3000)}')
		return messages
	info_print(f'Currently requested tokens: {baseConf.get("max_tokens", 3000)}')
	info_print('How many tokens should be requested?')
	new_tokens = pt.prompt(pt.ANSI(
		'\n' + clrtxt("magenta", " tokens ") + ': '
	)).strip()
	if new_tokens.isdigit():
		baseConf["max_tokens"] = int(new_tokens)
		info_print(f'Set requested tokens to {baseConf.get("max_tokens", 3000)}')
	else:
		info_print('Invalid input, keeping current requested tokens amount')
	return messages


# change owega's system prompt
def handle_context(temp_file, messages, ps, given=""):
	given = given.strip()
	if given:
		messages.messages[0]['content'] = given
		info_print(f"New context: {messages.messages[0]['content']}")
		return messages
	info_print("Old context: " + messages.messages[0]['content'])
	new_context = ps['context'].prompt(pt.ANSI(
		'\n' + clrtxt("magenta", " new context ") + ': ')).strip()
	if new_context:
		info_print(f"New context: {messages.messages[0]['content']}")
		messages.messages[0]['content'] = new_context
	else:
		info_print("New context empty, keeping old context!")
	return messages


# saves the messages and prompt to a json file
def handle_save(temp_file, messages, ps, given=""):
	given = given.strip()
	try:
		if given:
			file_path = given
		else:
			file_path = ps['file'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " file output ") + ': ')).strip()
		messages.save(file_path)
	except Exception:
		print(clrtxt("red", " ERROR ") + f": could not write to \"{file_path}\"")
	else:
		print(clrtxt("green", " SUCCESS ") + ": conversation saved!")
	return messages


# loads the messages and prompt from a json file
def handle_load(temp_file, messages, ps, given=""):
	given = given.strip()
	try:
		if given:
			file_path = given
		else:
			file_path = ps['file'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " file to load ") + ': ')).strip()
		messages.load(file_path)
	except Exception:
		print(clrtxt("red", " ERROR ") + f": could not read from \"{file_path}\"")
	else:
		print(clrtxt("green", " SUCCESS ") + ": conversation loaded!")
	return messages


# changes the selected model
def handle_model(temp_file, messages, ps, given=""):
	given = given.strip()
	info_print(f"Current model: {baseConf.get('model', '')}")
	list_models()
	print()
	if given:
		new_model = given
	else:
		new_model = ps['model'].prompt(pt.ANSI(
			'\n' + clrtxt("magenta", " new model ") + ': ')).strip()
	if (new_model.isnumeric()):
		if (int(new_model) < len(baseConf.get("available_models", []))):
			mn = int(new_model)
			baseConf["model"] = baseConf.get("available_models", [])[mn]
			info_print(f"Model changed to {baseConf.get('model', '')}")
		else:
			info_print(f"Model not available, keeping {baseConf.get('model', '')}")
	elif new_model in list(baseConf.get("available_models", [])):
		baseConf["model"] = new_model
		info_print(f"Model changed to {baseConf.get('model', '')}")
	else:
		info_print(f"Model not available, keeping {baseConf.get('model', '')}")
	return messages


# get input from a file instead of the terminal
def handle_finput(temp_file, messages, ps, given=""):
	given = given.strip()
	given = given.split(' ')[0]
	if given:
		file_path = given
	else:
		file_path = ps['file_input'].prompt(pt.ANSI(
			clrtxt("yellow", " FILE LOCATION ") + ": ")).strip()
	if (os.path.exists(file_path)):
		user_prompt = ps['main'].prompt(pt.ANSI(
			clrtxt("yellow", " PRE-FILE PROMPT ") + ": ")).strip()
		with open(file_path, "r") as f:
			file_contents = f.read()
			full_prompt = f"{user_prompt}\n```\n{file_contents}\n```\n'"
			messages = ask(
				full_prompt,
				messages,
				baseConf.get("model", ""),
				baseConf.get("temperature", 0.8),
				baseConf.get("max_tokens", 3000)
			)
			print()
			print(clrtxt("magenta", " OpenAI ") + ": ")
			print()
			print(messages.last_answer())
	else:
		info_print(f"Can't access {file_path}")
	return messages


# dict containing all handler functions
handlers = {
	"quit": handle_quit,
	"exit": handle_quit,
	"help": handle_help,
	"genconf": handle_genconf,
	"history": handle_history,
	"commands": handle_commands,
	"tokens": handle_tokens,
	"context": handle_context,
	"save": handle_save,
	"load": handle_load,
	"model": handle_model,
	"file_input": handle_finput,
}


# bottom toolbar and style for prompt_toolkit
def main_bottom_toolbar(what: str = "toolbar"):
	if what == "style":
		msd = {
			'red':     '#000000 bg:#FF0000',  # noqa: E241
			'green':   '#000000 bg:#00FF00',  # noqa: E241
			'blue':    '#000000 bg:#0000FF',  # noqa: E241
			'yellow':  '#000000 bg:#FFFF00',  # noqa: E241
			'magenta': '#000000 bg:#FF00FF',  # noqa: E241
			'cyan':    '#000000 bg:#00FFFF',  # noqa: E241
			'white':   '#000000 bg:#FFFFFF',  # noqa: E241
		}
		msd['bottom-toolbar'] = msd['white']
		msd['bottom-even'] = msd['magenta']
		msd['bottom-odd'] = msd['cyan']
		msd['bottom-on'] = msd['green']
		msd['bottom-off'] = msd['red']
		main_style = pt.styles.Style.from_dict(msd)
		return main_style

	class tr:
		def __init__(self):
			self.table = []
			self.count = 0

		def add(self, prefix="/", txt="", color="yellow"):
			new_class = "white"
			# is_even = (self.count % 2) == 0
			# new_class = "bottom-odd"
			# if is_even:
			# 	new_class = "bottom-even"
			if not isinstance(txt, str):
				txt = str(txt)
			if self.count:
				self.table.append((
					"class:blue",
					" - "
				))
			if prefix:
				if txt:
					prefix = prefix + ": "
				self.table.append((
					f"class:{new_class}",
					prefix
				))
			if txt:
				self.table.append((
					f"class:{color}",
					txt
				))
			self.count += 1

	to_ret = tr()
	to_ret.add(f"v{OwegaChangelog.version}")
	to_ret.add("tokens", baseConf.get("max_tokens", "unknown"))
	to_ret.add("model", baseConf.get("model", "unknown"))
	to_ret.add(
		"commands",
		"ON" if baseConf.get("commands") else "OFF",
		"bottom-on" if baseConf.get("commands") else "bottom-off"
	)
	return to_ret.table


# main interaction loop
def user_interaction_loop(temp_file=get_temp_file(), input_file=""):
	# get the prefix
	# prefix = baseConf.get('prefix', '/')
	prefix = '/'

	# generate completion from command list (handlers)
	command_list = {}
	for command in handlers.keys():
		command_list[prefix + command] = None

	# CTRL+N makes a new line
	main_kb = pt.key_binding.KeyBindings()

	@main_kb.add('c-n')
	def _(event):
		event.current_buffer.insert_text('\n')

	# this defines how newlines are shown
	def main_prompt_continuation(width, line_number, is_soft_wrap):
		cont = '   ' if is_soft_wrap else '...'
		if (width >= 4):
			return (' ' * (width - 4)) + cont + ' '
		else:
			return ' ' * width

	# get main style
	main_style = main_bottom_toolbar("style")

	# creates Conversation object and populate it
	messages = Conversation()
	connectLTS(messages.add_memory, messages.remove_memory, messages.edit_memory)
	if input_file:
		messages.load(input_file)

	# sets the input prompt
	input_prompt = '\n' + clrtxt("yellow", "  USER  ") + ": "

	# prompt sessions (for command history, and other parameters)
	ps = {}

	# keyword autocompletion
	main_completer = pt.completion.NestedCompleter.from_nested_dict(
		command_list
	)

	# main session, for general context
	ps['main'] = pt.PromptSession(
		history=pt.history.FileHistory(
			'' + get_home_dir() + '/.owega.history'
		),
		completer=main_completer,
		complete_while_typing=True,
		complete_in_thread=True,
		auto_suggest=pt.auto_suggest.AutoSuggestFromHistory(),
		bottom_toolbar=main_bottom_toolbar,
		style=main_style,
		key_bindings=main_kb,
		prompt_continuation=main_prompt_continuation,
	)

	# context session, when editing owega's system prompt
	ps['context'] = pt.PromptSession()

	# file session, with file completion
	ps['file'] = pt.PromptSession(
		completer=pt.completion.PathCompleter()
	)

	# file session with file completion for file_input directive
	ps['file_input'] = pt.PromptSession(
		completer=pt.completion.PathCompleter()
	)

	# model session, for model selection
	# TODO: add model completion
	ps['model'] = pt.PromptSession()

	# bootup info
	info_print("===== Owega =====")
	info_print(f"Owega v{OwegaChangelog.version}")
	info_print(f'Type "{prefix}help" for help')
	info_print(f"Default model is {baseConf.get('model', '')}")
	info_print(f"temp file is {temp_file}")

	# API key detection
	if baseConf.get("api_key", "").startswith("sk-"):
		openai.api_key = baseConf.get("api_key", "")
	else:
		# if key not in config: ask for key only if not already set (ie envvar)
		try:
			if not openai.api_key.startswith("sk-"):
				openai.api_key = getpass.getpass(prompt="OpenAI API Key: ")
		except AttributeError:
			openai.api_key = getpass.getpass(prompt="OpenAI API Key: ")
		baseConf["api_key"] = openai.api_key

	# main interaction loop:
	while True:
		# save temp file
		messages.save(temp_file)

		# get user input, and strip it (no excess spaces / tabs / newlines
		user_input = ps['main'].prompt(pt.ANSI(input_prompt)).strip()

		command_found = False
		if user_input.startswith(prefix):
			uinp_spl = user_input.split(' ')
			given = ' '.join(uinp_spl[1:])
			command = uinp_spl[0][len(prefix):]
			if command in handlers.keys():
				command_found = True
				current_handler = handlers.get(command, handle_help)
				messages = current_handler(temp_file, messages, ps, given)
		if not command_found:
			messages = ask(
				user_input,
				messages,
				baseConf.get("model", ''),
				baseConf.get("temperature", 0.8),
				baseConf.get("max_tokens", 3000)
			)

			# Print the generated response
			print()
			print(clrtxt("magenta", " OpenAI ") + ": ")
			print()
			print(messages.last_answer())


# parse command-line arguments
def parse_args():
	parser = argparse.ArgumentParser(description="Owega main application")
	parser.add_argument("-d", "--debug", action='store_true',
		help="Enable debug output")
	parser.add_argument("-c", "--changelog", action='store_true',
		help="Display changelog and exit")
	parser.add_argument("-l", "--license", action='store_true',
		help="Display license and exit")
	parser.add_argument("-v", "--version", action='store_true',
		help="Display version and exit")
	parser.add_argument("-f", "--config-file", type=str,
		help="Specify path to config file")

	parser.add_argument("-i", "--history", type=str,
		help="Specify the history file to import")

	parser.add_argument("-a", "--ask", type=str,
		help="Asks a question directly from the command line")

	parser.add_argument("-o", "--output", type=str,
		help="Saves the history to the specified file")

	return parser.parse_args()


# finds if any element in the list a is present in the list b
def is_la_in_lb(a, b):
	for e in a:
		if e in b:
			return True
	return False


# ask a single question (with a new context)
def single_ask(user_prompt, temp_file=get_temp_file(), input_file=""):
	messages = Conversation()
	connectLTS(messages.add_memory, messages.remove_memory, messages.edit_memory)
	if input_file:
		messages.load(input_file)
	messages = ask(
		user_prompt,
		messages,
		baseConf.get("model", ''),
		baseConf.get("temperature", 0.8),
		baseConf.get("max_tokens", 3000)
	)
	print(messages.last_answer())
	messages.save(temp_file)


# main function, runs if __name__ is "__main__" ;)
def main():
	args = parse_args()

	if (args.debug):  # bypass before loading conf
		baseConf["debug"] = True

	if args.changelog:
		print(OwegaChangelog.log)
	if args.license:
		print(OwegaLicense)
	if args.version:
		print(f"Owega v{OwegaChangelog.version}")
	if (args.changelog or args.license or args.version):
		do_quit(value=1)

	input_history = ""
	if (args.history):
		input_history = args.history

	temp_file = get_temp_file()
	if (args.output):
		temp_file = args.output

	get_conf(args.config_file)
	if baseConf.get("commands", False):
		existingFunctions.enableGroup("utility.system")
	else:
		existingFunctions.disableGroup("utility.system")

	if (args.debug):  # bypass after loading conf
		baseConf["debug"] = True

	if (args.ask):
		single_ask(args.ask, temp_file, input_history)
	else:
		try:
			user_interaction_loop(temp_file, input_history)
		except EOFError:
			do_quit(success_msg(), temp_file=temp_file)
		except KeyboardInterrupt:
			do_quit(success_msg())


if __name__ == "__main__":
	main()
