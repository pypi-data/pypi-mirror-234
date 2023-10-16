import json


def disabledFunction(*args, **kwargs):
	rdict = {}
	rdict["function_status"] = "Function disabled!"
	rdict["return_code"] = -1
	return json.dumps(rdict)


class Functions:
	def __init__(self):
		self.fstatuses = {}
		self.functions = {}
		self.descriptions = {}
		self.groups = {}

	def funExists(self, fname):
		if fname in self.fstatuses.keys():
			return True
		return False

	def addFunction(self, function, description):
		fname = description.get("name", "")
		if (not fname) or (self.funExists(fname)):
			return False
		self.fstatuses[fname] = True
		self.functions[fname] = function
		self.descriptions[fname] = description
		return True

	def connectFunction(self, fname, function):
		if not self.funExists(fname):
			return False
		self.fstatuses[fname] = True
		self.functions[fname] = function
		return True

	def removeFunction(self, fname):
		if not self.funExists(fname):
			return False
		self.fstatuses.pop(fname)
		self.functions.pop(fname)
		self.descriptions.pop(fname)
		return True

	def disableFunction(self, fname):
		if not self.funExists(fname):
			return False
		self.fstatuses[fname] = False
		return True

	def enableFunction(self, fname):
		if not self.funExists(fname):
			return False
		self.fstatuses[fname] = True
		return True

	def addGroup(self, gname, fnames):
		self.groups[gname] = fnames
		return True

	def removeGroup(self, gname):
		if gname not in self.groups.keys():
			return False
		self.groups.pop(gname)
		return True

	def enableGroup(self, gname):
		for fname in self.groups.get(gname, []):
			self.enableFunction(fname)

	def disableGroup(self, gname):
		for fname in self.groups.get(gname, []):
			self.disableFunction(fname)

	def getFunction(self, fname):
		if self.fstatuses.get(fname, False):
			return self.functions.get(fname, disabledFunction)
		return disabledFunction

	def getEnabled(self):
		descs = []
		for fname, desc in self.descriptions.items():
			if self.fstatuses.get(fname, False):
				descs.append(desc)
		return descs

	def append(self, other, gname=""):
		for other_gname, other_group in other.groups.items():
			self.addGroup(other_gname, other_group)
		group = []
		for fname, status in other.fstatuses.items():
			group.append(fname)
			self.addFunction(
				other.functions.get(fname, disabledFunction),
				other.descriptions.get(fname, {
					"name": fname,
					"description": "a disabled function",
					"parameters": {
						"type": "object",
					},
				})
			)
			if not status:
				self.disableFunction(fname)
		if gname:
			self.addGroup(gname, group)
		return self
