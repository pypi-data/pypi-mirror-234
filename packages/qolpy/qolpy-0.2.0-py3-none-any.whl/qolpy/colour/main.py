import math
import random
from typing import Any, Literal, Union
from .interface import Colour_Setting
from .switch import FauxSwitch

switch = FauxSwitch().switch

def random_colour(setting: Colour_Setting = "hex") -> str:
	"""
	Generate a random colour

	Args:
		setting: Optional; The type of colour you would like to get returned. Defualts to `hex`

	Returns:
		a random colour as a string, preformatted to be inserted directly into code.

		```py
		c = random_colour("rgb")
		# 235, 235, 123
		``` 
	"""
	random_hex: str = ""
	i: int = 0

	while i < 6:
		random_hex += hex(math.floor(random.random() * 16))[2:]
		i += 1

	if setting == "hex":
		return f"#{random_hex}"
	else:
		res = switch(setting, random_hex)
		return res[0] if res is not False else "error"
