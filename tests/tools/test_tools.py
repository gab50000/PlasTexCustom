import logging

from plastexcustom.tools import paragraph_checker


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_get_line_of_charpos():
    text = 5 * "\n" + "a"
    line = paragraph_checker.get_line_of_charpos(text, 5)
    print(line)