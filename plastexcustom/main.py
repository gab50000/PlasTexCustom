# TODO: Use plastex.Imagers.Imager to generate equation images

import sys

from plasTeX.TeX import TeX
from plasTeX.ConfigManager import ConfigManager

from custom_renderer import Renderer


c = ConfigManager()
c.add_section("debugging")
c["debugging"]["verbose"] = "True"

def convert(node):
    return u'<{}>{}</{}>'.format(node.nodeName, node.attributes["text"], node.nodeName)


def convert_edtext(node):
    return u'<edtext><text>{}</text><content>{}</content>'.format(
        node.attributes["text"], node.attributes["content"])


def main(*args):
    # Instantiate a TeX processor and parse the input text
    tex = TeX()
    tex.ownerDocument.config['files']['split-level'] = -100
    tex.ownerDocument.config['files']['filename'] = 'test.xml'
    
    with open(sys.argv[1], "r") as f:
        file_content = f.read()
    
    tex.input(file_content)
    document = tex.parse()

    # Render the document
    renderer = Renderer()
    renderer["edtext"] = convert_edtext
    renderer["Afootnote"] = convert
    renderer["Bfootnote"] = convert
    renderer.render(document)

