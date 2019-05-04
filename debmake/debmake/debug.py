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
import sys
#######################################################################
# Debug output
#######################################################################
def get_debug():
    try:
        e = os.environ["DEBUG"]
    except KeyError:
        e = ''
    return e

def debug(msg, type=''):
    e = get_debug()
    if (e != '' and type == '') or \
            (type in e):
        print(msg, file=sys.stderr)
    return

def debug_para(msg, para):
    e = get_debug()
    if 'p' in e:
        line = '{}:\n'.format(msg)
        for x in para.keys():
            line += '  para[{}] = "{}"\n'.format(x, para[x])
        print(line, file=sys.stderr)
    elif e:
        line = '{}:\n'.format(msg)
        line += '  para[{}] = "{}"\n'.format('package', para['package'])
        line += '  para[{}] = "{}"\n'.format('version', para['version'])
        line += '  para[{}] = "{}"\n'.format('revision', para['revision'])
        line += '  para[{}] = "{}"\n'.format('targz', para['targz'])
        print(line, file=sys.stderr)
    return

def debug_debs(msg, debs):
    e = get_debug()
    if 'd' in e:
        line = '{}: \n'.format(msg)
        for deb in debs:
            line += '  Binary Package: {}\n'.format(deb['package'])
            line += '    Architecture: {}\n'.format(deb['arch'])
            line += '    Multi-Arch:   {}\n'.format(deb['multiarch'])
            line += '    Depends:      {}\n'.format(deb['depends'])
            line += '    Pre-Depends:  {}\n'.format(deb['pre-depends'])
            line += '    Type:         {}\n'.format(deb['type'])
        print(line, file=sys.stderr)
    return

#######################################################################
# Test code
#######################################################################
if __name__ == '__main__':
    debug('DEBUG ON!')
    para = {}
    para['package'] = 'package'
    para['version'] = '1.0'
    para['targz'] = 'tar.gz'
    debug_para('debug_para', para)

