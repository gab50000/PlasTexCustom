# coding=utf-8
"""Hauptskript, das zuerst den Parser aufruft, und anschließend den Dokumentenbaum mithilfe des
custom_renderers sowie der hier definierten Funktionen rendert."""

import argparse
import logging
import sys
import os
import codecs
import subprocess

from plasTeX.TeX import TeX
from plasTeX.ConfigManager import ConfigManager

from lxml import etree
from xml.sax.saxutils import escape, unescape

import plastexcustom
from plastexcustom import packages
from custom_renderer import Renderer
from TexTree import walk_tree, print_tree, print_node, get_parents, find_formatter_class


c = ConfigManager()
c.add_section("debugging")
c["debugging"]["verbose"] = "True"


logger = logging.getLogger(__name__)


def read_tags(filename):
    """Liest XML Tags aus einer Datei <filename>.
    Sucht nach dieser Datei erst im aktuellen Verzeichnis (von dem aus das Skript aufgerufen wurde),
    danach im files Ordner des PlastexCustom Packages."""
    file_path = os.path.join(os.path.dirname(__file__), "files")
    for path in (".", file_path):
        try:
            with open(os.path.join(path, filename), "r") as f:
                tags = f.read().split()
        except IOError:
            logger.debug("Found no file {} in directory {}".format(filename,
                                                                   os.path.abspath(path)))
            continue
        logger.debug("Found file {} in directory {}".format(filename,
                                                            os.path.abspath(path)))
        logger.debug("Tags: {}".format(tags))
        return tags
    return []


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
    Kann benutzt werden, um zu verhindern, dass unnötige Elemente in der XML-Datei auftauchen.
    Achtung: Alle Kindesknoten werden dann auch nicht gerendert!"""
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
    return u"<p>"


def close_paragraph(node):
    """Schließt einen Paragraphen mittels </p>"""
    return u"</p>"


def textsize(node):
    return u'<v size="{}">{}</v>'.format(node.nodeName, unicode(node))


def eszett(node):
    return u"ß"


def textsuperscript(node):
    return u'<hi rendition="#sup">{}</hi>'.format(unicode(node))


def convert_section(node):
    form = u"<section> <title> {} </title>\n {} \n</section>\n"
    return form.format(node.title, u"".join(map(unicode, node.allChildNodes)))

#---------------------------------------------------------------------------------------------------
def validate(xml_filename):
    curdir = os.path.dirname(plastexcustom.__file__)
    relaxng_file = os.path.abspath(os.path.join(curdir, "files/basisformat.rng.xml"))
    logger.debug("Open RelaxNG file {}".format(relaxng_file))
    relaxng_doc = etree.parse(relaxng_file)
    relaxng = etree.RelaxNG(relaxng_doc)
    doc = etree.parse(xml_filename)
    relaxng.assertValid(doc)


def main(*args):
    parser = argparse.ArgumentParser("Convert tex to XML")
    parser.add_argument("filename", help="Latex-Filename")
    parser.add_argument("--pretty", action="store_true", help="Prettify output")
    parser.add_argument("--validate", action="store_true", help="Validate XML using "
                                                                "Relax NG schema")
    parser.add_argument("--loglevel", "-l", default="INFO",
                        choices=["info", "INFO", "debug", "DEBUG", "warn", "WARN"],
                        help="Set log level")
    parser.add_argument("--commit", action="store_true", help="Add commit hash to first line of "
                                                              "XML document")
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

    # Alle in der Datei IGNORE enthaltenen Latex-Befehlsnamen werden nicht gerendert
    tags_not_to_be_written = read_tags("IGNORE")
    for t in tags_not_to_be_written:
        renderer[t] = do_not_write_tags

    # Alle Latex-Befehle, die in der Datei REMOVE stehen, werden nicht ins XML-Dokument
    # geschrieben
    # Achtung: gilt auch für alle enthaltenen Kindknoten
    # Bei Bedarf ergänzen!
    to_be_removed = read_tags("REMOVE")

    for tbi in to_be_removed:
        renderer[tbi] = do_nothing

    # Alle Formelbefehle und Environments kommen in die folgende Liste
    math_envs = ["math", "displaymath", "eqnarray", "equation"]
    for me in math_envs:
        renderer[me] = equation_as_latexsrc

    renderer["edtext"] = convert_edtext
    renderer["includegraphics"] = convert_graphics
    renderer["pstart"] = open_paragraph
    renderer["pend"] = close_paragraph
    renderer["textsuperscript"] = textsuperscript
    renderer["section"] = convert_section

    renderer["ss"] = eszett

    # Render the document
    renderer.render(document)

    if args.commit:
        commit_hash = subprocess.check_output("git rev-parse HEAD".split()).strip()
        with open(xml_filename, "r") as f:
            content = f.readlines()
        with open(xml_filename, "w") as f:
            f.writelines(["<!-- Commit Hash: {} --> \n".format(commit_hash)] + content)

    if args.pretty:
        logger.info("Make XML document pretty")
        # Make XML pretty
        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(xml_filename, parser)
        tree.write(xml_filename, pretty_print=True)

    if args.validate:
        validate(xml_filename)


def validate_cli():
    xml_filename = sys.argv[1]
    validate(xml_filename)
