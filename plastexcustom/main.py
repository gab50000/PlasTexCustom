# coding=utf-8
"""Hauptskript, das zuerst den Parser aufruft, und anschließend den Dokumentenbaum mithilfe des
custom_renderers sowie der hier definierten Funktionen rendert."""

import sys
import os
import codecs

from plasTeX.TeX import TeX
from plasTeX.ConfigManager import ConfigManager

from lxml import etree
from xml.sax.saxutils import escape, unescape

from plastexcustom import packages
from custom_renderer import Renderer
from TexTree import walk_tree, print_tree, print_node, get_parents, find_formatter_class

custom_package_dir = os.path.dirname(packages.__file__)
sys.path.insert(0, custom_package_dir)

c = ConfigManager()
c.add_section("debugging")
c["debugging"]["verbose"] = "True"


#---------------------------------------------------------------------------------------------------
# Hier werden die Funktionen definiert, die das XML Ausgabeformat für jeden Latex-Befehl bestimmen.

def convert_edtext(node):
    """Rendert das edtext Kommando in der Form 
    <edtext><text> ... </text><app> ... </app></edtext>"""
    return u'<edtext><text>{}</text><app>{}</app></edtext>'.format(
        unicode(node.attributes["text"]), unicode(node.attributes["content"]))


def do_nothing(node):
    """Diese Funktion gibt einen leeren (Unicode-) String zurück.
    Kann benutzt werden, um zu verhindern, dass unnötige Elemente in der XML-Datei auftauchen."""
    return u''


def do_not_write_tags(node):
    """Schreibt den Inhalt des aktuellen Environments/Befehls nach XML, aber erzeugt keine Tags
    dafür"""
    return unicode(node)


def convert_graphics(node):
    return u"<graphics>\n<file>\n{}\n</file>\n</graphics>".format(unicode(node.attributes["file"]))


def equation_as_latexsrc_with_image(node):
    """Funktion, um Mathe-Umgebungen umzuwandeln. 
    Im <src> Tag wird die Original Latex-Formel angezeigt, während <imgpath> den Pfad zum erstellten
    Formelbild enthält.
    Anmerkung: Bilder werden nicht erstellt. Plastex-Bug?"""
    src_content = escape(unicode(node.source))
    img_path = escape(unicode(node.image.url))
    return u'<formula><src>{}</src> <imgpath>{}</imgpath></formula>'.format(src_content, img_path)


def equation_as_latexsrc(node):
    """Wie equation_as_latexsrc_with_image, aber ohne <imgpath>...</imgpath>"""
    src_content = escape(unicode(node.source))
    return u'<formula><src>"{}"</src></formula>'.format(src_content)


def open_paragraph(node):
    """Öffnet einen Paragraphen mittels <p>"""
    parents = get_parents(node)
    style = find_formatter_class(parents)
    if style:
        return u'<p size="{}">'.format(style)
    return u"<p>"


def end_paragraph(node):
    """Schließt einen Paragraphen mittels </p>"""
    return u"</p>"


def textsize(node):
    return u'<v size="{}">{}</v>'.format(node.nodeName, unicode(node))


#---------------------------------------------------------------------------------------------------


def main(*args):
    # Determine name of XML output
    filename_root, ext = os.path.splitext(sys.argv[1])
    xml_filename = filename_root + ".xml"

    # Instantiate a TeX processor and parse the input text
    tex = TeX()
    tex.ownerDocument.config['files']['split-level'] = -100
    tex.ownerDocument.config['files']['filename'] = xml_filename
    tex.ownerDocument.config['images']['imager'] = 'gspdfpng'
    tex.ownerDocument.config['images']['filenames'] = 'xmlimages/img-$num(4)'

    with codecs.open(sys.argv[1], "r", encoding="utf-8") as f:
        file_content = f.read()

    tex.input(file_content)
    document = tex.parse()

    renderer = Renderer()

    # Alle in textsizes enthaltenen Latex-Befehle werden nicht gerendert

    textsizes = ["tiny", "scriptsize", "footnotesize", "small", "normalsize", "large", "Large",
                 "LARGE", "huge", "Huge"]

    for ts in textsizes:
        renderer[ts] = do_not_write_tags

    # Alle Latex-Befehle, die in der folgenden Liste stehen, werden nicht ins XML-Dokument
    # geschrieben
    # Bei Bedarf ergänzen!

    to_be_ignored = ["vspace", "renewcommand", "pstart", "pend"]
    for tbi in to_be_ignored:
        renderer[tbi] = do_nothing

    # Alle Formelbefehle und Environments kommen in die folgende Liste

    math_envs = ["math", "displaymath", "eqnarray", "equation"]
    for me in math_envs:
        renderer[me] = equation_as_latexsrc

    renderer["edtext"] = convert_edtext
    renderer["includegraphics"] = convert_graphics

    # Render the document
    renderer.render(document)

    # Make XML pretty
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(xml_filename, parser)
    tree.write(xml_filename, pretty_print=True)

