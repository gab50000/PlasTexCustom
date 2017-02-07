from plasTeX import Base


class math(Base.Environment):
    args = "formula:str"

    def invoke(self, tex):
        Base.Command.invoke(self, tex)


class displaymath(Base.Environment):
    args = "formula:str"

    def invoke(self, tex):
        Base.Command.invoke(self, tex)


class eqnarray(Base.Environment):
    args = "formula:str"

    def invoke(self, tex):
        Base.Command.invoke(self, tex)


class equation(Base.Environment):
    args = "formula:str"

    def invoke(self, tex):
        Base.Command.invoke(self, tex)
