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
import debmake.yn
###########################################################################
# untar: called from debmake.main()
###########################################################################
# tarball   = package-version.tar.gz (or  package_version.orig.tar.gz)
# targz     = tar.gz
# srcdir    = package-version
# tar       = True if -t, False if -a or -d
# dist      = True if -d, False if -a or -t
# parent    = package (original VCS directory for -d)
# yes       = True if -y, False as default
###########################################################################
def untar(tarball, targz, srcdir, dist, tar, parent, yes):
    print('I: pwd = "{}"'.format(os.getcwd()), file=sys.stderr)
    if not os.path.isfile(tarball):
        print('E: missing the "{}" file.'.format(tarball), file=sys.stderr)
        exit(1)
    if tar: # -t
        if os.path.isdir(srcdir):
            print('I: use existing "{}".'.format(srcdir), file=sys.stderr)
        else:
            print('E: fail to find "{}".'.format(srcdir), file=sys.stderr)
            exit(1)
    else: # -a -d
        if os.path.isdir(srcdir):
            debmake.yn.yn('remove "{}" directory in untar'.format(srcdir), 'rm -rf ' + srcdir, yes)
        # setup command line
        if targz == 'tar.bz2':
            command = 'tar --bzip2 -xvf '
            commandx = 'tar --bzip2 -tf '
        elif targz == 'tar.xz':
            command = 'tar --xz -xvf '
            commandx = 'tar --xz -tf '
        elif targz == 'tar.gz':
            command = 'tar -xvzf '
            commandx = 'tar -tzf '
        else:
            print('E: the extension "{}" not supported.'.format(targz), file=sys.stderr)
            exit(1)
        command += tarball
        print('I: $ {}'.format(command), file=sys.stderr)
        if subprocess.call(command, shell=True) != 0:
            print('E: failed to untar.', file=sys.stderr)
            exit(1)
        print('I: untared {}.'.format(tarball), file=sys.stderr)
        # rename source directory
        commandx += tarball + '|grep -v /.'
        print('I: {}'.format(commandx), file=sys.stderr)
        try:
            tarsrcdirs = subprocess.check_output(commandx, shell=True, universal_newlines=True).strip().split('\n')
        except CalledProcessError:
            print('E: failed to list the stem directory of tar.', file=sys.stderr)
            exit(1)
        # tailing / may or may not exist.
        if len(tarsrcdirs) > 1:
            print('W: {} first level directories found.'.format(len(tarsrcdirs)), file=sys.stderr)
        if tarsrcdirs[0] =="":
            print('E: No first level directory found.', file=sys.stderr)
            exit(1)
        elif tarsrcdirs[0][-1:] == '/':
            tarsrcdir = tarsrcdirs[0][:-1]
        else:
            tarsrcdir = tarsrcdirs[0]
        if tarsrcdir != srcdir:
            print('I: move source tree from {} to {}.'.format(tarsrcdir, srcdir), file=sys.stderr)
            command = 'mv -f ' + tarsrcdir + ' ' + srcdir
            print('I: $ {}'.format(command), file=sys.stderr)
            if subprocess.call(command, shell=True) != 0:
                print('E: failed to move directory.', file=sys.stderr)
                exit(1)
    # copy debian/* for -d
    if dist and os.path.isdir(parent + '/debian'):
        command = 'cp -drl ' + parent + '/debian ' + srcdir + '/debian'
        # execute command: copy debian tree (with hardlink)
        print('I: $ {}'.format(command), file=sys.stderr)
        if subprocess.call(command, shell=True) != 0:
            print('E: cp -drl failed.', file=sys.stderr)
            exit(1)
    # cd srcdir
    os.chdir(srcdir)
    print('I: pwd = "{}"'.format(os.getcwd()), file=sys.stderr)
    return

if __name__ == '__main__':
    # untar(tarball, targz, srcdir, dist, tar, parent)
    # -a
    os.chdir('tarball')
    untar("example.tar.gz", "tar.gz", "example-1.0", False, False, "")
    os.chdir('..')
    # -d
    os.chdir('dist')
    untar("example.tar.gz", "tar.gz", "example-1.0", True, False, "example")
    os.chdir('..')
    # -t
    os.chdir('tar')
    untar("", "tar.gz", "example-1.0", False, True, "")
    os.chdir('..')

