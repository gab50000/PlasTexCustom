# coding=utf-8
"""Erstellt ein simples Tex-File mit Fülltext."""

import os
import sys

from loremipsum import get_sentences


TEX_CONTENT = """
\documentclass{{scrbook}}
\usepackage{{amsmath}}
\usepackage{{graphicx}}

\\begin{{document}}
{}
\end{{document}}
"""



def main():
    test_name = sys.argv[1]
    if os.path.exists(test_name):
        print >> sys.stderr, "Directory already exists. Aborting..."
        sys.exit(1)

    os.mkdir(test_name)
    tex_path = os.path.join(test_name, "test.tex")

    with open(tex_path, "w") as f:
        lorem_content = "".join(get_sentences(10))
        print >> f, TEX_CONTENT.format(lorem_content)


