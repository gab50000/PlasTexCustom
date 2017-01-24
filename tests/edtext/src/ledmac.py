from plasTeX import Base


class edtext(Base.Command):
    """\edtext{text}"""
    args = 'text'

    def invoke(self, tex):
        Base.Command.invoke(self, tex)


#  class Afootnote(Base.Command):
    #  """\Afootnote{text}"""
    #  args = 'text'

    #  def invoke(self, tex):
        #  Base.Command.invoke(self, tex)
#
#
#class Bfootnote(Base.Command):
#    args = 'Bfootnote:str'
#
#    def invoke(self, tex):
#        Base.Command.invoke(self, tex)
#
#
#class Cfootnote(Base.Command):
#    args = 'Cfootnote:str'
#
#    def invoke(self, tex):
#        Base.Command.invoke(self, tex)
