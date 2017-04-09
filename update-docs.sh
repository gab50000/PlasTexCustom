#!/bin/sh

sphinx-apidoc -f -o sphinx/source plastexcustom
sphinx-build -a -b html sphinx/source docs
