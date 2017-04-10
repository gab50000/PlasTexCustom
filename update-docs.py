import sh
import os


md_files = sh.find("sphinx", "-name", "*.md").splitlines()
for md in md_files:
    name, ext = os.path.splitext(md)
    sh.pandoc("-f", "markdown","-o", "{}.rst".format(name), "{}.md".format(name))
sh.sphinx_apidoc("-f", "-o", "sphinx/source", "plastexcustom")
sh.sphinx_build("-a", "-b", "html", "sphinx/source", "docs")
