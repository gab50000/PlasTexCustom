from plastexcustom import CustomBase as Base


class edtext(Base.Command):
    """\edtext{text}{content}"""
    args = 'text content'


class Afootnote(Base.Command):
    """\Afootnote{text}"""
    args = 'text'


class Bfootnote(Base.Command):
    args = 'text'


class Cfootnote(Base.Command):
    args = 'text'


class lemma(Base.Command):
    args = 'text'
