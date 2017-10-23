from plastexcustom import CustomBase as Base
from plasTeX.Base.TeX.Primitives import par
from plasTeX.Base.LaTeX.Sectioning import section
from reledmac import pstart, pend


class pleibvdash(Base.Command):
    args = "self"


class textso(Base.Command):
    args = "self"


class textsuperscript(Base.Command):
    args = "self"


class ss(Base.Command):
    args = ""


class centering(Base.Environment):
    args = ""
    def digest(self, tokens):
        for token in tokens:
            if type(token) in (section, par, pend):
                tokens.push(token)
                break
            self.childNodes.append(token)
