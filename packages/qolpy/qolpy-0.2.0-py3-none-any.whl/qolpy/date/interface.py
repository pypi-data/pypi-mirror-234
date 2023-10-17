from typing_extensions import TypedDict, Literal


class Day_Object(TypedDict):
    short: str
    """The shorthand text version of day"""
    long: str
    """The long text version of day"""
    ordinal_month: str
    """The ordinal of the number version of the month day"""
    ordinal_week: str
    """The ordinal of th enumber version of the week day"""
    week_number: int
    """The number param of the weekday"""
    month_number: int
    """The number param of the month day"""


class Month_Object(TypedDict):
    """An object containing month options for the date"""

    short: str
    """The shorthand text cersion of the month"""
    long: str
    """The long text version of the month"""
    ordinal: str
    """The ordinal of the number version of the month"""
    number: int
    """The numeric version of the month"""


class Year_Object(TypedDict):
    short: int
    """The shorthand version of the year"""
    long: int
    """The long version of the year"""


class Date_Object(TypedDict):
    """An object containing multiple options for the date"""

    day: Day_Object
    """An object containng day options for the date"""
    month: Month_Object
    """An object containing month options for the date"""
    year: Year_Object
    """An object containing year options for the date"""


Date_Format = Literal[
    "nns", "nnl", "sss", "ssl", "lll", "nss", "nsl", "nls", "nll", "none"
]
