import sys
import re
import codecs
import logging


logger = logging.getLogger(__name__)


def get_line_of_charpos(text, charpos):
    linebreak_pos = [m.start() for m in re.finditer(r"$", text[:charpos + 1], flags=re.MULTILINE)]
    # Get number of comment lines before charpos
    for i, line in enumerate(text.splitlines()):
        logger.debug(u"{}: {}".format(i, line))
    logger.debug("Linebreak positions: {}".format(linebreak_pos))
    logger.debug("Charpos is {}".format(charpos))
    # If charpos is before first line break, line number is 1
    if charpos < linebreak_pos[0]:
        return 1
    for (i, m1), m2 in zip(enumerate(linebreak_pos[:-1], start=1), linebreak_pos[1:]):
        logger.debug("Checking line {} (pos {} - pos {}".format(i, m1, m2))
        if m1 < charpos < m2:
            logger.debug("{} < {} < {}".format(m1, charpos, m2))
            return i + 1


def check_single_file(filename, last_status=0):
    logger.info("Check file {}".format(filename))
    start_exp = re.compile(r"\\pstart")
    end_exp = re.compile(r"\\pend")
    with codecs.open(filename, "r", encoding="utf-8") as f:
        # Get all lines which are not comments
        lines = f.readlines()
    # Join lines to one string
    content = "".join(lines)

    status = last_status

    matches = []
    # position offset caused by removed comments
    offset = 0
    positions = []

    for line in lines:
        tmp_match = []
        if not line.lstrip().startswith("%"):
            start_match = re.search(start_exp, line)
            end_match = re.search(end_exp, line)
            if start_match:
                tmp_match.append(start_match)
            if end_match:
                tmp_match.append(end_match)
            tmp_match = sorted(tmp_match, key=lambda m: m.start())
            matches += tmp_match
            positions += [m.start() + offset for m in tmp_match]
        offset += len(line)

    counter = [1 if m.group() == u"\\pstart" else -1 for m in matches]
    logger.debug("Found positions: {}".format(positions))

    summe = 0

    for i, x in enumerate(counter):
        summe += x
        if summe < 0 or summe > 1:
            logger.warn("pstart tags do not match pend tags!")
            problem_line = get_line_of_charpos(content, positions[i])
            logger.warn("Offending line: {}".format(problem_line))
            sys.exit(1)

    if status == 0:
        logger.info("Everything is fine in file {}".format(filename))
    else:
        logger.info("One paragraph is still open at end of file {}".format(filename))

    return status


def main():
    logging.basicConfig(level=logging.INFO)
    filenames = sys.argv[1:]

    status = 0
    for fn in filenames:
        status = check_single_file(fn, last_status=status)
        logger.debug("Last status: {}".format(status))
