from typing_extensions import Union
from .interface import Date_Object, Date_Format
from .switch import FauxSwitch

switch = FauxSwitch().switch

day_dict = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

month_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

ordinals = {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd", 31: "st"}


def parse_date(
    month_day: int,
    week_day: int,
    month: int,
    year: int,
    c_format: Date_Format = "none",
    american: bool = False,
) -> Union[Date_Object, str, bool]:
    """
    Get formated dates ready for a DB or frontend

    Args:
                month_day: the day of the month; `dt.day`
        week_day: the day of the week; `d.weekday()`
        month: the month as a number; `d.month`
        year: the full year; `d.year`
        c_format optional; `n` - numeric, `s` - shorthand text, `l` - full text
        american: optional; whether you want the date to be formatted in the American style

    Returns:
        if no format is provided it will return a `DateObject` object with metadata about the date, else it will return a string in your chosen format
    """
    date_dict: Date_Object = {
        "day": {
            "long": "N/A" if week_day > 6 or week_day < 0 else day_dict[week_day],
            "week_number": -1 if week_day > 6 or week_day < 0 else week_day + 1,
            "month_number": -1 if month_day > 31 or month_day < 1 else month_day,
            "ordinal_month": "N/A"
            if month_day > 31 or month_day < 1
            else ordinals[month_day]
            if month_day in ordinals
            else "th",
            "ordinal_week": "N/A"
            if week_day > 6 or week_day < 1
            else ordinals[week_day + 1]
            if week_day + 1 in ordinals
            else "th",
            "short": "N/A" if week_day > 6 or week_day < 1 else day_dict[week_day][0:3],
        },
        "month": {
            "long": "N/A" if month > 12 or month < 1 else month_dict[month],
            "number": -1 if month > 12 or month < 1 else month,
            "ordinal": "N/A"
            if month > 12 or month < 1
            else ordinals[month]
            if month in ordinals
            else "th",
            "short": "N/A" if month > 12 or month < 1 else month_dict[month][0:3],
        },
        "year": {"short": int(f"{year}"[2:4]), "long": year},
    }

    if c_format == "none":
        return date_dict
    else:
        return switch(c_format, date_dict, american)
