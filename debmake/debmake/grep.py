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
import os
import re
import sys
#######################################################################
# grep rtext file
def grep(file, rtext, *range):
    lines = ''
    if not os.path.isfile(file):
        print('I: skipping :: {} (missing file)'.format(file), file=sys.stderr)
    else:
        reg = re.compile(rtext)
        if len(range) == 0:
            lbgn = 0
            lend = -1
        elif len(range) == 1:
            lbgn = range[0]
            lend = -1
        else:
            lbgn = range[0]
            lend = range[1]
        with open(file, mode='r', encoding='utf-8') as f:
            for (i, l) in enumerate(f.readlines()):
                if ( i >= lbgn ) and (( lend < 0 ) or ( lend > i)):
                    match = reg.search(l)
                    if match:
                        lines += l
    return lines

#######################################################################
# Test script
#######################################################################
if __name__ == '__main__':
    print(grep('/bin/zcat', r'^#!', 0, 2), end='')
    print('----')
    print(grep('/bin/zcat', r'terms', 0, 10), end='')
    print('----')
    if grep('/bin/zcat', r'terms', 0, 10):
        print('found')
    print('----')
    if not grep('/bin/zcat', r'teXXXXs', 0, 10):
        print('not found')
        

