from typing_extensions import Union
from .interface import Number_Setting

settings_dict = {
    "comma": ",",
    "space": " ",
    "punct": ".",
}


def num_parse(value: Union[int, str], setting: Number_Setting = "comma") -> str:
    """
    Send in a number and get back a parsed number... like its EXCEL!

    Args:
                value: the number you want to be mutated
        setting: the delimiter for the number

    Returns:
                the mutated number with delimiters as a string
    """
    divider: str = settings_dict[setting] if setting in settings_dict else setting

    decimal_index: int = str(value).find(".")
    decimal_value: str = str(value)[decimal_index + 1 :] if decimal_index > 0 else ""
    number: str = str(value)[:decimal_index] if decimal_index > 0 else str(value)

    number_list: list[str] = list(str(number))
    number_list.reverse()
    mutated_number: str = ""
    count: int = 0

    for num in number_list:
        if count == 3:
            mutated_number += divider
            count = 1
        else:
            count += 1

        mutated_number += num

    mutated_number_list: list[str] = list(mutated_number)
    mutated_number_list.reverse()
    delimited_number: str = "".join(mutated_number_list)

    if decimal_index > 0:
        delimited_number += (
            f",{decimal_value}"
            if divider == "punct" or divider == "."
            else f".{decimal_value}"
        )

    return delimited_number
