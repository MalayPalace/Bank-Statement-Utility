import sys


def remove_comma(value: str):
    if value:
        return value.replace(",", "")
    return value


def append_str(text: str, append_text: str):
    if text and append_text:
        return text + append_text
    return text


def is_ui_execution():
    execution_path_list = sys.argv[0].split("/")
    value = execution_path_list[len(execution_path_list) - 1]

    if "main_ui.py".__eq__(value):
        return True
    return False
