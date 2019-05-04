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
import re
import debmake.read
#######################################################################
def control(para):
    ndebs = len(para['debs'])
    types = set()
    for deb in para['debs']:
        types.add(deb['type'])
    ntypes = len(types)
    #
    msg = control_src(para)
    if para['desc'].strip():
        desc = para['desc'].strip()
    else:
        desc = 'auto-generated package by debmake'
    #
    if para['desc_long'].rstrip():
        desc_long = para['desc_long'].rstrip()
    elif para['desc'].strip():
        desc_long = ' ' + para['desc'].strip()
    else:
        desc_long = ''
    if desc_long:
        desc_long_xtra = ''
    else:
        if para['tutorial']:
            desc_long_xtra = debmake.read.read(para['base_path'] + '/share/debmake/extra0desc_long/_long_tutorial').rstrip()
        else:
            desc_long_xtra = debmake.read.read(para['base_path'] + '/share/debmake/extra0desc_long/_long').rstrip()
    for i, deb in enumerate(para['debs']):
        desc_long_type = debmake.read.read(para['base_path'] + '/share/debmake/extra0desc_long/' + deb['type']).rstrip() 
        if ndebs == 1: # single binary
            deb['desc'] = desc
        elif ndebs == ntypes: # all uniq *type* -> no index 
            deb['desc'] = desc + ': {}'.format(deb['type'])
        else:
            deb['desc'] = desc + ': {} #{}'.format(deb['type'], i)
        if ndebs == 1: # single binary
            if desc_long:
                deb['desc_long'] = desc_long + '\n'
            else:
                deb['desc_long'] = desc_long_xtra + '\n'
        elif ndebs == ntypes: # all uniq *type* -> no index
            if i == 0:
                if desc_long:
                    deb['desc_long'] = desc_long_type + '\n .\n' + desc_long + '\n'
                else:
                    deb['desc_long'] = desc_long_type + '\n .\n' + desc_long_xtra + '\n'
            else:
                if desc_long:
                    deb['desc_long'] = desc_long_type + '\n .\n' + desc_long + '\n'
                else:
                    deb['desc_long'] = desc_long_type + '\n'
        else:
            if i == 0:
                if desc_long:
                    deb['desc_long'] = desc_long_type + ': #{}\n .\n'.format(i) + desc_long + '\n'
                else:
                    deb['desc_long'] = desc_long_type + ': #{}\n .\n'.format(i) + desc_long_xtra + '\n'
            else:
                if desc_long:
                    deb['desc_long'] = desc_long_type + ': #{}\n .\n'.format(i) + desc_long + '\n'
                else:
                    deb['desc_long'] = desc_long_type + ': #{}\n'.format(i)
        msg += control_bin(para, deb)
    return msg

#######################################################################
def control_src(para):
    msg = '''\
Source: {0}
Section: {1}
Priority: {2}
Maintainer: {3} <{4}>
Build-Depends: {5}
Standards-Version: {6}
Homepage: {7}
{8}: {9}
{10}: {11}
'''.format(
            para['package'],
            para['section'],
            para['priority'],
            para['fullname'],
            para['email'],
            ',\n\t'.join(para['build_depends']),
            para['standard_version'],
            para['homepage'],
            guess_vcsvcs(para['vcsvcs']),
            para['vcsvcs'],
            guess_vcsbrowser(para['vcsbrowser']),
            para['vcsbrowser'])
    if 'python2' in para['dh_with']:
        msg += 'X-Python-Version: >= 2.6\n'
    if 'python3' in para['dh_with']:
        msg += 'X-Python3-Version: >= 3.2\n'
    # anything for perl and others XXX FIXME XXX
    msg += '\n'
    return msg

#######################################################################
def guess_vcsvcs(vcsvcs):
    if re.search('\.git$', vcsvcs):
        return '#Vcs-Git'
    elif re.search('\.hg$', vcsvcs):
        return '#Vcs-Hg'
    elif re.search('^:pserver:', vcsvcs):
        # CVS :pserver:anonymous@anonscm.debian.org:/cvs/webwml
        return '#Vcs-Cvs'
    elif re.search('^:ext:', vcsvcs):
        # CVS :ext:username@cvs.debian.org:/cvs/webwml
        return '#Vcs-Cvs'
    elif re.search('^svn[:+]', vcsvcs):
        # SVN svn://svn.debian.org/ddp/manuals/trunk manuals
        # SVN svn+ssh://svn.debian.org/svn/ddp/manuals/trunk
        return '#Vcs-Svn'
    else:
        return '#Vcs-Git'

#######################################################################
def guess_vcsbrowser(vcsbrowser):
    if re.search('\.git$', vcsbrowser):
        return '#Vcs-Browser'
    elif re.search('\.hg$', vcsbrowser):
        return '#Vcs-Browser'
    elif re.search('^:pserver:', vcsbrowser):
        # CVS :pserver:anonymous@anonscm.debian.org:/cvs/webwml
        return '#Vcs-Browser'
    elif re.search('^:ext:', vcsbrowser):
        # CVS :ext:username@cvs.debian.org:/cvs/webwml
        return '#Vcs-Browser'
    elif re.search('^svn[:+]', vcsbrowser):
        # SVN svn://svn.debian.org/ddp/manuals/trunk manuals
        # SVN svn+ssh://svn.debian.org/svn/ddp/manuals/trunk
        return '#Vcs-Browser'
    else:
        return '#Vcs-Browser'

#######################################################################
def control_bin(para, deb):
    # non M-A
    if para['monoarch']:
        multiarch = ''
        predepends = ''
    # M-A + lib (pre-depends line)
    elif deb['pre-depends']:
        multiarch = 'Multi-Arch: ' + deb['multiarch'] + '\n'
        predepends = 'Pre-Depends: ' + ',\n\t'.join(deb['pre-depends']) + '\n'
    # M-A + non-lib
    else:
        multiarch = 'Multi-Arch: ' + deb['multiarch'] + '\n'
        predepends = ''
    if deb['type'] == 'dev':
        section = 'Section: libdevel\n'
    elif deb['type'] == 'lib':
        section = 'Section: libs\n'
    elif deb['type'] == 'doc':
        section = 'Section: doc\n'
    else:
        section = ''
    ###################################################################
    return '''\
Package: {0}
{1}Architecture: {2}
{3}{4}Depends: {5}
Description: {6}
{7}
'''.format(
            deb['package'],
            section,
            deb['arch'],
            multiarch,
            predepends,
            ',\n\t'.join(deb['depends']),
            deb['desc'],
            deb['desc_long'])

#######################################################################
# Test script
#######################################################################
if __name__ == '__main__':
    import debmake.debs
    para = {}
    para['package'] = 'package'
    para['section'] = 'misc'
    para['priority'] = 'normal'
    para['fullname'] = 'Osamu Aoki'
    para['email'] = 'osamu@debian.org'
    para['standard_version'] = '4.1.1'
    para['build_depends'] = set()
    para['homepage'] = 'https://www.debian.org'
    para['vcsvcs'] = 'git:git.debian.org'
    para['vcsbrowser'] = 'https://anonscm.debian.org'
    para['debs'] = set()
    para['dh_with'] = set()
    print(control(para))
    print('***********************************************************')
    para['dh_with'] = set({'python3'})
    para['binaryspec'] = '-:python,-doc:doc,lib'
    para['monoarch'] = False
    para['debs'] = debmake.debs.debs(para['binaryspec'], para['package'], para['monoarch'], para['dh_with'])
    print(control(para))
