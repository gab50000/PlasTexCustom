from plastexcustom import CustomBase as Base


class pleibvdash(Base.Command):
    args = "self"
    def digest(self, tokens):
        self.image_path = u"images/abc"
