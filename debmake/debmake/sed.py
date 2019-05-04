#!/usr/bin/python3
# vim:se tw=0 sts=4 ts=4 et ai:
"""
Copyright © 2014 Osamu Aoki

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import glob
import os
import sys
import debmake.cat
import debmake.debug
#######################################################################
def sed(confdir, destdir, substlist, package, mask='*', tutorial=False):
    ###################################################################
    # confdir:   configuration file directory with / at the end
    # destdir:   destination directory with / at the end
    # substlist: substitution dictionary
    # package:   binary package name
    # mask:      source file mask for glob. Usually, *
    ###################################################################
    lconfdir = len(confdir)
    for file in glob.glob(confdir + mask):
        print('I: substituting => {}'.format(file), file=sys.stderr)
        with open(file, mode='r', encoding='utf-8') as f:
            text = f.read()
        for k in substlist.keys():
            text = text.replace(k, substlist[k])
        if file[lconfdir:lconfdir+7] == 'package':
            newfile = destdir + package + file[lconfdir+7:]
        else:
            newfile = destdir + file[lconfdir:]
        debmake.debug.debug('Ds: "{}"'.format(text), type='s')
        debmake.cat.cat(newfile, text, tutorial=tutorial)
    return

#######################################################################
# Test script
#######################################################################
if __name__ == '__main__':
    tutorial = False
    substlist = {
        '@BINPACKAGE@': 'binpackage',
        '@PACKAGE@': 'package',
        '@UCPACKAGE@': 'package'.upper(),
        '@YEAR@': '2014',
        '@FULLNAME@': 'fullname',
        '@EMAIL@': 'email@example.org',
        '@SHORTDATE@': '11 Jan. 2013',
    }
    sed('../extra2/', 'debian/', substlist, 'package', tutorial=tutorial)
    sed('../extra3/', 'debian/', substlist, 'package', tutorial=tutorial)
    sed('../extra4/', 'debian/copyright-example/', substlist, 'package', tutorial=tutorial)

