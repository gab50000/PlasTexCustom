# coding=utf-8
# TODO: Use plastex.Imagers.Imager to generate equation images

import sys
import os
import codecs

from plasTeX.TeX import TeX
from plasTeX.ConfigManager import ConfigManager

from plastexcustom import packages
from custom_renderer import Renderer

custom_package_dir = os.path.dirname(packages.__file__)
sys.path = [custom_package_dir] + sys.path

c = ConfigManager()
c.add_section("debugging")
c["debugging"]["verbose"] = "True"


# Hier werden die Funktionen definiert, die das XML Ausgabeformat für jeden Latex-Befehl bestimmen.

def convert(node):
    """Default Konvertierung.
    Setzt den Nodenamen (also den Namen des jeweiligen Latexbefehls) in Tags. Dazwischen wird das
    Text Attribut geschrieben."""
    if "formatting" in node.attributes:
        formatting = u", ".join(node.attributes["formatting"])
    else:
        formatting = u""
    return u'<{} formatting="{}">{}</{}>'.format(
        node.nodeName, formatting, unicode(node.attributes["text"]), node.nodeName)


def convert_edtext(node):
    return u'<edtext><text>{}</text><app>{}</app></edtext>'.format(
        unicode(node.attributes["text"]), unicode(node.attributes["content"]))


def do_nothing(node):
    return u''


def convert_graphics(node):
    return u"<graphics>\n<file>\n{}\n</file>\n</graphics>".format(node.attributes["file"])


def handle_equation(node):
    return u'<formula>{}</formula>'.format(node.image.url)


def handle_macro(node):
    import ipdb; ipdb.set_trace


def open_paragraph(node):
    return u"<p>"


def end_paragraph(node):
    return u"</p>"


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

    import ipdb; ipdb.set_trace()
    tex.input(file_content)
    document = tex.parse()

    # Render the document
    renderer = Renderer()
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

