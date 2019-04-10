#!/bin/sh
set -e
. ./duprkit
export DK_VERBOSE=1

src="example"
version="0"
maintainer="anonymous <anon@example.org>"
dkGen_debian_changelog .
test -r debian/changelog

section="science"
stdver="4.3.0"
compat="11"
description="hello world"
dkGen_debian_control .
test -r debian/control

license="Expat"
dkGen_debian_copyright .
test -r debian/copyright 

dkGen_debian_rules .
test -x debian/rules

dkGen_debian_source_format .
test -r debian/source/format

dkGenerate foobar
test -r foobar/debian/changelog
test -r debian/control
test -r debian/copyright 
test -x debian/rules
test -r debian/source/format

echo "@SRC@ @VERSION@" > junk
dkSubst_ junk

mkdir junk.d;
echo "@SECTION@" > junk.d/a
echo "@STDVER@"  > junk.d/b
dkSubst junk.d
