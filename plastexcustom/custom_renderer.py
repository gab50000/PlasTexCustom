import string
from plasTeX.Renderers import Renderer

from plastexcustom.TexTree import find_formatter_class, get_parents


class Renderer(Renderer):

    def default(self, node):
        """ Rendering method for all non-text nodes """
        s = []

        # Handle characters like \&, \$, \%, etc.
        if len(node.nodeName) == 1 and node.nodeName not in string.letters:
            return self.textDefault(node.nodeName)

        # Handle Latex macros
        if node.macroName:
            return self.textDefault(node.nodeName)

        # Start tag

        # Find parents and check for formatting


        s.append('<%s>' % node.nodeName)
        # See if we have any attributes to render
        if node.hasAttributes():
            for key, value in node.attributes.items():
                # Remove non alphanumeric characters
                if not key.isalnum():
                    key = "".join(char for char in key if char.isalnum())
                # If the key is 'self', don't render it
                # these nodes are the same as the child nodes
                if key == 'self':
                    continue
                s.append('<%s>%s</%s>' % (key, unicode(value), key))

        # Invoke rendering on child nodes
        s.append(unicode(node))

        # End tag
        s.append('</%s>' % node.nodeName)

        return u'\n'.join(s)

    def textDefault(self, node):
        """ Rendering method for all text nodes """
        return node.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
