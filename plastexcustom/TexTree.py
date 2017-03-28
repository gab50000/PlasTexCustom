import codecs
import os
import sys

from plasTeX.TeX import TeX

from plastexcustom import packages


custom_package_dir = os.path.dirname(packages.__file__)
sys.path = [custom_package_dir] + sys.path


class Tree:
    def __init__(self, node, children, height, print_text=False):
        self.node = node
        self.name = node.nodeName
        self.children = children
        self.char_width = len(self.name)  # width of name string
        self.height = height
        self.print_text = print_text
        if hasattr(node, "__unicode__"):
            self.text = node.__unicode__()
        else:
            self.text = ""
        if self.children:
            self.max_char_width = sum([child.max_char_width for child in self.children])
        else:
            if self.text:
                self.max_char_width = len(self.text)
            else:
                self.max_char_width = len(self.name)

    def __repr__(self):
        repr = []
        rows = self.get_tree_rows()
        for r in reversed(rows):
            repr.append(" ".join(r).center(self.max_char_width))
        return "\n".join(repr)

    def __getattr__(self, item):
        if not hasattr(self, item):
            return getattr(self.node, item)

    def __getitem__(self, item):
        return self.node.__getitem__(item)

    def get_tree_rows(self, rows=None):
        if not rows:
            rows = [[] for i in range(self.height)]
            starting_point = True
        else:
            starting_point = False
        rows[self.height - 1].append(self.text if self.text else "<" + self.name + ">")
        if self.children:
            for c in self.children:
                Tree.get_tree_rows(c, rows)

        if starting_point:
            return rows


def print_tree(node, level=0):
    print 4 * level * " ", node.name
    for child in node.children:
        print_tree(child, level=level+1)
    print ""


def print_node(node, level=0):
    print 4 * level * " ", node.nodeName
    for child in node.childNodes:
        print_node(child, level=level+1)
    print ""


def walk_tree(node):
    if node.hasChildNodes():
        children = [walk_tree(child) for child in node.childNodes]
        height = max((c.height for c in children)) + 1
    else:
        children = []
        height = 1

    return Tree(node, children, height)


def get_parents(node):
    if node.parentNode is not None:
        return  get_parents(node.parentNode) + [node.parentNode]
    else:
        return []


def find_formatter_class(parents_list):
    formatters = {"tiny", "scriptsize", "footnotesize", "small", "normalsize",
                  "large", "Large", "LARGE", "huge", "Huge", "it"}

    style = []
    for parent in parents_list:
        parent_name = parent.__class__.__name__
        if parent_name in formatters:
            style.append(parent_name)
    return " ".join(style)


def main():
    # Determine name of XML output
    filename_root, ext = os.path.splitext(sys.argv[1])
    xml_filename = filename_root + ".xml"

    # Instantiate a TeX processor and parse the input text
    tex = TeX()
    tex.ownerDocument.config['files']['split-level'] = -100
    tex.ownerDocument.config['files']['filename'] = xml_filename
    tex.ownerDocument.config['images']['imager'] = 'gspdfpng'

    with codecs.open(sys.argv[1], "r", encoding="utf-8") as f:
        file_content = f.read()

    tex.input(file_content)
    document = tex.parse()
    import ipdb; ipdb.set_trace()
