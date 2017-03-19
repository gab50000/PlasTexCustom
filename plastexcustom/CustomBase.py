from plasTeX import Base


class Environment(Base.Environment):
    def invoke(self, tex):
        Base.Environment.invoke(self, tex)


class Command(Base.Command):
    def invoke(self, tex):
        Base.Command.invoke(self, tex)
