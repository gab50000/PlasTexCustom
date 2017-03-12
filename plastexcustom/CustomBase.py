from plasTeX import Base


def has_formatting(node):
    return hasattr(node.attributes, "formatting")


class Environment(Base.Environment):
    def digest(self, tokens):
        Base.Environment.digest(self, tokens)
        parent = self.parentNode
        while parent:
            if has_formatting(parent):
                self.attributes["formatting"].update(self.parentNode.attributes["formatting"])
                break
            else:
                parent = parent.parentNode


class Command(Base.Command):
    def digest(self, tokens):
        Base.Command.digest(self, tokens)
        parent = self.parentNode
        while parent:
            if has_formatting(parent):
                self.attributes["formatting"].update(self.parentNode.attributes["formatting"])
                break
            else:
                parent = parent.parentNode
