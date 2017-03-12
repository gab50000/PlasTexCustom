from plastexcustom import CustomBase as Base


class pleibvdash(Base.Command):
    args = "self"
    def digest(self, tokens):
        self.image_path = u"images/abc"


class footnotesize(Base.Command):
    args = ""

    def digest(self, tokens):
        Base.Command.digest(self, tokens)
        self.attributes["formatting"] = {"font": "footnotesize"}


class tiny(Base.Command):
    args = ""

    def digest(self, tokens):
        self.attributes["formatting"] = {"font": "tiny"}
