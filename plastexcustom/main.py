# coding=utf-8
"""Hauptskript, das zuerst den Parser aufruft, und anschließend den Dokumentenbaum mithilfe des
custom_renderers sowie der hier definierten Funktionen rendert."""

import argparse
import logging
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


logger = logging.getLogger(__name__)

#---------------------------------------------------------------------------------------------------
# Hier werden die Funktionen definiert, die das XML Ausgabeformat für jeden Latex-Befehl bestimmen.

def convert_edtext(node):
    """Rendert das edtext Kommando in der Form 
    <edtext><text> ... </text><app> ... </app></edtext>"""
    node_text = unicode(node.attributes["text"])
    node_content = unicode(node.attributes["content"])
    logger.debug(u'Converting node with text "{}" and content "{}"'.format(node_text, node_content))
    return u'<edtext><text>{}</text><app>{}</app></edtext>'.format(node_text, node_content)


def do_nothing(node):
    """Diese Funktion gibt einen leeren (Unicode-) String zurück.
    Kann benutzt werden, um zu verhindern, dass unnötige Elemente in der XML-Datei auftauchen."""
    logger.debug(u"Return empty string for node {}".format(node.nodeName))
    return u''


def debug(node):
    import ipdb; ipdb.set_trace()


def do_not_write_tags(node):
    """Schreibt den Inhalt des aktuellen Environments/Befehls nach XML, aber erzeugt keine Tags
    dafür"""
    logger.debug(u"Do not write tags for node {}".format(node.nodeName))
    return unicode(node)


def convert_graphics(node):
    filename = unicode(node.attributes["file"])
    logger.debug(u"Convert {} to Image {}".format(node.nodeName, filename))
    return u"<graphics>\n<file>\n{}\n</file>\n</graphics>".format(filename)


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
    return u"\n<p>\n"


def close_paragraph(node):
    """Schließt einen Paragraphen mittels </p>"""
    return u"\n</p>\n"


def textsize(node):
    return u'<v size="{}">{}</v>'.format(node.nodeName, unicode(node))


def eszett(node):
    return u"ß"


#---------------------------------------------------------------------------------------------------


def main(*args):
    parser = argparse.ArgumentParser("Convert tex to XML")
    parser.add_argument("filename", help="Latex-Filename")
    parser.add_argument("--pretty", action="store_true", help="Prettify output")
    parser.add_argument("--loglevel", "-l", default="INFO",
                        choices=["info", "INFO", "debug", "DEBUG", "warn", "WARN"],
                        help="Set log level")
    args = parser.parse_args()

    logger.setLevel(getattr(logging, args.loglevel.upper()))
    logger.info("Log level set to {}".format(args.loglevel))
    # Determine name of XML output
    filename_root, ext = os.path.splitext(sys.argv[1])
    xml_filename = filename_root + ".xml"

    # Instantiate a TeX processor and parse the input text
    tex = TeX()
    tex.ownerDocument.config['files']['split-level'] = -100
    tex.ownerDocument.config['files']['filename'] = xml_filename
    tex.ownerDocument.config['images']['imager'] = 'gspdfpng'
    tex.ownerDocument.config['images']['filenames'] = 'xmlimages/img-$num(4)'
    tex.ownerDocument.config['images']['save-file'] = "on"

    with codecs.open(sys.argv[1], "r", encoding="utf-8") as f:
        file_content = f.read()

    tex.input(file_content)
    document = tex.parse()

    renderer = Renderer()

    # Alle in textsizes enthaltenen Latex-Befehle werden nicht gerendert

    textsizes = ["tiny", "scriptsize", "footnotesize", "small", "normalsize", "large", "Large",
                 "LARGE", "huge", "Huge"]

    other = ["count", "setcounter"]

    for ts in textsizes:
        renderer[ts] = do_not_write_tags

    for ot in other:
        renderer[ot] = do_not_write_tags

    # Alle Latex-Befehle, die in der folgenden Liste stehen, werden nicht ins XML-Dokument
    # geschrieben
    # Achtung: gilt auch für alle enthaltenen Kindknoten
    # Bei Bedarf ergänzen!

    to_be_ignored = ["vspace", "renewcommand"]

    for tbi in to_be_ignored:
        renderer[tbi] = do_nothing

    # Alle Formelbefehle und Environments kommen in die folgende Liste

    math_envs = ["math", "displaymath", "eqnarray", "equation"]
    for me in math_envs:
        renderer[me] = equation_as_latexsrc

    renderer["edtext"] = convert_edtext
    renderer["includegraphics"] = convert_graphics
    renderer["pstart"] = open_paragraph
    renderer["pend"] = close_paragraph

    renderer["ss"] = debug

    # Render the document
    renderer.render(document)

    if args.pretty:
        logger.info("Make XML document pretty")
        # Make XML pretty
        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(xml_filename, parser)
        tree.write(xml_filename, pretty_print=True)

