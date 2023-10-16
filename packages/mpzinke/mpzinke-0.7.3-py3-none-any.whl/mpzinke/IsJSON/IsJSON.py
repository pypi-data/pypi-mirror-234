

import json


def is_json(string: str) -> bool:
	try:
		json.loads(string)
		return True

	except Exception as error:
		return False
