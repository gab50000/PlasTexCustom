import sys
import re
import codecs
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_line_of_charpos(text, charpos):
    matches = [m.start() for m in re.finditer(r"$", text, flags=re.MULTILINE)]
    logger.debug(matches)
    # If charpos is before first line break, line number is 1
    if charpos < matches[0]:
        return 1
    for (i, m1), m2 in zip(enumerate(matches[:-1], start=1), matches[1:]):
        if m1 < charpos < m2:
            return i + 1


def main():
    start_exp = re.compile(r"\\pstart")
    end_exp = re.compile(r"\\pend")
    filename = sys.argv[1]
    with codecs.open(filename, "r", encoding="utf-8") as f:
        # Get all lines which are not comments
        lines = f.readlines()
    # Join lines to one string
    content = "".join(lines)
    content_stripped = "".join(line for line in lines if not line.lstrip().startswith("%"))
    pstart_matches = re.finditer(start_exp, content_stripped)
    pend_matches = re.finditer(end_exp, content_stripped)
    matches = sorted(list(pstart_matches) + list(pend_matches), key=lambda m: m.start())
    counter = [1 if m.group() == u"\\pstart" else -1 for m in matches]

    summe = 0
    for i, x in enumerate(counter):
        summe += x
        if summe < 0 or summe > 1:
            logger.warn("pstart tags do not match pend tags!")
            problem_line = get_line_of_charpos(content, matches[i].start())
            logger.warn("Offending line: {}".format(problem_line))
            break
    else:
        logger.info("Everything is fine")


