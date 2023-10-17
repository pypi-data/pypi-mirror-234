from functools import reduce

def abbreviate(text: str, delimiter: str = " ", reverse: bool = False) -> str:
    """
    Make an abbreviation from a string.

    Args:
        txt: The string you wish to abbreviate.
        delimiter: The char/string that differentiates one word from another.
        reverse: A boolean option to reverse the return string.

    Returns:
        An uppercased abbreviation of the string.
    """    
    text_list: list[str] = text.split(delimiter)

    if reverse:
        text_list.reverse()
    
    initials: str = reduce(lambda iteration, word: iteration + word[0], text_list, "")

    return initials.upper()

def to_title_case(text: str, delimiter: str = " ") -> str:
    """
    Make a string title case.

    Args:
        txt: the string to title case.
        delimiter: is the char/string that differentiates one word from another.

    Returns:
        a title cased string
    """
    cleaned_text: str = text.lower()
    text_list: list[str] = cleaned_text.split(delimiter)
    text_list = [string.capitalize() for string in text_list]

    return delimiter.join(text_list)

def to_sentence_case (text: str, delimiter: str = " ") -> str:
    """
    Make a string sentence case.
    
    Args:
        txt: the text to title.
        delimiter:  is the char/string that differentiates one word from another.

    Returns:
        a sentence cased string
    """
    cleaned_text: str = text.lower()
    text_list: list[str] = cleaned_text.split(delimiter)

    whitelist: list[str] = [".", "!", "?", ":", ";"]
    i: int = 0

    for string in text_list:
        prev_string: str = " " if i == 0 else text_list[i - 1]
        prev_char: str = prev_string[-1]

        if i == 0:
            text_list[i] = string.capitalize()
        elif prev_char in whitelist:
            text_list[i] = string.capitalize()
        elif string == "i":
            text_list[i] = "I"
        elif string.find("i'm") != -1:
            index: int = string.find("i'm")
            begin: str = string[0:index - 3]
            end: str = string[index + 3:]
            text_list[i] = begin + "I'm" + end

        i += 1

    return delimiter.join(text_list)
