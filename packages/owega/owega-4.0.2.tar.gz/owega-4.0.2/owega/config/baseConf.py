from owega.utils import get_home_dir, info_print
from owega.utils import debug_print as dp_internal
import os
import openai
import json

baseModels = [
	"gpt-3.5-turbo-16k",
	"gpt-4",
]
baseConf = {
	"api_key": "",
	"temperature": 0.8,
	"max_tokens": 3000,
	"keep_count": 100,
	"available_models": baseModels,
	"model": "gpt-3.5-turbo-16k",
	"debug": False,
	"commands": False,
	"prefix": "/",
	"blank": ""
}


def debug_print(text: str) -> None:
	return dp_internal(text, baseConf.get("debug", False))


# loads the config from a config file
def get_conf(conf_path=""):
	if not conf_path:
		conf_path = get_home_dir() + "/.owega.json"
		debug_print(f"conf_path is {conf_path}")
	if (os.path.exists(conf_path)):
		with open(conf_path) as f:
			conf_dict = json.load(f)
			for k, v in conf_dict.items():
				baseConf[k] = v
	if baseConf.get("api_key", "") != "":
		openai.api_key = baseConf["api_key"]


# list available models
def list_models():
	info_print("Available models:")
	for index, model in enumerate(baseConf.get("available_models", [])):
		info_print(f"    [{index}]: {model}")
