from typing import Union, Literal, Any, List, Tuple
from .interface import Colour_Setting

class FauxSwitch(object):
    """A lambda class based switch to change hex to other colour format"""
    def switch(self, setting: Colour_Setting, r_hex: str) -> Union[Any, Literal[False]]:
        """A lambda class based switch to change hex to other colour format"""
        formated_setting: str = f"__to_{setting}__"
        colour_switch = getattr(self, formated_setting, lambda r_hex=r_hex: False)
        return colour_switch(r_hex)
    
    @staticmethod
    def __compute_colour__(r: int, g: int, b: int, setting: Literal["cmyk", "hs*"]) -> List[float]:
        if setting == "cmyk":
            cc: float = 1 - r / 255
            cm: float = 1 - g / 255
            cy: float = 1 - b / 255
            ck: float = min(cc, cm, cy)
            return [cc, cm, cy, ck]
        
        cr: float = r / 255
        cg: float = g / 255
        cb: float = b / 255
        c_min: float = min(cr, cg, cb)
        c_max: float = max(cr, cg, cb)
        return [cr, cg, cb, c_min, c_max]
    
    def __to_rgb__(self, r_hex: str) -> Tuple[str, int, int, int]:
        """
        Convert a hex to RGB
    
        Args:
		    hex: the colour as a hex
        
        Returns:
		    a tuple of `red`, `green`, and `blue` values
        """
        r = int(r_hex[:2], 16)
        g = int(r_hex[2:4], 16)
        b = int(r_hex[4:6], 16)

        as_string: str = f"rbg({r}, {g}, {b})"

        return (as_string, r, g, b)

    def __to_cmyk__(self, r_hex: str) -> Tuple[str, float, float, float, float]:
        """
        Convert a hex to CMYK
	
        Args:
            hex: the colour as a hex

        Returns:
            a tuple of `cyan`, `magenta`, `yellow`, `key` as percentages
        """
        r, g, b = self.__to_rgb__(r_hex)[1:]
        
        if r == 0 and g == 0 and b == 0:
            return ("cmyk(0%, 0%, 0%, 100%)", 0, 0, 0, 100)
        
        cc, cm, cy, ck = self.__compute_colour__(r, g, b, "cmyk")

        dc: float = (cc - ck) / (1 - ck)
        dm: float = (cm - ck) / (1 - ck)
        dy: float = (cy - ck) / (1 - ck)

        c: float = dc * 100
        m: float = dm * 100
        y: float = dy * 100
        k: float = ck * 100

        as_string: str = f"cmyk({c}%, {m}%, {y}%, {k}%)"

        return (as_string, c, m, y, k)
    
    def __to_hsv__(self, r_hex: str) -> Tuple[str, float, float, float]:
        """
        Convert a hex to HSV
	
        Args:
            hex: the colour as a hex

        Returns:
            a tuple of `hue`, `saturation` as a percentage, `value` as a percentage
        """
        r, g, b = self.__to_rgb__(r_hex)[1:]
        cr, cg, cb, c_min, cv = self.__compute_colour__(r, g, b, "hs*")

        x: float = cg - cb if cr == c_min else cr - cg if cb == c_min else cb - cr
        y: int = 3 if cr == c_min else 1 if cb == c_min else 5

        h: float = 60 * (y - x / (cv - c_min))

        cS: float = (cv - c_min) / cv

        s: float = cS * 100
        v: float = cv * 100

        as_string: str = f"hsv({h}, {s}%, {v}%)"

        return (as_string, h, s, v)

    def __to_hsl__(self, r_hex: str) -> Tuple[str, float, float, float]:
        """
	    Convert a hex to HSL

        Args:
        	hex: the colour as a hex

        Returns:
        	a tuple of `hue`, `saturation` as a percentage, `lightness` as a percentage
        """
        r, g, b = self.__to_rgb__(r_hex)[1:]
        cr, cg, cb, c_min, c_max = self.__compute_colour__(r, g, b, 'hs*')

        cl: float = c_min + c_max
        l: float = cl * 50

        if c_min == c_max:
            return (f"hsl(0, 0%, {l}%)", 0, 0, l)
	
        x: float = cg - cb if cr == c_min else cr - cg if cb == c_min else cb - cr
        y: float = 3 if cr == c_min else 1 if cb == c_min else 5

        h: float = 60 * (y - x / (c_max - c_min))

        cs: float = (c_max - c_min) / (2 - c_max - c_min) if (cl / 2) > 0.5 else (c_max - c_min) / (c_max + c_min)

        s: float = cs * 100

        as_string: str = f"hsl({h}, {s}%, {l}%)"

        return (as_string, h, s, l)
