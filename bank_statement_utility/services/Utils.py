def remove_comma(value: str):
    if value:
        return value.replace(",", "")
    return value


def append_str(text: str, append_text: str):
    if text and append_text:
        return text + append_text
    return text
