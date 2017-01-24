# Import renderer from previous code sample
import sys

from plasTeX.TeX import TeX

from custom_renderer import Renderer


def convert(node):
    return u'<{}>\n{}\n</{}>'.format(node.nodeName, unicode(node.attributes["text"].textContent), node.nodeName)


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
    renderer["edtext"] = convert
    renderer.render(document)
