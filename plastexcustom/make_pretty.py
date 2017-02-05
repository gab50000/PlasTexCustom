import os
import sys

from lxml import etree


def main(*args):
    filename = sys.argv[1]
    root, ext = os.path.splitext(filename)
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(filename, parser)
    tree.write(root + "_pretty" + ext, pretty_print=True)