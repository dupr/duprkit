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
import sys
###########################################################################
def match_prefix(name, prefix):
    l = len(prefix)
    return (len(name) > 1) and (name[:l] == prefix)

def match_suffix(name, suffix):
    l = len(suffix)
    return (len(name) > 1) and (name[-l:] == suffix)
###########################################################################
# sanity: called from debmake.main()
###########################################################################
def debs(binaryspec, package, monoarch, dh_with):
    #######################################################################
    # parse binary package names and their specification: binaryspec -> debs
    #######################################################################
    debs = [] # list
    pset = set()
    tset = set()
    dropch = "'" + '"' + " " + "\t" + "\n"
    for x0 in binaryspec.strip(dropch).split(','):
        x = x0.strip()
        ###################################################################
        # split: y[0] = bin-package-name-marker y[1] = bin-package-type
        ###################################################################
        y = x.split(':')
        if len(y) >= 3:
            print('E: -b does not support the 3rd argument yet: {}'.format(x), file=sys.stderr)
            exit(1)
        ###################################################################
        # get real binary package name: p
        ###################################################################
        p = y[0].strip()
        if p == '':
            p = package
        elif p == '-':
            p = package
        elif p[0] == '-':
            p = package + p
        # first default values and then override or update values
        a = 'any'       # arch
        m = 'foreign'   # muiti-arch
        t = ''          # type
        dp = {'${misc:Depends}'}
        pd = set()
        ###################################################################
        # Prefix names should come first to be overriden later
        ###################################################################
        if match_prefix(p, 'lib'):
            a = 'any'
            m = 'same'
            t = 'lib'
        elif match_prefix(p, 'fonts-'):
            a = 'all'
            m = 'foreign'
            t = 'data'
        elif match_prefix(p, 'python-'):
            a = 'all'
            m = 'foreign'
            t = 'python'
        elif match_prefix(p, 'python3-'):
            a = 'all'
            m = 'foreign'
            t = 'python3'
        else:
            pass
        # Suffix names override
        if match_suffix(p, '-perl'):
            a = 'all'
            m = 'foreign'
            t = 'perl'
        elif match_suffix(p, '-dev'):
            a = 'any'
            m = 'same'
            t = 'dev'
        elif match_suffix(p, '-bin') or \
             match_suffix(p, 'tools') or \
             match_suffix(p, 'utils'):
            a = 'any'
            m = 'foreign'
            t = 'bin'
        elif match_suffix(p, '-doc') or \
             match_suffix(p, '-manual') or \
             match_suffix(p, '-html'):
            a = 'all'
            m = 'foreign'
            t = 'doc'
        elif match_suffix(p, '-common'):
            a = 'all'
            m = 'foreign'
            t = 'data'
        else:
            pass
        ###################################################################
        # override if explicit 2nd argument exists, e.g. all in foo:all
        ###################################################################
        # The shorter match comes after the longer match
        if len(y) >= 2:
            t = y[1].strip()
            if match_prefix(t, 'an') or \
               match_prefix(t, 'f'): # any foreign (deprecated)
                a = 'any'
                m = 'foreign'
                if t =='':
                    t = 'bin'
            if match_prefix(t, 'b'): # bin
                a = 'any'
                m = 'foreign'
                t = 'bin'
            elif match_prefix(t, 'da'): # data
                a = 'all'
                m = 'foreign'
                t = 'data'
            elif match_prefix(t, 'de'): # dev
                a = 'any'
                m = 'same'
                t = 'dev'
            elif match_prefix(t, 'do'): # doc
                a = 'all'
                m = 'foreign'
                t = 'doc'
            elif match_prefix(t, 'l'): # lib
                a = 'any'
                m = 'same'
                t = 'lib'
            elif match_prefix(t, 'pe') or (t == 'pl'): # perl
                a = 'all'
                m = 'foreign'
                t = 'perl'
            elif match_prefix(t, 'python3') or (t == 'py3'): # python3
                a = 'all'
                m = 'foreign'
                t = 'python3'
            elif match_prefix(t, 'py'): # python
                a = 'all'
                m = 'foreign'
                t = 'python'
            elif match_prefix(t, 'ruby') or (t == 'rb'): # ruby
                a = 'all'
                m = 'foreign'
                t = 'ruby'
            elif match_prefix(t, 'sc') or (t == 'sh'): # script
                a = 'all'
                m = 'foreign'
                t = 'script'
            ###############################################################
            # ambiguous type values (but clear about arch/multi-arch
            ###############################################################
            elif match_prefix(t, 'an') or \
               match_prefix(t, 'f'): # any foreign
                a = 'any'
                m = 'foreign'
                if t == '':
                    t = 'bin'
            elif match_prefix(t, 'a'): # all
                a = 'all'
                m = 'foreign'
                if t == '':
                    t = 'script'
            elif match_prefix(t, 'sa'): # same
                a = 'any'
                m = 'same'
                if t == '':
                    t = 'lib'
            elif t == '': # bin as default
                pass
            else:
                print('E: -b: {} has undefined type: {}'.format(p, t), file=sys.stderr)
                exit(1)
        ###################################################################
        # update binary package type from dh_with and arch setting
        ###################################################################
        if t == '':
            if 'perl_build' in dh_with:
                a = 'all'
                t = 'perl'
            elif 'perl_makemaker' in dh_with:
                a = 'all'
                t = 'perl'
            elif 'python2' in dh_with:
                a = 'all'
                t = 'python'
            elif 'python3' in dh_with:
                a = 'all'
                t = 'python3'
            elif a == 'any': # bin as default 
                t = 'bin'
            else:
                print('E: -b: {} has arch={}, dh_with={} and null type.'.format(p, a, dh_with), file=sys.stderr)
                exit(1)
        # t always have non NULL string value !
        ###################################################################
        # monoarch = non-multi-arch
        ###################################################################
        if monoarch:
            m = ''
        ###################################################################
        # multi arch and library package
        ###################################################################
        if (not monoarch) and t == 'lib':
            # set this only for M-A library packages
            pd.update({'${misc:Pre-Depends}'})
        ###################################################################
        # update binary package dependency by package type etc.
        ###################################################################
        if t == 'bin': # executable
            dp.update({'${shlibs:Depends}'})
        elif t == 'lib': # library
            dp.update({'${shlibs:Depends}'})
        elif t == 'perl': # dh_perl(1)
            dp.update({'${perl:Depends}'})
        elif t == 'python': # dh_python2
            dp.update({'${python:Depends}'})
        elif t == 'python3': # dh_python3
            dp.update({'${python3:Depends}'})
        elif t == 'ruby': # gem2deb ??? XXXX FIXME XXXX
            dp.update({'${ruby:Depends}'})
        else:
            pass
        ###################################################################
        # loging and sanity check
        ###################################################################
        print('I: binary package={} Type={} / Arch={} M-A={}'.format(p, t, a, m), file=sys.stderr)
        if p in pset:
            print('E: duplicate definition of package name "{}"'.format(p), file=sys.stderr)
            exit(1)
        pset.update({p})
        if t in tset:
            print('W: duplicate definition of package type "{}"'.format(t), file=sys.stderr)
            print('W: *** manual modification of debian/{}.install required ***'.format(p), file=sys.stderr)
        tset.update({t})
        ###################################################################
        # append dictionary to a list
        ###################################################################
        debs.append({'package': p, 
                'arch': a, 
                'multiarch': m, 
                'depends': dp, 
                'pre-depends': pd,
                'type': t})
    ###################################################################
    return debs

#######################################################################
# Test script
#######################################################################
if __name__ == '__main__':
    print(match_prefix('deb', 'deb'))
    if match_prefix('deb', 'deb'):
        print('deb match deb')
    else:
        print('deb not match deb')
    print('----- no dh_with')
#    dh_with = set()
#    binaryspec = '-,-doc:doc,libpackage1, libpackage-dev'
#    monoarch = False
#    debs(binaryspec, 'package', monoarch, dh_with)
#    print('----- dh_with python3')
#    dh_with = set({'python3'})
#    debs(binaryspec, 'package', monoarch, dh_with)
#    print('----- monoarch True dh_with python3')
#    monoarch = True
#    debs(binaryspec, 'package', monoarch, dh_with)
