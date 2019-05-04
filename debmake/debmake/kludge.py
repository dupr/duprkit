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
import collections
import glob
import itertools
import operator
import os
import re
import sys
import debmake.checkdep5
import debmake.scanfiles

re_round0 = re.compile(r'\.0')

def copydiff(mode, pedantic):
    ###########################################################################
    # parse existing debian/copyright against source tree
    ###########################################################################
    if not os.path.isfile('debian/copyright'):
        print('E: You need debian/copyright.')
        exit(1)
    with open('debian/copyright', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    patterns_for_license = []
    license = ''
    default_license = ''
    f_file = False
    f_cont = False
    f_license = False
    patterns = []
    iptn = -1
    licenses_old = {}
    file_to_pattern = {}
    for line in lines + ['']: # easy sure EOF
        line = line.rstrip()
        if line == '':
            # summarize data
            if patterns_for_license != [] and license != '':
                for ptn in patterns_for_license:
                    patterns.append(ptn)
                    if ptn == '*':
                        default_license = license
                    iptn += 1 # 0, 1, 2, 3 ...
                    globbed_file_or_dirs = glob.glob(ptn)
                    if globbed_file_or_dirs:
                        for file_or_dir in globbed_file_or_dirs:
                            if os.path.isfile(file_or_dir):
                                file_to_pattern[file_or_dir] = (iptn, ptn)
                                licenses_old[file_or_dir] = license
                                debmake.debug.debug('Dn: Pattern #{:02}: {}, file={}, {}'.format(iptn, ptn, file_or_dir, license), type='n')
                            elif os.path.isdir(file_or_dir):
                                for dir, subdirs, files in os.walk(file_or_dir):
                                    #debmake.debug.debug('Dn: Pattern #{:02}: {}, dir={}, files={}'.format(iptn, ptn, dir, files), type='n')
                                    for file in files:
                                        filepath = os.path.join(dir, file)
                                        file_to_pattern[filepath] = (iptn, ptn)
                                        licenses_old[filepath] = license
                                        debmake.debug.debug('Dn: Pattern #{:02}: {}, filepath={}, {}'.format(iptn, ptn, filepath, license), type='n')
                    else:
                        file_to_pattern['__MISSING__'] = (iptn, ptn)
                        licenses_old['__MISSING__'] = license
                        debmake.debug.debug('Dn: Pattern #{:02}: {}, file={}, {}'.format(iptn, ptn, '__MISSING__', license), type='n')
            # Next stanza
            patterns_for_license = []
            license = ''
            f_file = False
            f_cont = False
            f_license = False
        elif line[:6].lower() == 'files:':
            patterns_for_license += line[6:].split()
            f_file = True
            f_cont = True
        elif line[:8].lower() == 'license:':
            license = line[8:].strip()
            f_cont = False
        elif f_cont == True and line[:1] == ' ':
            patterns_for_license += line.split()
        elif f_cont == True and line[:1] == '\t':
            patterns_for_license += line.split()
        elif line[:1].lower() != ' ':
            f_cont = False
        else:
            pass
    nptn = iptn + 1
    ###########################################################################
    iptn_to_ptn = {}
    iptn_to_files = collections.defaultdict(list)
    for file, (iptn, ptn) in file_to_pattern.items():
        iptn_to_ptn[iptn] = ptn
        iptn_to_files[iptn].append(file)
        debmake.debug.debug('Dn: file="{}", iptn="{}", ptn="{}"'.format(file, iptn, ptn), type='n')
    if nptn != len(iptn_to_ptn):
        print("W: ***** Number of patterns unused: {} out of range(0, {}) *****".format(nptn - len(iptn_to_ptn), nptn), file=sys.stderr)
    ###########################################################################
    # scan copyright of the source tree and create license_new[]
    ###########################################################################
    (nonlink_files, xml_html_files, binary_files, huge_files, extcount, extcountlist) = debmake.scanfiles.scanfiles()
    data_new = debmake.checkdep5.checkdep5(nonlink_files, mode=1, pedantic=pedantic)
    licenses_new = {}
    for (licenseid, licensetext, files, copyright_lines) in data_new:
        licenseid = licenseid.strip()
        debmake.debug.debug('Dn: debian/copyright: "{}": {}'.format(licenseid, files), type='n')
        for file in files:
            licenses_new[file] = licenseid
    ###########################################################################
    # generate data with before/after
    ###########################################################################
    data = []
    for iptn in range(0, nptn):
        if iptn in iptn_to_ptn.keys():
            ptn = iptn_to_ptn[iptn]
            files = iptn_to_files[iptn]
        else:
            print('W: ***** Pattern #{:02}: "{}" unused, reorder debian/copyright *****'.format(iptn, patterns[iptn]), file=sys.stderr)
        for file in files:
            old = licenses_old[file]
            if file in licenses_new.keys():
                new = licenses_new[file]
            else:
                new = ''
            if new == '_SAME_' and default_license != '':
                new = default_license
            if old == new and mode <= 5:
                printdiff = False # exact match
            elif old.lower() == new.lower() and mode <= 4:
                printdiff = False # case insensitive match
            elif old.lower() == re_round0.sub('', new.lower()) and mode <= 4:
                printdiff = False # ignore tailing .0
            elif new =='' and mode <= 3:
                printdiff = False
            elif new[:2] == '__' and mode <= 2:
                printdiff = False
            else: # (old, new) not the same or mode >= 6
                printdiff = True
            data.append((iptn, ptn, file, printdiff, old, new))
    return data

def kludge(mode, pedantic):
    basedata = copydiff(mode, pedantic)
    iptn_group_data = []
    data = sorted(basedata, key=operator.itemgetter(0))
    for k, g in itertools.groupby(basedata, operator.itemgetter(0)):
        iptn_group_data.append(list(g))      # Store group iterator as a list
    data_iptn_licenses = []
    for iptn_group in iptn_group_data:
        licenses_group_data = []
        iptn_group = sorted(iptn_group, key=operator.itemgetter(4, 5))
        for k, g in itertools.groupby(iptn_group, operator.itemgetter(4, 5)):
            licenses_group_data.append(list(g))      # Store group iterator as a list
        data_iptn_licenses.append(licenses_group_data)
    print('=== debian/copyright checked for {} data ==='.format(len(basedata)))
    outdata = []
    for match_iptn in data_iptn_licenses:
        for match_licenses in match_iptn:
            files = []
            for match_iptn_licenses in match_licenses:
                (iptn, ptn, file, printdiff, old, new) = match_iptn_licenses
                if printdiff:
                    files.append(file)
            if files:
                outdata.append((iptn, ptn, files, printdiff, old, new))
    for outx in outdata:
        (iptn, ptn, files, printdiff, old, new) = outx
        print('Pattern #{:02}: {}'.format(iptn, ptn))
        print('  File: {}'.format('\n        '.join(files)))
        print('- {}'.format(old))
        print('+ {}'.format(new))
        print()

##############################################################################
if __name__ == '__main__':
    kludge(1, False)
