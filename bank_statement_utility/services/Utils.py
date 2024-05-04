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

    # Considering both cases of whether UI started through installed module or through python main_ui
    if "main_ui".__contains__(value) or "bank_statement_utility_ui".__contains__(value):
        return True
    return False
