import functools


@functools.total_ordering
class Version:
	def __init__(self,
		major: int = 0,
		minor: int = 0,
		patch: int = 0,
		status: str = ""
	):
		while status[0:1] == '-':
			status = status[1:]
		self.major = major
		self.minor = minor
		self.patch = patch
		self.status = status

	def from_dct(self, dct):
		self.__init__(
			dct.get("major", 0),
			dct.get("minor", 0),
			dct.get("patch", 0),
			dct.get("status", "")
		)
		return self

	def to_dct(self):
		dct = {
			"major": self.major,
			"minor": self.minor,
			"patch": self.patch,
			"status": self.status,
		}
		return dct

	def _is_valid_operand(self, other):
		return (
			hasattr(other, "major")
			and hasattr(other, "minor")
			and hasattr(other, "patch")
			and hasattr(other, "status")
		)

	def _compare_statuses(self, other) -> int:
		if not self._is_valid_operand(other):
			return NotImplemented

		# returns 0 if equal, -1 if self is lesser than other, 1 otherwise
		if self.status == other.status:
			return 0

		# fixes after standards
		if ("fix" not in self.status) and ("fix" in other.status):
			return -1
		if ("fix" in self.status) and ("fix" not in other.status):
			return 1

		# 1.0.0-rc1 is less than 1.0.0
		if self.status and (not other.status):
			return -1

		# 1.0.0 is greater than 1.0.0-rc1
		if (not self.status) and other.status:
			return 1

		# there should not be over 9 release candidates (preferably way less)
		# so 1.0.0-rc1 < 1.0.0-rc2
		if self.status < other.status:
			return -1
		return 1

	def __eq__(self, other):
		if not self._is_valid_operand(other):
			return NotImplemented
		return (
			(self.major == other.major)
			and (self.minor == other.minor)
			and (self.patch == other.patch)
			and (self.status == other.status)
		)

	def __lt__(self, other):
		if not self._is_valid_operand(other):
			return NotImplemented
		if (self.major < other.major):
			return True
		if (self.major > other.major):
			return False
		if (self.minor < other.minor):
			return True
		if (self.minor > other.minor):
			return False
		if (self.patch < other.patch):
			return True
		if (self.patch > other.patch):
			return False
		if (self._compare_statuses(other) < 0):
			return True
		return False

	def __str__(self):
		s = ""
		if self.status:
			s = f"-{self.status}"
		return f"{self.major}.{self.minor}.{self.patch}{s}"

	def __repr__(self):
		return self.__str__()
