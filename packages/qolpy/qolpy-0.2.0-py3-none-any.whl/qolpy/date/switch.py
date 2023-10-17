from typing_extensions import Union, Any
from .interface import Date_Object, Date_Format


class FauxSwitch(object):
    """A switch to create parsed dates"""

    def switch(
        self, c_format: Date_Format, date_dict: Date_Object, american: bool
    ) -> Union[Any, bool]:
        formated_format: str = f"__{c_format}__"
        date_switch = getattr(
            self, formated_format, lambda date_dict=date_dict, american=american: False
        )
        return date_switch(date_dict, american)

    def __lll__(self, date_dict: Date_Object, american: bool) -> str:
        return f"{date_dict['day']['long']} {date_dict['day']['month_number']}{date_dict['day']['ordinal_month']} {date_dict['month']['long']}, {date_dict['year']['long']}".strip()

    def __nll__(self, date_dict: Date_Object, american: bool) -> str:
        if american:
            return f"{date_dict['month']['long']} {date_dict['day']['month_number']} {date_dict['year']['long']}".strip()
        else:
            return f"{date_dict['day']['month_number']} {date_dict['month']['long']} {date_dict['year']['long']}".strip()

    def __nls__(self, date_dict: Date_Object, american: bool) -> str:
        if american:
            return f"{date_dict['month']['long']} {date_dict['day']['month_number']} {date_dict['year']['short']}".strip()
        else:
            return f"{date_dict['day']['month_number']} {date_dict['month']['long']} {date_dict['year']['short']}".strip()

    def __nnl__(self, date_dict: Date_Object, american: bool) -> str:
        if american:
            return f"{date_dict['month']['number']} {date_dict['day']['month_number']} {date_dict['year']['long']}".strip()
        else:
            return f"{date_dict['day']['month_number']} {date_dict['month']['number']} {date_dict['year']['long']}".strip()

    def __nns__(self, date_dict: Date_Object, american: bool) -> str:
        if american:
            return f"{date_dict['month']['number']} {date_dict['day']['month_number']} {date_dict['year']['short']}".strip()
        else:
            return f"{date_dict['day']['month_number']} {date_dict['month']['number']} {date_dict['year']['short']}".strip()

    def __nsl__(self, date_dict: Date_Object, american: bool) -> str:
        if american:
            return f"{date_dict['month']['short']} {date_dict['day']['month_number']} {date_dict['year']['long']}".strip()
        else:
            return f"{date_dict['day']['month_number']} {date_dict['month']['short']} {date_dict['year']['long']}".strip()

    def __nss__(self, date_dict: Date_Object, american: bool) -> str:
        if american:
            return f"{date_dict['month']['short']} {date_dict['day']['month_number']} {date_dict['year']['short']}".strip()
        else:
            return f"{date_dict['day']['month_number']} {date_dict['month']['short']} {date_dict['year']['short']}".strip()

    def __ssl__(self, date_dict: Date_Object, american: bool) -> str:
        return f"{date_dict['day']['short']} {date_dict['day']['month_number']} {date_dict['month']['short']}, {date_dict['year']['long']}".strip()

    def __sss__(self, date_dict: Date_Object, american: bool) -> str:
        return f"{date_dict['day']['short']} {date_dict['day']['month_number']} {date_dict['month']['short']}, {date_dict['year']['short']}".strip()
