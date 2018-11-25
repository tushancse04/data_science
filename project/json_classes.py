import json


class result:
	def _init__(self):
		pass

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class presult:
	def _init__(self):
		pass