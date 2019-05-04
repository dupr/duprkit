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
import datetime
import glob
import os
import re
import subprocess
import sys
###########################################################################
# sanity: called from debmake.main()
###########################################################################
def sanity(para):
    #######################################################################
    # Normalize para[] for each exclusive build case (-d -t -a)
    #######################################################################
    package = ''
    version = ''
    revision = ''
    targz = ''
    if para['archive']: # -a
        # remote URL
        reurl = re.match(r'(http://|https://|ftp://).*/([^/]+)$', para['tarball'])
        if reurl:
            url = para['tarball']
            para['tarball'] = reurl.group(2)
            if os.path.isfile('/usr/bin/wget'):
                command = '/usr/bin/wget ' + url
            elif os.path.isfile('/usr/bin/curl'):
                command = '/usr/bin/curl ' + url
            else: 
                print('E: please install wget or curl.', file=sys.stderr)
                exit(1)
            print('I: $ {}'.format(command), file=sys.stderr)
            if subprocess.call(command, shell=True) != 0:
                print('E: wget/curl failed.', file=sys.stderr)
                exit(1)
        parent = ''
        # tarball: ibus-1.5.5-2.fc19.src.rpm
        resrcrpm = re.match(r'([^/_]+-[^/_-]+)-[0-9]+\.[^.]+\.src\.rpm$', os.path.basename(para['tarball']))
        if resrcrpm:
            command = 'rpm2cpio ' + para['tarball'] + '|cpio -dium'
            print('I: $ {}'.format(command), file=sys.stderr)
            if subprocess.call(command, shell=True) != 0:
                print('E: rpm2cpioc ... | cpio -dium failed.', file=sys.stderr)
                exit(1)
            files = glob.glob(resrcrpm.group(1) + '*.tar.gz') + \
                    glob.glob(resrcrpm.group(1) + '*.tar.bz2') + \
                    glob.glob(resrcrpm.group(1) + '*.tar.xz')
            if files:
                para['tarball'] = files[0]
            else:
                print('E: no tar found in src.rpm.', file=sys.stderr)
                exit(1)
        if not os.path.isfile(para['tarball']):
            print('E: Non-existing tarball name {}'.format(para['tarball']), file=sys.stderr)
            exit(1)
        if os.path.abspath(os.path.dirname(para['tarball'])) != os.getcwd():
            command = 'cp ' + para['tarball'] + ' ' + os.path.basename(para['tarball'])
            print('I: $ {}'.format(command), file=sys.stderr)
            if subprocess.call(command, shell=True) != 0:
                print('E: {} failed.'.format(command), file=sys.stderr)
                exit(1)
        para['tarball'] = os.path.basename(para['tarball'])
        # tarball: package_version.orig.tar.gz
        reorigtar = re.match(r'([^/_]+)_([^-/_]+)\.orig\.(tar\.gz|tar\.bz2|tar\.xz)$', para['tarball'])
        # tarball: package-version.tar.gz or package_version.tar.gz
        rebasetar = re.match(r'([^/_]+)[-_]([^-/_]+)\.(tar\.gz|tar\.bz2|tar\.xz)$', para['tarball'])
        if reorigtar:
            package = reorigtar.group(1).lower()
            version = reorigtar.group(2)
            targz = reorigtar.group(3)
        elif rebasetar:
            package = rebasetar.group(1).lower()
            version = rebasetar.group(2)
            targz = rebasetar.group(3)
        else:
            print('E: Non-supported tarball name {}'.format(para['tarball']), file=sys.stderr)
            exit(1)
    #######################################################################
    if not para['archive']: # not -a
        parent = os.path.basename(os.getcwd())
        # check changelog for package/version/revision (non-native package)
        if not para['native'] and os.path.isfile('debian/changelog'):
            with open('debian/changelog', mode='r', encoding='utf-8') as f:
                line = f.readline()
            pkgver = re.match('([^ \t]+)[ \t]+\(([^()]+)-([^-()]+)\)', line)
            if pkgver:
                package = pkgver.group(1).lower()
                version = pkgver.group(2)
                revision = pkgver.group(3)
            else:
                print('E: changelog start with "{}"'.format(line), file=sys.stderr)
                exit(1)
    #######################################################################
    if para['tar']: # -t
        if version == '':
            version = datetime.datetime.utcnow().strftime("0~%y%m%d%H%M") # 0~YYMMDDHHmm
    #######################################################################
    # set parent/srcdir/tarball/package/version/revision
    para['parent'] = parent
    if para['package'] == '':
        para['package'] = package
    elif para['package'] != package:
        print('W: -p "{}" != auto set value "{}"'.format(para['package'], package), file=sys.stderr)
    if para['version'] == '':
        para['version'] = version
    elif para['version'] != version:
        print('W: -u "{}" != auto set value "{}"'.format(para['version'], version), file=sys.stderr)
    #######################################################################
    if not para['archive']: # not -a
        if para['revision'] == '':
            para['revision'] = revision
        elif para['revision'] != revision:
            print('W: -r "{}" != auto set value "{}"'.format(para['revision'], revision), file=sys.stderr)
    #######################################################################
    if para['archive']: # -a
        if para['targz'] == '':
            para['targz'] = targz
        elif para['targz'] != targz:
            print('W: -r "{}" != auto set value "{}"'.format(para['targz'], targz), file=sys.stderr)
    #######################################################################
    if not para['archive']: # not -a
        # set para['targz']
        if para['targz'] == '':
            para['targz'] = 'tar.gz'
        elif para['targz'][0] == 'g':
            para['targz'] = 'tar.gz'
        elif para['targz'][0] == 'b':
            para['targz'] = 'tar.bz2'
        elif para['targz'][0] == 'x':
            para['targz'] = 'tar.xz'
        elif para['targz'] == 'tar.gz':
            pass
        elif para['targz'] == 'tar.bz2':
            pass
        elif para['targz'] == 'tar.xz':
            pass
        else:
            print('E: --targz (-z) value is invalid: {}'.format(para['targz']), file=sys.stderr)
            exit(1)
    #######################################################################
    if para['archive']:
        para['srcdir'] = para['package'] + '-' + para['version']
        # para['tar'] may be Foo-1.0.tar.xz and keep it so.
    elif para['dist']: # -d
        pass # differ package/version/tarball/srcdir
    else: # normal (native/non-native) or -t
        if para['version'] == '':# -u missing
            pkgver = re.match('^([^_]+)-([^-_]+)$', parent)
            if pkgver:
                if para['package'] == '': # both -p and -u missing
                    para['package'] = pkgver.group(1).lower()
                para['version'] = pkgver.group(2) # -u missing
            else:
                print('E: invalid parent directory for setting package/version: {}'.format(parent), file=sys.stderr)
                print('E: rename parent directory to "package-version".', file=sys.stderr)
                exit(1)
        elif para['package'] == '': # -u set, -p missing
            para['package'] = parent.lower()
        para['srcdir'] = para['package'] + '-' + para['version']
        para['tarball'] = para['package'] + '-' + para['version'] + '.' + para['targz']
    #######################################################################
    if para['revision'] == '':
        para['revision'] = '1'
    #######################################################################
    # Dynamic content with package name etc.
    #######################################################################
    para['section'] = 'unknown'
    para['priority'] = 'optional'
    para['homepage'] = '<insert the upstream URL, if relevant>'
    para['vcsvcs'] = 'https://salsa.debian.org/debian/' + para['package'] + '.git'
    para['vcsbrowser'] = 'https://salsa.debian.org/debian/' + para['package']
    #######################################################################
    # Override default for local only package (cheat lintian)
    #######################################################################
    if para['invoke']:
        para['local'] = True
    if para['local']:
        para['section'] = 'local'
        para['homepage'] = 'http://www.debian.org'
        para['email'] = 'bogus@localhost'
    return para
