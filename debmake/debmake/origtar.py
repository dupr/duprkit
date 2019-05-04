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
# origtar: called from debmake.main()
###########################################################################
def origtar(package, version, targz, tarball, srcdir):
    # cd ..
    os.chdir('..')
    print('I: pwd = "{}"'.format(os.getcwd()), file=sys.stderr)
    #######################################################################
    # make package_versdion.orig.tar.gz in the parent directory if not exist
    # source is in srcdir
    #######################################################################
    origtargz = package + '_' + version + '.orig.' + targz
    if os.path.isfile(tarball):
        if tarball == origtargz:
            print('I: Use existing "{}" as upstream tarball'.format(tarball), file=sys.stderr)
        else:
            command = 'ln -sf ' + tarball + ' ' + origtargz
            print('I: $ {}'.format(command), file=sys.stderr)
            if subprocess.call(command, shell=True) != 0:
                print('E: failed to create symlink.', file=sys.stderr)
                exit(1)
    elif os.path.isfile(origtargz):
        print('I: Use existing "{}" as upstream tarball'.format(origtargz), file=sys.stderr)
    else:
        print('E: missing "{}".'.format(tarball), file=sys.stderr)
        exit(1)
    os.chdir(srcdir) # calling side ensures this 
    print('I: pwd = "{}"'.format(os.getcwd()), file=sys.stderr)
    return

if __name__ == '__main__':
    print('no test')

