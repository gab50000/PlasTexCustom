import sys
import re
import codecs
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    filename = sys.argv[1]
    with codecs.open(filename, "r", encoding="utf-8") as f:
        content = "".join(line for line in f if not line.lstrip().startswith("%"))
    pstart_matches = re.finditer(r"\\pstart", content)
    pend_matches = re.finditer(r"\\pend", content)
    pstart_positions = (m.start() for m in pstart_matches)
    pend_positions = (m.start() for m in pend_matches)
    matches = sorted(list(pstart_matches) + list(pend_matches), key=lambda m: m.start())
    counter = [1 if m.group() == u"\\pstart" else -1 for m in matches]

    summe = 0
    for i, x in enumerate(counter):
        summe += x
        if summe < 0:
            logger.warn("pstart tags do not match pend tags!")
            break
    else:
        logger.info("Everything is fine")


