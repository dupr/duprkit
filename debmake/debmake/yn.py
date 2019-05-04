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
import subprocess
import sys
###########################################################################
# yn: ask mes and execute command
###########################################################################
def yn(mes, command, yes):
    if yes == 1:
        yn = 'y'
    elif yes == 2:
        yn = 'n'
    else:
        yn = input('?: {} [Y/n]: '.format(mes))
        if yn == '':
            yn = 'y'
        else:
            yn = yn[0].lower()
    if (yn =='y'):
        if command:
            print('I: $ {}'.format(command), file=sys.stderr)
            if subprocess.call(command, shell=True) != 0:
                print('E: failed to run command.', file=sys.stderr)
                exit(1)
    else:
        print('E: terminating since "n" chosen at Y/n question.', file=sys.stderr)
        exit(1)
    print('I: pwd = "{}"'.format(os.getcwd()), file=sys.stderr)
    return

if __name__ == '__main__':
    print('I: ask', file=sys.stderr)
    yn("list current directory (ask)", "ls -la", 0)
    print('I: always yes', file=sys.stderr)
    yn("list current directory (always yes)", "ls -la", 1)
    print('I: never yes', file=sys.stderr)
    yn("list current directory (never yes)", "ls -la", 2)

