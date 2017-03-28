#!/bin/sh

sphinx-apidoc -o sphinx/source plastexcustom
sphinx-build -b html sphinx/source docs
