from plastexcustom import CustomBase as Base


class math(Base.Environment):
    args = "formula"


class displaymath(Base.Environment):
    args = "formula"


class eqnarray(Base.Environment):
    args = "formula"


class equation(Base.Environment):
    args = "formula"

