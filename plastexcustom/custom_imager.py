from plasTeX.Imagers import Imager

class CustomImager(Imager):
    def compileLatex(self, source):
        macros = """

        """
        source = macros + source
        Imager.compileLatex(self, source)