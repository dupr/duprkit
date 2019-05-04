#!/usr/bin/python3
# vim:se tw=0 sts=4 ts=4 et ai:
"""
Copyright © 2014-2018 Osamu Aoki

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
import time
import debmake.analyze
import debmake.checkdep5
import debmake.copyright
import debmake.debian
import debmake.debs
import debmake.debug
import debmake.dist
import debmake.kludge
import debmake.origtar
import debmake.para
import debmake.sanity
import debmake.scanfiles
import debmake.tar
import debmake.untar
#######################################################################
# Basic package information
#######################################################################

__debian_policy__   = '4.1.4'   # debian policy version
__debian_compat__   = '11'       # debian/compat
__programname__     = 'debmake'
__version__         = '4.3.1'
__copyright__       = 'Copyright © 2014-2018 Osamu Aoki <osamu@debian.org>'
__license__         = '''\
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


#######################################################################
# main program
#######################################################################
def main():
#######################################################################
# set parameters from commandline etc.
#######################################################################
    debmake.debug.debug('D: {} started'.format(sys.argv[0]), type='i')
    debmake.debug.debug('D: PYTHONPATH = {} '.format(':'.join(sys.path)), type='i')
    print('I: set parameters', file=sys.stderr)
    para = {}
    para['cwd'] = os.getcwd()
    para['program_name'] = __programname__
    para['program_version'] = __version__
    para['program_copyright'] = __copyright__
    para['program_license'] = __license__
    para['date'] = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    para['shortdate'] = time.strftime("%d %b %Y")
    para['year'] = time.strftime("%Y")
    para['standard_version'] = __debian_policy__    # Debian policy_
    para['compat'] = __debian_compat__              # debhelper
    para['build_depends']   = {'debhelper (>=' + para['compat'] +'~)'}
    para['desc'] = ''
    para['desc_long'] = ''
    para['export'] = set()
    para['override'] = set()
    # get prefix for install --user/ ,, --prefix/ ,, --home
    fullparent = os.path.dirname(sys.argv[0])
    if fullparent == '.':
        para['base_path'] = '..'
    else:
        para['base_path'] = os.path.dirname(fullparent)
    para = debmake.para.para(para)
    debmake.debug.debug_para('Dp: @post-para para[*]', para)
#######################################################################
# -v: print version and copyright notice and exit
#######################################################################
    if para['print_version']:
        print('{0} (version: {1}) {2}\n\n{3}'.format(
                para['program_name'],
                para['program_version'],
                para['program_copyright'],
                para['program_license']), file=sys.stderr)
        return
#######################################################################
# -c: scan source for copyright+ license text, print and exit
#######################################################################
    if para['copyright'] !=0:
        print('I: scan source for copyright+license text and file extensions', file=sys.stderr)
        (nonlink_files, xml_html_files, binary_files, huge_files, counter, count_list) = debmake.scanfiles.scanfiles()
        data = debmake.checkdep5.checkdep5(nonlink_files, mode=para['copyright'], pedantic=para['pedantic'])
        print(debmake.copyright.copyright('package', set(), data, xml_html_files, binary_files, huge_files, mode=para['copyright'], tutorial=para['tutorial']))
        return
#######################################################################
# -k: compare debian/copyright with the source and exit
#######################################################################
    if para['kludge'] !=0:
        print('I: compare debian/copyright with the source', file=sys.stderr)
        debmake.kludge.kludge(para['kludge'], para['pedantic'])
        return
#######################################################################
# sanity check parameters without digging deep into source tree
#######################################################################
    print('I: sanity check of parameters', file=sys.stderr)
    para = debmake.sanity.sanity(para)
    debmake.debug.debug_para('Dp: @post-sanity para[*]', para)
    print('I: pkg="{}", ver="{}", rev="{}"'.format(para['package'], para['version'], para['revision']), file=sys.stderr)
#######################################################################
# -d: make dist (with upstream buildsystem dist/sdist target)
#######################################################################
    if para['dist']:
        print('I: make the upstream tarball with "make dist" equivalents', file=sys.stderr)
        para = debmake.dist.dist(para)
        debmake.debug.debug_para('Dp: @post-dist para[*]', para)
        print('I: pkg="{}", ver="{}", rev="{}"'.format(para['package'], para['version'], para['revision']), file=sys.stderr)
#######################################################################
# -t: make tar (with "tar --exclude=debian" command)
#######################################################################
    elif para['tar']:
        print('I: make the upstream tarball with "tar --exclude=debian"', file=sys.stderr)
        debmake.tar.tar(para['tarball'], para['targz'], para['srcdir'], para['parent'], para['yes'])
        debmake.debug.debug_para('Dp: @post-tar para[*]', para)
#######################################################################
# -a, -d: extract archive from tarball (tar -xvzf)
#######################################################################
    if para['archive'] or para['dist']:
        print('I: untar the upstream tarball', file=sys.stderr)
        debmake.untar.untar(para['tarball'], para['targz'], para['srcdir'], para['dist'], para['tar'], para['parent'], para['yes'])
        debmake.debug.debug_para('Dp: @post-untar para[*]', para)
#######################################################################
# always: generate orig tarball if missing and non-native package
#######################################################################
    para['parent'] = os.path.basename(os.getcwd()) # update !!!
    print('I: *** start packaging in "{}". ***'.format(para['parent']), file=sys.stderr)
    if para['parent'] != para['srcdir']:
        print('W: parent dirtectory should be "{}".  (If you use pbuilder, this may be OK.)'.format(para['srcdir']), file=sys.stderr)
    if not para['native']:
        print('I: provide {}_{}.orig.tar.gz for non-native Debian package'.format(para['package'], para['version']), file=sys.stderr)
        # ln -sf parent/dist/Foo-1.0.tar.gz foo_1.0.orig.tar.gz
        debmake.origtar.origtar(para['package'], para['version'], para['targz'], para['tarball'], para['parent'])
        para['tarball'] = para['package'] + '_' + para['version'] + '.orig.' + para['targz']
        debmake.debug.debug_para('Dp: @post-origtar para[*]', para)
#######################################################################
# -q: quit here before generating template debian/* package files
#######################################################################
    if para['quitearly']:
        print('I: quit early after making the upstream tarball.', file=sys.stderr)
        exit(0)
#######################################################################
# Prep to create debian/* package files
#######################################################################
    print('I: parse binary package settings: {}'.format(para['binaryspec']), file=sys.stderr)
    para['debs'] = debmake.debs.debs(para['binaryspec'], para['package'], para['monoarch'], para['dh_with'])
    debmake.debug.debug_debs("Dd: para['debs'] =>", para['debs'])
    print('I: analyze the source tree', file=sys.stderr)
    para = debmake.analyze.analyze(para)
    debmake.debug.debug_para('Dp: @post-analyze para[*]', para)
    #debmake.gui()          # GUI setting
    #debmake.debug.debug_para('Dp: @post-gui para[*]', para)
#######################################################################
# Make debian/* package files
#######################################################################
    print('I: make debian/* template files', file=sys.stderr)
    debmake.debian.debian(para)
#######################################################################
# Make Debian package(s)
#######################################################################
    if para['judge']:
        command = 'fakeroot dpkg-depcheck -m -C -o ../{0}.depcheck.log -f -catch-alternatives debian/rules install >../{0}.build.log 2>&1'.format(para['package'])
        print('I: $ {}'.format(command), file=sys.stderr)
        if subprocess.call(command, shell=True) != 0:
            print('E: failed to run dpkg-depcheck.', file=sys.stderr)
            exit(1)
        command = 'LANG=C ; sed -e "1d" < ../{0}.depcheck.log | sort >../{0}.build-dep.log'.format(para['package'])
        print('I: $ {}'.format(command), file=sys.stderr)
        if subprocess.call(command, shell=True) != 0:
            print('E: failed to run sort on build-dep.', file=sys.stderr)
            exit(1)
        if len(para['debs']) == 1:
            bpackage = para['debs'][0]['package']
            command = 'LANG=C; find debian/' + bpackage + ' -type f 2>&1 | sed -e "s/^debian\/' + bpackage + '\///" | sort >../{0}.install.log'.format(para['package'])
            print('I: $ {}'.format(command), file=sys.stderr)
            if subprocess.call(command, shell=True) != 0:
                print('E: failed to run find debian/{}.'.format(bpackage), file=sys.stderr)
                exit(1)
        elif len(para['debs']) > 1:
            command = 'LANG=C; find debian/tmp -type f 2>&1 | sed -e "s/^debian\/tmp\///" | sort >../{0}.install.log'.format(para['package'])
            print('I: $ {}'.format(command), file=sys.stderr)
            if subprocess.call(command, shell=True) != 0:
                print('E: failed to run find debian/tmp.', file=sys.stderr)
                exit(1)
        else:
            print('E: No binary package was generated.', file=sys.stderr)
            exit(1)
        print('I: upon return to the shell, current directory becomes {}'.format(para['cwd']), file=sys.stderr)
        print('I: please execute "cd {0}" before building the binary package'.format(os.getcwd()), file=sys.stderr)
        print('I: with dpkg-buildpackage (or debuild, pdebuild, sbuild, ...).', file=sys.stderr)
    elif para['invoke']:
        print('I: {}'.format(para['invoke']), file=sys.stderr)
        if subprocess.call(para['invoke'], shell=True) != 0:
            print('E: failed to build Debian package(s).', file=sys.stderr)
            exit(1)
        if para['archive']:
            print('I: please inspect the build results.'.format(os.getcwd()), file=sys.stderr)
        else:
            print('I: upon return to the shell, current directory becomes {}'.format(para['cwd']), file=sys.stderr)
            print('I: please execute "cd .." and inspect the build results.'.format(os.getcwd()), file=sys.stderr)
    elif os.getcwd() != para['cwd']:
        print('I: upon return to the shell, current directory becomes {}'.format(para['cwd']), file=sys.stderr)
        print('I: please execute "cd {0}" before building the binary package'.format(os.getcwd()), file=sys.stderr)
        print('I: with dpkg-buildpackage (or debuild, pdebuild, sbuild, ...).', file=sys.stderr)
    return

#######################################################################
# Test code
#######################################################################
if __name__ == '__main__':
    main()

