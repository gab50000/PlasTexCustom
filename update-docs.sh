#!/bin/sh

sphinx-apidoc -f -o sphinx/source plastexcustom
sphinx-build -b html sphinx/source docs
