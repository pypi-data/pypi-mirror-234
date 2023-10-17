from yattag import Doc


def noun(name: str, num: int) -> str:
    """
    This function returns a noun in it's right for a specific quantity
    :param name:
    :param num:
    :return:
    """
    if num == 0 or num > 1:
        return name + "s"
    return name


class HtmlGen:
    def __init__(self):
        document, tag, text, line = Doc().ttl()
        self.document = document
        self.tag = tag
        self.text = text
        self.line = line
