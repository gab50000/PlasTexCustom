from plasTeX import Base


class pleibvdash(Base.Command):
    args = "self"
    def digest(self, tokens):
        self.image_path = u"images/abc"
