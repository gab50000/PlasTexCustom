# coding=utf-8
"""Hauptskript, das zuerst den Parser aufruft, und anschließend den Dokumentenbaum mithilfe des
custom_renderers sowie der hier definierten Funktionen rendert."""

import sys
import os
import codecs

from plasTeX.TeX import TeX
from plasTeX.ConfigManager import ConfigManager

from lxml import etree

from plastexcustom import packages
from custom_renderer import Renderer
from TexTree import walk_tree, print_tree, print_node, get_parents, find_formatter_class

custom_package_dir = os.path.dirname(packages.__file__)
sys.path = [custom_package_dir] + sys.path

c = ConfigManager()
c.add_section("debugging")
c["debugging"]["verbose"] = "True"


# Hier werden die Funktionen definiert, die das XML Ausgabeformat für jeden Latex-Befehl bestimmen.

def convert_edtext(node):
    """Rendert das edtext Kommando in der Form 
    <edtext><text> ... </text><app> ... </app></edtext>"""
    return u'<edtext><text>{}</text><app>{}</app></edtext>'.format(
        unicode(node.attributes["text"]), unicode(node.attributes["content"]))


def do_nothing(node):
    """Diese Funktion gibt einen leeren (Unicode-) String zurück.
    Kann benutzt werden, um unnötige Elemente aus der XML-Datei zu entfernen."""
    return u''


def convert_graphics(node):
    return u"<graphics>\n<file>\n{}\n</file>\n</graphics>".format(node.attributes["file"])


def handle_equation(node):
    return u'<formula>{}</formula>'.format(node.image.url)


def handle_macro(node):
    import ipdb; ipdb.set_trace


def open_paragraph(node):
    parents = get_parents(node)
    style = find_formatter_class(parents)
    if style:
        return u'<p size="{}">'.format(style)
    return u"<p>"


def end_paragraph(node):
    return u"</p>"


def textsize(node):
    return u'<v size="{}">{}</v>'.format(node.nodeName, unicode(node))


def main(*args):
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

    # Render the document
    renderer = Renderer()

    #renderer["tiny"] = textsize
    #renderer["scriptsize"] = textsize
    #renderer["footnotesize"] = textsize
    #renderer["small"] = textsize
    #renderer["normalsize"] = textsize
    #renderer["large"] = textsize
    #renderer["Large"] = textsize
    #renderer["LARGE"] = textsize
    #renderer["huge"] = textsize
    #renderer["Huge"] = textsize

    renderer["edtext"] = convert_edtext
#    renderer["Afootnote"] = convert
#    renderer["Bfootnote"] = convert
#    renderer["Cfootnote"] = convert
#    renderer["lemma"] = convert
    renderer["pstart"] = open_paragraph
    renderer["pend"] = end_paragraph
    #renderer["includegraphics"] = handle_equation
    renderer["vspace"] = do_nothing
    renderer["renewcommand"] = do_nothing
    #renderer["math"] = handle_equation
    #renderer["displaymath"] = handle_equation
    #renderer["eqnarray"] = handle_equation
    #renderer["equation"] = handle_equation
    #renderer["pleibvdash"] = handle_macro
    renderer.render(document)

    # Make XML pretty
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(xml_filename, parser)
    tree.write(xml_filename, pretty_print=True)

