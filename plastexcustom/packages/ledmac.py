from plasTeX import Base


class edtext(Base.Command):
    """\edtext{text}{content}"""
    args = 'text content'

    def invoke(self, tex):
        Base.Command.invoke(self, tex)


class Afootnote(Base.Command):
    """\Afootnote{text}"""
    args = 'text'

    def invoke(self, tex):
        Base.Command.invoke(self, tex)


class Bfootnote(Base.Command):
    args = 'text'

    def invoke(self, tex):
        Base.Command.invoke(self, tex)


class Cfootnote(Base.Command):
    args = 'text'

    def invoke(self, tex):
        Base.Command.invoke(self, tex)


class lemma(Base.Command):
    args = 'text'

    def invoke(self, tex):
        Base.Command.invoke(self, tex)
