#!/bin/sh
set -e

. ./duprkit

license="Expat"
dkGen_debian_copyright
test -r debian/copyright
