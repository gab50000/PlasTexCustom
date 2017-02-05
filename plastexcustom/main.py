# TODO: Use plastex.Imagers.Imager to generate equation images

import sys
import os
import codecs

from plasTeX.TeX import TeX
from plasTeX.ConfigManager import ConfigManager

from plastexcustom import packages
from custom_renderer import Renderer

sys.path.append(os.path.dirname(packages.__file__))

c = ConfigManager()
c.add_section("debugging")
c["debugging"]["verbose"] = "True"


def convert(node):
    return u'<{}>{}</{}>'.format(node.nodeName, unicode(node.attributes["text"]), node.nodeName)


def convert_edtext(node):
    return u'<edtext><text>{}</text><app>{}</app></edtext>'.format(
        unicode(node.attributes["text"]), unicode(node.attributes["content"]))


def do_nothing(node):
    return u''


def convert_graphics(node):
    return u"<graphics>\n<file>\n{}\n</file>\n</graphics>".format(node.attributes["file"])


def main(*args):
    # Instantiate a TeX processor and parse the input text
    tex = TeX()
    tex.ownerDocument.config['files']['split-level'] = -100
    tex.ownerDocument.config['files']['filename'] = 'test.xml'

    with codecs.open(sys.argv[1], "r", encoding="utf-8") as f:
        file_content = f.read()

    tex.input(file_content)
    document = tex.parse()

    # Render the document
    renderer = Renderer()
    renderer["edtext"] = convert_edtext
    renderer["Afootnote"] = convert
    renderer["Bfootnote"] = convert
    renderer["Cfootnote"] = convert
    renderer["lemma"] = convert
    renderer["includegraphics"] = convert_graphics
    renderer["vspace"] = do_nothing
    renderer["renewcommand"] = do_nothing
    renderer.render(document)

