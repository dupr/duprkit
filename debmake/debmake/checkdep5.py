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
import glob
import hashlib
import itertools
import operator
import os
import re
import subprocess
import sys
import debmake.debug
import debmake.lc
###################################################################
# Constants for sanity
###################################################################
INITIAL_LINES = 1               # lines (if 1, first line only)
MAX_INITIAL_LINE_LENGTH = 2048  # chars. >> MAX_*_LINE_LENGTH
                                # check MAX_FILE_SIZE in scanfiles.py
MAX_TOTAL_LINES = 2048          # lines
NORMAL_LINE_LENGTH = 64         # chars
MIN_COPYRIGHT_LINE_LENGTH = 8   # chars
MAX_COPYRIGHT_LINE_LENGTH = 256 # chars
MAX_COPYRIGHT_LINES = 256       # lines
MAX_LICENSE_LINE_LENGTH = 1024  # chars
MAX_LICENSE_LINES = 1024        # lines
MAX_NON_ASCII = 0.25            # ratio
MAX_BAD_LINES = 4               # lines
###################################################################
# parse_lines() uses following state parameters to scan and extract
# in its MAIN-LOOP to generate:
#  * copyright_lines
#  * license_lines as list of string
###################################################################
#------------------------------------------------------------------
# format state lists
#------------------------------------------------------------------
fs = [
'F_BLNK', # Blank line
'F_QUOTE', # C /*...*/ in a line
'F_BLKP', # Python triple-quote
'F_BLKPE',
'F_BLKP0',
'F_BLKQ',
'F_BLKQE', # Python triple-doublequote
'F_BLKQ0',
'F_BLKC',
'F_BLKCE',
'F_BLKC2', # C /* multilines */
'F_BLKC1',
'F_BLKC0',
'F_PLAIN1', # Shell etc. #
'F_PLAIN2', # C++ //
'F_PLAIN3',
'F_PLAIN4',
'F_PLAIN5',
'F_PLAIN6',
'F_PLAIN7',
'F_PLAIN8',
'F_PLAIN9',
'F_PLAIN10',
'F_PLAIN11',
'F_PLAIN12',
'F_PLAIN0', # Before initial line), ignore until initial line
'F_PLAIN0U', # After  initial line), use line as is
'F_PLAIN0I', # After  initial line), ignore and insert blank line; or set EOF
'F_EOF', # force EOF before processing the next line
]
# enum(fs)
for (i, name) in enumerate(fs):
    exec('{} = {}'.format(name.strip(), i))
F_EOF = -1 # override

# entry format style id list
all_non_entry_formats = {
F_BLKPE, F_BLKP0,
F_BLKQE, F_BLKQ0,
F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0,
F_EOF}

all_formats = set()
all_entry_formats = set()
for name in fs:
    id = eval(name.strip())
    all_formats.add(id)
    if id not in all_non_entry_formats:
        all_entry_formats.add(id)

#------------------------------------------------------------------
# content_state
#------------------------------------------------------------------
cs = [
'C_INIT',  # initial content_state
'C_COPY',  # copyright found
'C_COPYB', # blank after C_COPY
'C_AUTH',  # AUTHOR: like
'C_AUTHB', # blank after C_AUTH
'C_LICN',  # license found
'C_LICNB', # blank after C_LICN
]
# enum(cs)
for (i, name) in enumerate(cs):
    exec('{} = {}'.format(name.strip(), i))

#------------------------------------------------------------------
# format rule definitions
#------------------------------------------------------------------
formats = {} # dictionary
# define next format state
# formats[*][0]: regex to match
# formats[*][1]: next format state allowed
# formats[*][2]: format state allowed (set this to persistent_format at the initial valid line)

# Blank line
formats[F_BLNK] = (
        re.compile(r"^(?P<prefix>)\s*(?P<text>)\s*(?P<postfix>)$"),  # Python
        all_entry_formats,
        all_entry_formats,
        )
# C /* ... */ in a line
formats[F_QUOTE] = (
        re.compile(r'^(?P<prefix>/\*+)\s*(?P<text>.*?)\s*(?P<postfix>\*+/)\s*(?://.*)?$'),  # C /*...*/ or C++ /*...*/  //...
        all_entry_formats,
        {F_QUOTE, F_PLAIN2, F_BLKC, F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0, F_BLNK}
        )

# python block mode start with '''
formats[F_BLKP] = (
        re.compile(r"^.*?(?P<prefix>''')\s*(?P<text>.*?)\s*(?P<postfix>)$"),  # Python
        [F_BLKPE, F_BLKP0],
        {F_BLKP, F_BLKPE, F_BLKP0, F_BLNK}
        )
formats[F_BLKPE] = (
        re.compile(r"^(?P<prefix>)\s*(?P<text>.*?)\s*(?P<postfix>''').*$"),  # Python
        all_entry_formats,
        {F_BLKP, F_BLKPE, F_BLKP0, F_BLNK}
        )
formats[F_BLKP0] = (
        re.compile(r'^(?P<prefix>)\s*(?P<text>.*?)\s*(?P<postfix>)$'),
        [F_BLKPE, F_BLKP0],
        {F_BLKP, F_BLKPE, F_BLKP0, F_BLNK}
        )

# python block mode start with """
formats[F_BLKQ] = (
        re.compile(r'^.*?(?P<prefix>""")\s*(?P<text>.*?)\s*(?P<postfix>)$'),  # Python
        [F_BLKQE, F_BLKQ0],
        {F_BLKQ, F_BLKQE, F_BLKQ0, F_BLNK}
        )
formats[F_BLKQE] = (
        re.compile(r'^(?P<prefix>)\s*(?P<text>.*?)\s*(?P<postfix>""").*$'),  # Python
        all_entry_formats,
        {F_BLKQ, F_BLKQE, F_BLKQ0, F_BLNK}
        )
formats[F_BLKQ0] = (
        re.compile(r'^(?P<prefix>)\s*(?P<text>.*?)\s*(?P<postfix>)$'),
        [F_BLKQE, F_BLKQ0],
        {F_BLKQ, F_BLKQE, F_BLKQ0, F_BLNK}
        )

# C block mode start with /* (But also C++ may)
formats[F_BLKC] = (
        re.compile(r'^(?P<prefix>/\*+)\s*(?P<text>.*?)\s*(?P<postfix>)$'),  # C /*...
        [F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0],
        {F_QUOTE, F_PLAIN2, F_BLKC, F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0, F_BLNK}
        )
formats[F_BLKCE] = (
        re.compile(r'^(?P<prefix>\*+|)\s*(?P<text>.*?)\s*(?P<postfix>\*+/).*$'),  # C ...*/ or *...*/
        all_entry_formats,
        {F_QUOTE, F_PLAIN2, F_BLKC, F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0, F_BLNK}
        )
formats[F_BLKC2] = (
        re.compile(r'^(?P<prefix>\*+)\s*(?P<text>.*?)\s*(?P<postfix>\*+)$'),  # C *...*
        [F_BLKCE, F_BLKC2],
        {F_QUOTE, F_PLAIN2, F_BLKC, F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0, F_BLNK}
        )
formats[F_BLKC1] = (
        re.compile(r'^(?P<prefix>\*+)\s*(?P<text>.*?)\s*(?P<postfix>)$'),  # C *...
        [F_BLKCE, F_BLKC1],
        {F_QUOTE, F_PLAIN2, F_BLKC, F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0, F_BLNK}
        )
formats[F_BLKC0] = (
        re.compile(r'^(?P<prefix>)\s*(?P<text>.*?)\s*(?P<postfix>)$'), # bare lines
        [F_BLKCE, F_BLKC0],
        {F_QUOTE, F_PLAIN2, F_BLKC, F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0, F_BLNK}
        )

# comment start with something
formats[F_PLAIN1] = (
        re.compile(r'^(?P<prefix>#+)\s*(?P<text>.*?)\s*(?P<postfix>)$'),   # Shell/Perl/Python
        all_entry_formats,
        {F_PLAIN1, F_BLNK}
        )

formats[F_PLAIN2] = (
        re.compile(r'^(?P<prefix>//+)\s*(?P<text>.*?)\s*(?P<postfix>)$'),  # C++ // or C(new)
        all_entry_formats,
        {F_QUOTE, F_PLAIN2, F_BLKC, F_BLKCE, F_BLKC2, F_BLKC1, F_BLKC0, F_BLNK}
        )

formats[F_PLAIN3] = (
        re.compile(r'^(?P<prefix>--+)\s*(?P<text>.*?)\s*(?P<postfix>)$'),  # Lua --
        all_entry_formats,
        {F_PLAIN3, F_BLNK}
        )

formats[F_PLAIN4] = (
        re.compile(r'^(?P<prefix>\.\\")\s*(?P<text>.*?)\s*(?P<postfix>)$'), # manpage
        all_entry_formats,
        {F_PLAIN4, F_BLNK}
        )

formats[F_PLAIN5] = (
        re.compile(r'^(?P<prefix>@%:@)\s*(?P<text>.*?)\s*(?P<postfix>)$'),  # autom4te.cache
        all_entry_formats,
        {F_PLAIN5, F_BLNK}
        )

formats[F_PLAIN6] = (
        re.compile(r'^(?P<prefix>@c)\s*(?P<text>.*?)\s*(?P<postfix>)$'), # Texinfo @c
        all_entry_formats,
        {F_PLAIN6, F_BLNK}
        )

formats[F_PLAIN7] = (
        re.compile(r"^(?P<prefix>')\s*(?P<text>.*?)\s*(?P<postfix>)$"),# Basic
        all_entry_formats,
        {F_PLAIN7, F_BLNK}
        )

formats[F_PLAIN8] = (
        re.compile(r'^(?P<prefix>;+)\s*(?P<text>.*?)\s*(?P<postfix>)$'),# vim
        all_entry_formats,
        {F_PLAIN8, F_BLNK}
        )

formats[F_PLAIN9] = (
        re.compile(r'^(?P<prefix>dnl)\s*(?P<text>.*?)\s*(?P<postfix>)$'),# m4 dnl
        all_entry_formats,
        {F_PLAIN9, F_BLNK}
        )

formats[F_PLAIN10] = (
        re.compile(r'^(?P<prefix>%)\s*(?P<text>.*?)\s*(?P<postfix>)$'),# texinfo.tex
        all_entry_formats,
        {F_PLAIN10, F_BLNK}
        )

formats[F_PLAIN11] = (
        re.compile(r'^(?P<prefix>!+)\s*(?P<text>.*?)\s*(?P<postfix>)$'),# vim
        all_entry_formats,
        {F_PLAIN11, F_BLNK}
        )

formats[F_PLAIN12] = (
        re.compile(r'^(?P<prefix>")\s*(?P<text>.*?)\s*(?P<postfix>)$'),# vim
        all_entry_formats,
        {F_PLAIN12, F_BLNK}
        )

# Last rule before initial line, no leading character
formats[F_PLAIN0] = (
        re.compile(r'^(?P<prefix>)\s*(?P<text>.*?)\s*(?P<postfix>)$'),     # Text
        all_entry_formats,
        {F_PLAIN0U}
        )

# Last rule after initial line with no leading character, line as is with no leading character
formats[F_PLAIN0U] = (
        re.compile(r'^(?P<prefix>)\s*(?P<text>.*?)\s*(?P<postfix>)$'),     # Text
        {F_PLAIN0U},
        {} # never used
        )

# Last rule after initial line, practically blank line as blank line or EOF
formats[F_PLAIN0I] = (
        re.compile(r'^(?P<prefix>)\s*(?P<text>.*?)\s*(?P<postfix>)$'),     # Text
        all_entry_formats,
        {} # never used
        )

###################################################################
# parse_lines() uses regex to change state in its MAIN-LOOP:
###################################################################
# Be careful with " " in regex with re.VERBOSE ==> Use \s
#------------------------------------------------------------------
# Extract copyright+license from a source file
#------------------------------------------------------------------
# pre-process line (drop anywhere)
re_preprocess_drop = re.compile(r'''(?:
        ^timestamp=.*$|                         # timestamp line
        ^scriptversion=.*$|                     # version line
        ^\$.*:.*\$|                             # CVS/RCS version
        ^-\*-\s+coding:.*-\*-.*$|               # EMACS
        ^vim?:.*$|                              # VIM/VI
        All\s+Rights?\s+Reserved.?|             # remove
        <BR>|                                   # HTML
        ^\.bp                                   # manpage
        )''', re.IGNORECASE | re.VERBOSE)
# some of the above are duplicate of re_license_drop
# removal in preproces ensures not to miss extracting the license section

re_license_end_always = re.compile(r'''(
        ^EOT$|^EOF$|^EOL$|^END$|        # shell <<EOF like lines
        ^msgid\s|                       # po/pot
        ^msgstr\s                       # po/pot
        )''', re.IGNORECASE | re.VERBOSE)

re_license_end_no_init = re.compile(r'''(
        [=?_]|                          # C MACRO code
        ^#if|                           # C CPP
        ^#include|                      # C CPP
        ^static\s+.*=|                  # C
        ^const\s+.*=|                   # C
        ^struct\s+.*=|                  # C
        enum\s.*\s{|                    # C enum
        class\s.*\s{|                   # C++
        ^"""|^\'\'\'|                   # python block comment
        ^=cut|                          # perl
        ^---|^@@|                       # diff block
        ^\.TH|                          # no .TH for manpage
        ^\.SH|                          # no .SH for manpage
        ^Who\sare\swe\?$|               # The Linux Foundation License templates
        ^-----------|                   # ./configure
        ^Usage:|                        # ltmain.sh
        ^serial\s+[0-9]|                # aclocal.m4
        ^@configure_input@|             # ltversion.m4
        ^This\sfile\sis\smaintained|    # Automake files
        ^Basic\sInstallation\s          # INSTALL
        ^Do\sall\sthe\swork\sfor\sAutomake| # aclocal.m4 Automake
        ^Originally\s+written\s+by\+.{10,20}?\s+Please\s+send\spatches| # config.guess
        ^Please\s+note\s+that\s+the| # Makefile.in.in (gettext)
        ^Please\s+send\s+patches\s+with|   # config.sub
        ^Please\s+send\s+patches\s+to|  # config.sub, config.guess
        ^if\s+not\s+1,\s+datestamp\s+to\s+the\s+version\s+number|  # configure.ac
        ^the\s+first\s+argument\s+passed\s+to\s+this\s+file|  # config.rpath
        ^You\s+can\s+get\s+the\s+latest\s+version\s+of| # config.guess GPL3+ based
        ^@include|                      # Texinfo
        ^@end|                          # Texinfo
        ^%\*\*|                         # Texinfo
        ^Module\s+Name|                 # ASM
        ^Local\s+includes|              # C++ (aptitude)
        ^System\s+includes|             # C++ (aptitude)
        ^Please\s+try\s+the\s+latest\s+version\s+of # Texinfo.tex
        )''', re.IGNORECASE | re.VERBOSE)

# Now line starting with Copyright (c)
re_copyright_maybe = re.compile(r'''^\s*
        (?:
            (?:\(C\)|©)?\s*
            (?:portions\s+|Partly\s+based\s+on\s+code\s+)?
            (?:Copyright|Copyr\.)\s*
            (?:\(C\)|©)?\s*
        |(?:\(C\)|©)\s*
        |\\\(co\s*
        ) # for vim syntax highlighter
        (?P<copyright>.*)$
        ''', re.IGNORECASE | re.VERBOSE)

# matching line is excluded to be identified as copyright.
re_copyright_exclude = re.compile(r'''(?:
        [=?$]|                  # C MACRO
        YEAR|                   # template
        YOUR\s+NAME|            # template
        name\s+of\s+author|     # template
        Copyright[^\s(:]|       # text or variable name
        Copyright:?$|           # text
        Copyright\s+notice|     # text
        Copyright\s+holder|     # text
        Copyright\s+section|    # text
        Copyright\s+stanza|     # text
        copyright\s+file|       # text
        copyright\s+and\s+license # text
        )''', re.IGNORECASE | re.VERBOSE)

def copyright_start(line):
    m1 = re_copyright_maybe.search(line)
    m2 = re_copyright_exclude.search(line)
    if m1 and not m2:
        return m1.group('copyright').strip()
    else:
        return False

re_author_maybe = re.compile(r'''^\s*(?:
        authors?[\s:]|
        maintainers?[\s:]|
        translators?[\s:])
        \s*(?P<author>.*)\s*$
        ''', re.IGNORECASE | re.VERBOSE)

re_author_exclude = re.compile(r'''(
        ^authors?\sbe\s|
        ^authors?\sor\s
        )''', re.IGNORECASE | re.VERBOSE)

def author_start(line):
    m1 = re_author_maybe.search(line)
    m2 = re_author_exclude.search(line)
    if m1 and not m2:
        return m1.group('author').strip()
    else:
        return False

re_license = re.compile(r'''(
        ^Copying\s+and\s+distribution\s+of\s+this\s+file|       # PERMISSIVE
        ^Distributed\s+under\s+the\s+Boost\s+Software\s+License,|   # Boost
        ^Everyone\s+is\s+permitted\s+to\s+copy\s+and\s+distribute|  # GNU FULL
        ^Distribute\s+under\s[AL]?GPL\s+version|                # GPL short
        ^Licensed\s+to\s+the\s+Apache\s+Software\s+Foundation|  #Apache-2.0_var1
        ^Licensed\s+under\s+|                                   # ECL
        ^Licensed\s+under\s+the\s+Apache\s+License|             #Apache-2.0_var2
        ^License\s+Applicability.\s+Except\s+to\s+the\s+extent\s+portions|  # SGI
        ^Permission\s+is\s+granted\s+to\s+copy,\s+distribute|   # GFDL 1.1
        ^Permission\s+is\s+hereby\s+granted|                    # MIT
        ^Permission\s+to\suse,\s+copy,\s+modify|                # ISC
        ^Redistribution\s+and\s+use\s+in\s+source\s+and\s+binary\s+forms|   # Apache 1.0/BSD
        ^The\s+contents\s+of\s+this\s+file|                     # ErlPL, ...
        ^The\s+contents\s+of\s+this\s+file\s+are\s+subject\s+to| # MPL-1.0 1.1
        ^This\s+.{2,40}\s+is\s+free\s+software|                 # makefile.in etc.
        ^This\s+file\s+is\s+distributed\s+under\s+the\s+same\s+license\s+as\s+.{5,40}\.$| # same
        ^This\s+library\s+is\s+free\s+software|                 # LGPL variants
        ^This\s+license\s+is\s+a\s+modified\s+version\s+of\s+the|   # AGPL-1.0
        ^This\s+program\s+can\s+redistributed|                  # LaTeX LPPL 1.0
        ^This\s+program\s+is\s+free\s+software|                 # GPL variants
        ^This\s+program\s+may\s+be\s+redistributed|             # LaTeX LPPL 1.1 1.2
        ^This\s+software\s+is\s+furnished\s+under\s+license|    # DEC
        ^This\s+software\s+is\s+provided\s+|                    # Zlib
        ^This\s+Source\s+Code\s+Form\s+is\s+subject\s+to\s+the\s+terms\s+of| # MPL 2.0
        ^This\s+work\s+is\s+distributed\s+under|                # W3C
        ^This\s+work\s+may\s+be\s+redistributed|                # LaTeX LPPL 1.3
        ^This\s+program\s+and\s+the\+accompanying\s+materials|  # INTEL
        ^unless\s+explicitly\s+acquired\s+and\s+licensed        # Watcom
        )''', re.IGNORECASE | re.VERBOSE)

def license_start(line):
    m1 = re_license.search(line)
    return m1

# COPY/AUTH continue? (FSF address etc.)
re_no_year = re.compile(r'''
        ^675\s+Mass\s+Ave|
        ^59\s+Temple|
        ^510\s+Third|                # Affero
        ^51\s+Franklin               # last line without bar
        ''', re.IGNORECASE | re.VERBOSE)

# COPY/AUTH --> LICN
re_license_maybe = re.compile(r'''(
        ^Copying\s|
        ^Everyone\s|
        ^Licensed\s|
        ^License\s|
        ^Permission\s|
        ^Redistribution\s|
        ^This\s|
        ^GNU\s+General\s+Public\s+License\s+|                   # 1 liner GPL
        ^GPL|                                                   # 1 liner GPL
        ^LGPL|                                                  # 1 liner GPL
        ^BSD|                                                   # 1 liner BSD
        ^MIT|                                                   # 1 liner MIT
        ^Unless\s|
        \sare\s|
        \sis\s|
        \sdistributed\s
        )''', re.IGNORECASE | re.VERBOSE)

# In the above and re_license_drop, please do not try to drop simple
# "written by ..." or "originally written by ..." line.  That has negative impact.
# !!! Better to be safe than sorry !!!

# This should be also listed in re_license_start_sure
re_license_end_next = re.compile(r'''(
    ^This\s+file\s+is\s+distributed\s+under\s+the\s+same\s+license\s+as\s+.{5,40}\.$
        )''', re.IGNORECASE | re.VERBOSE)

###################################################################
# parse_lines() uses following to process line in its MAIN-LOOP:
###################################################################
#------------------------------------------------------------------
# process line to identify new state based on above definitions
#------------------------------------------------------------------
def check_format_style(line, xformat_state, persistent_format):
    # main process loop
    prefix = ''
    postfix = ''
    format_state = F_EOF
    formats_allowed = formats[xformat_state][1]
    for f in formats_allowed:
        if f in persistent_format:
            regex = formats[f][0]
            m = regex.search(line)
            if m:
                line = m.group('text').strip()
                prefix = m.group('prefix') # for debug output
                postfix = m.group('postfix') # for debug output
                format_state = f
                break
    debmake.debug.debug('Ds: format={}->{}, prefix="{}", postfix="{}": "{}"'.format(fs[xformat_state], fs[format_state], prefix, postfix, line), type='s')
    return (line, format_state)
#------------------------------------------------------------------
# count non-ascii characters
#------------------------------------------------------------------
re_ascii = re.compile('[\s!-~]')

def len_non_ascii(line):
    non_ascii = re_ascii.sub('', line)
    if non_ascii:
        n_non_ascii = len(non_ascii)
    else:
        n_non_ascii = 0
    return n_non_ascii
###################################################################
# parse_lines() uses followings in its POST-PROCESS to generate:
#  * copyright_data (dictionary holding tuple)
#  * license_lines  (cleaned-up strings)
###################################################################
#------------------------------------------------------------------
# split copyright line into years and name
#------------------------------------------------------------------
re_year_yn = re.compile(r'''^
        (?P<year>\d\d[-,.;\s\d]*):?\s*
        (?P<name>\D.*)$''', re.IGNORECASE | re.VERBOSE)

re_year_ny = re.compile(r'''^
        (?P<name>.*?\D)\s*
        (?P<year>\d\d[-.,;\s\d]*)$''', re.IGNORECASE | re.VERBOSE)
def split_years_name(copyright_line, pedantic=False):
    # copyright_line: leading "Copyright (c)" is removed in MAIN-LOOP
    copyright_line = copyright_line.strip()
    if (not pedantic) and copyright_line[:2] == '__':
        # If copyright_line starts '__' non-valid data marker, treat it as no data unless pedantic
        years = ''
        name = ''
    else:
        # split copyright_line into years and name
        m1 = re_year_yn.search(copyright_line)
        m2 = re_year_ny.search(copyright_line)
        if m1:
            years = m1.group('year').strip()
            name = m1.group('name').strip()
        elif m2:
            years = m2.group('year').strip()
            name = m2.group('name').strip()
        elif copyright_line:
            years = 'NO_MATCH' # sign for funkey copyright_line
            name = copyright_line.strip()
        else:
            years = ''
            name = ''
    debmake.debug.debug('Dy: years="{}", name="{}" <- "{}"'.format(years, name, copyright_line), type='y')
    return (years, name)

#------------------------------------------------------------------
# Parse years into tuple (year_min, year_max)
#------------------------------------------------------------------
re_year_1900 = re.compile(r'''
        (?P<pre>.*?)
        (?P<n1>19\d\d)\s*[-,]\s*
        (?P<n2>\d\d)
        (?P<post>\D.*|$)''', re.IGNORECASE | re.VERBOSE)

re_year_2000 = re.compile(r'''
        (?P<pre>.*?)
        (?P<n1>20\d\d)\s*[-,]\s*
        (?P<n2>\d\d)
        (?P<post>\D.*|$)''', re.IGNORECASE | re.VERBOSE)

re_year = re.compile(r'\d\d+')

def get_year_range(years):
    # 1990-91 -> 1990-1991 etc.
    while True:
        m = re_year_1900.search(years)
        if m:
            years = m.group('pre') + m.group('n1') + '-19' + \
                    m.group('n2') + m.group('post')
        else:
            break
    # 2010-11 -> 2010-2011 etc.
    while True:
        m = re_year_2000.search(years)
        if m:
            years = m.group('pre') + m.group('n1') + '-20' + \
                    m.group('n2') + m.group('post')
        else:
            break
    # year range
    year_min = 9999
    year_max = 0
    for year_string in re_year.findall(years):
        year = int(year_string)
        year_min =  min(year_min, year)
        year_max =  max(year_max, year)
    return (year_min, year_max)

#------------------------------------------------------------------
# Parse name to remove junks
#------------------------------------------------------------------
re_name_drop = re.compile(r'''
        (?:originally\s+)?(?:written\s+)?by
        ''', re.IGNORECASE | re.VERBOSE)

re_fsf_addr = re.compile(r'^Free\s+Software\s+Foundation,\s+Inc\.',
        re.IGNORECASE)

def normalize_name(name):
    name = name.strip()
    name = re_name_drop.sub('', name).strip()
    if re_fsf_addr.search(name): # If FSF, strip address etc.
        name = 'Free Software Foundation, Inc.' 
    return name

#------------------------------------------------------------------
# Analyze all copyright_lines into copyright_data
#------------------------------------------------------------------
def analyze_copyright(copyright_lines, file, utf8=True, pedantic=False):
    #------------------------------------------------------------------
    # sanitize copyright_lines
    #------------------------------------------------------------------
    n_copyright_lines = len(copyright_lines)
    if n_copyright_lines > MAX_COPYRIGHT_LINES:
        copyright_lines = [ "__MANY_COPYRIGHT_LINES__({}lines) in: {}".format(n_copyright_lines, file) ]
    for (i, copyright_line) in enumerate(copyright_lines):
        copyright_line = copyright_line.strip()
        copyright_lines[i] = copyright_line
        n_copyright = len(copyright_line)
        if n_copyright < MIN_COPYRIGHT_LINE_LENGTH:
            copyright_lines[i] = "__SHORT_LINE__({}chars.) in: {}[{}]".format(n_copyright, file, i)
        if n_copyright > MAX_COPYRIGHT_LINE_LENGTH:
            copyright_lines[i] = "__LONG_LINE__({}chars.) in: {}[{}]".format(n_copyright, file, i)
        if not utf8:
            n_non_ascii = len_non_ascii(copyright_line)
            if (n_copyright * MAX_NON_ASCII) < n_non_ascii:
                copyright_lines[i] = "__MANY_NON_ASCII__({}chars. over {}chars.) in: {}[{}]".format(n_non_ascii, n_copyright, file, i)
    copyright_data = {}
    for copyright_line in copyright_lines:
        (years, name) = split_years_name(copyright_line, pedantic=pedantic)
        name = normalize_name(name).strip()
        (year_min, year_max) = get_year_range(years)
        if name in copyright_data.keys():
            (year0_min, year0_max) = copyright_data[name]
            year_min =  min(year_min, year0_min)
            year_max =  max(year_max, year0_max)
        if name:
            copyright_data[name] = (year_min, year_max)
        else:
            print('W: analyze_copyright: skip name="", years={}-{}'.format(year_min, year_max), file=sys.stderr)
    return copyright_data

#------------------------------------------------------------------
# Clean license
#------------------------------------------------------------------
re_license_drop = re.compile(r'''
        ^timestamp=.*$|             # timestamp line
        ^scriptversion=.*$|         # version line
        ^\$Id:.*\$|                 # CVS/RCS version
        ^-\*-\s+coding:.*-\*-.*$|   # EMACS
        ^vim?:.*$|                  # VIM/VI
        ^@file.*$|                  # embedded texinfo
        ^\\.*$                      # embedded texinfo?
        ''', re.IGNORECASE | re.VERBOSE)
# The above needs to be duplicated to be included in re_preprocess_drop

def clean_license(license_lines, file, utf8=True, pedantic=False):
    #------------------------------------------------------------------
    # sanitize license_lines
    #------------------------------------------------------------------
    n_license_lines = len(license_lines)
    if n_license_lines > MAX_LICENSE_LINES:
        license_lines = [ "__MANY_LICENSE_LINES__({}lines) starting with: {}".format(n_license_lines, license_lines[0][0:NORMAL_LINE_LENGTH]) ]
    for (i, license_line) in enumerate(license_lines):
        if license_line[0:len(file) + 1] == (file + ':'):
            license_lines[i] = ''
        license_lines[i] = re_license_drop.sub('', license_lines[i])
    bad_lines = 0
    for (i, license_line) in enumerate(license_lines):
        license_line = license_line.strip()
        license_lines[i] = license_line
        n_license = len(license_line)
        if n_license > MAX_LICENSE_LINE_LENGTH:
            bad_lines = bad_lines + 1
            if bad_lines < MAX_BAD_LINES:
                license_lines[i] = "_LONG_LINE_({}chars.) starting with: {}".format(n_license, license_line[0:NORMAL_LINE_LENGTH])
            else:
                license_lines[i] = "_LONG_LINE_({}chars.) ... truncated.: {}".format(n_license)
                license_lines = license_lines[0:i+1]
                break
        if not utf8:
            n_non_ascii = len_non_ascii(license_line)
            if (n_license * MAX_NON_ASCII) < n_non_ascii:
                bad_lines = bad_lines + 1
                if bad_lines < MAX_BAD_LINES:
                    license_lines[i] = "_MANY_NON_ASCII_({}chars. over {}chars.) starting with: {}".format(n_non_ascii, n_license, license_line[0:NORMAL_LINE_LENGTH])
                else:
                    license_lines[i] = "_MANY_NON_ASCII_({}chars. over {}chars.) ... truncated.".format(n_non_ascii, n_license)
                    license_lines = license_lines[0:i+1]
                    break
    # Drop consecutive blank lines
    i = 0
    f_blank = True
    while i < len(license_lines):
        if license_lines[i] == '':
            if f_blank:
                del license_lines[i]
            else:
                i = i + 1
            f_blank = True
        else:
            f_blank = False
            i = i + 1
    if len(license_lines) > 0 and license_lines[-1] == '':
        del license_lines[-1]
    return license_lines

##########################################################################
# format_string and content_string
##########################################################################
def format_string(format):
    return ','.join(map(lambda f: fs[f], sorted(format)))

def content_string(content):
    return ','.join(map(lambda c:cs[c], sorted(content)))

##########################################################################
# Main text process loop over lines
##########################################################################
def parse_lines(lines, file, utf8=True, pedantic=False):
    persistent_format = all_formats
    valid_lines = 0 # increment if COPY or LICN found
    format_state = F_PLAIN0
    content_state = C_INIT
    format_found = set()
    content_found = {C_INIT}
    copyright_lines = []
    license_lines = []
    author_lines = []
    ##########################################################################
    # MAIN-LOOP for lines (start)
    ##########################################################################
    for (i, line) in enumerate(lines):
        # set previous values
        xformat_state = format_state
        xcontent_state = content_state
        debmake.debug.debug('Db: begin xformat={}, xcontent={}, format_found={}, content_found={}: "{}"'.format(fs[xformat_state], cs[xcontent_state], format_string(format_found), content_string(content_found), line), type='b')
        if i > MAX_TOTAL_LINES:
            if license_lines != []:
                license_lines.append("__MANY_TOTAL_LINES__({}lines) truncating at: {}".format(i, line[0:NORMAL_LINE_LENGTH]))
        #------------------------------------------------------------------
        # pre-process line
        #------------------------------------------------------------------
        line = line.strip()
        # drop magic line for debmake testing
        if line[0:7] == "#%#%#%#":
            line = ''
        if i < INITIAL_LINES:
            n = len(line)
            if n > MAX_INITIAL_LINE_LENGTH:
                copyright_lines.append("__INITIAL_LONG_LINE__({}chars.) in: {}[{}]".format(n, file, i))
                #license_lines.append("__INITIAL_LONG_LINE__ (binary file?)")
                break
            if not utf8:
                n_non_ascii = len_non_ascii(line)
                if (n * MAX_NON_ASCII) < n_non_ascii:
                    copyright_lines.append("__INITIAL_NON_ASCII_LINE__({}chars.) in: {}[{}]".format(n, file, i))
                    #license_lines.append("__INITIAL_NON_ASCII_LINE__ (binary file?)")
                    break
        if line[:1] == '+': # hack to drop patch (1 level)
            line = line[1:]
        if line == '.':     # empty line only with . as empty
            line = ''
        if line[:len(file)] == file:
            line = ""
        line= re_preprocess_drop.sub('', line)
        line = line.strip()
        #------------------------------------------------------------------
        # procss line (Now line does not have formatting characters)
        #------------------------------------------------------------------
        (line, format_state) = check_format_style(line, xformat_state, persistent_format)
        # If the line is EOF, exit
        if format_state == F_EOF:
            break
        if xcontent_state != C_INIT:
            format_found |= {format_state}
        #------------------------------------------------------------------
        # MAIN IF BRANCHING
        #------------------------------------------------------------------
        # ending ?
        if re_license_end_always.search(line): # end no matter what
            debmake.debug.debug('Dm: license_end_always: "{}"'.format(line), type='m')
            break
        elif xcontent_state != C_INIT and \
                re_license_end_no_init.search(line):
            debmake.debug.debug('Dm: xcontent_state != C_INIT and license_end_no_init: "{}"'.format(line), type='m')
            break
        # blank line
        elif line == '':
            if xcontent_state == C_COPY:
                debmake.debug.debug('Dm: C_COPY + blank line', type='m')
                content_state = C_COPYB
                content_found |= {C_COPYB}
            elif xcontent_state == C_LICN:
                debmake.debug.debug('Dm: C_LICN + blank line', type='m')
                license_lines.append(line)
                content_state = C_LICNB
                content_found |= {C_LICNB}
            elif xcontent_state == C_AUTH:
                debmake.debug.debug('Dm: C_AUTH + blank line', type='m')
                content_state = C_AUTHB
                content_found |= {C_AUTHB}
            else:
                debmake.debug.debug('Dm: repeated blank lines', type='m')
        # starting a new section (C_INIT->... and others->...)
        elif xcontent_state != C_LICN and copyright_start(line):
            debmake.debug.debug('Dm: xcontent_state != C_LICN and copyright_start: "{}"'.format(line), type='m')
            line = copyright_start(line)
            if line:
                copyright_lines.append(line)
            content_state = C_COPY
            content_found |= {C_COPY}
            valid_lines += 1
            if valid_lines == 1: # The first valid line after C_INIT
                persistent_format = formats[format_state][2] # set
                debmake.debug.debug('Dm: persistent: "{}"'.format(format_string(persistent_format)), type='m')
        elif xcontent_state != C_LICN and author_start(line): # author_start_sure
            debmake.debug.debug('Dm: xcontent_state != C_LICN and author_start: "{}"'.format(line), type='m')
            line = author_start(line)
            if line:
                author_lines.append(line)
            content_state = C_AUTH
            content_found |= {C_AUTH}
            valid_lines += 1
            if valid_lines == 1: # The first valid line after C_INIT
                persistent_format = formats[format_state][2] # set
                debmake.debug.debug('Dm: persistent: "{}"'.format(format_string(persistent_format)), type='m')
        elif license_start(line):
            debmake.debug.debug('Dm: license_start_sure: "{}"'.format(line), type='m')
            license_lines.append(line)
            content_state = C_LICN
            content_found |= {C_LICN}
            valid_lines += 1
            if valid_lines == 1: # The first valid line after C_INIT
                persistent_format = formats[format_state][2] # set
                debmake.debug.debug('Dm: persistent: "{}"'.format(format_string(persistent_format)), type='m')
            if re_license_end_next.search(line):
                break
        # special transitions: COPY/AUTH --> LICN
        elif xcontent_state in [C_COPY, C_AUTH] and re_license_maybe.search(line):
            debmake.debug.debug('Dm: xcontent_state in [C_INIT, C_COPY, C_AUTH] and license_maybe: "{}"'.format(line), type='m')
            license_lines.append(line)
            license_found = True
            content_state = C_LICN
            content_found |= {C_LICN}
        elif xcontent_state == C_LICN: # line != ''
            debmake.debug.debug('Dm: C_LICN + non-blank line: "{}"'.format(line), type='m')
            license_lines.append(line)
            content_state = C_LICN
            content_found |= {C_LICN}
        # All C_INIT -> other section transitions have been exhausted
        elif xcontent_state == C_INIT:
            debmake.debug.debug('Dm: C_INIT cont, ignore: "{}"'.format(line), type='m')
            content_state = C_INIT
            content_found |= {C_INIT}
        elif xcontent_state == C_COPY:
            debmake.debug.debug('Dm: copyright_cont: "{}"'.format(line), type='m')
            if len(copyright_lines) == 0:
                copyright_lines = [ line ]
            elif re_no_year.search(line):
                copyright_lines[-1] = (copyright_lines[-1] + ' ' + line).strip()
            elif copyright_lines[-1][-1:] == ',' and line[:1] in '0123456789':
                copyright_lines[-1] = (copyright_lines[-1] + line).strip()
            elif line[:1] not in '0123456789':
                copyright_lines[-1] = (copyright_lines[-1] + ' ' + line).strip()
            else:
                copyright_lines.append(line)
            content_state = C_COPY
            content_found |= {C_COPY}
        elif xcontent_state == C_AUTH:
            debmake.debug.debug('Dm: author_cont: "{}"'.format(line), type='m')
            if len(author_lines) == 0:
                author_lines = [ line ]
            elif re_no_year.search(line):
                author_lines[-1] = (author_lines[-1] + ' ' + line).strip()
            elif author_lines[-1][-1:] == ',' and line[:1] in '0123456789':
                author_lines[-1] = (author_lines[-1] + line).strip()
            elif line[:1] not in '0123456789':
                author_lines[-1] = (author_lines[-1] + ' ' + line).strip()
            else:
                author_lines.append(line)
            content_state = C_AUTH
            content_found |= {C_AUTH}
        elif xcontent_state == C_AUTH: # line != ''
            debmake.debug.debug('Dm: C_AUTH + non-blank line: "{}"'.format(line), type='m')
            author_lines.append(line)
            content_state = C_AUTH
            content_found |= {C_AUTH}
        elif xcontent_state == C_COPYB: # line != ''
            debmake.debug.debug('Dm: C_COPYB + non-blank line: "{}"'.format(line), type='m')
            license_lines.append(line)
            content_state = C_LICN
            content_found |= {C_LICN}
        elif xcontent_state == C_LICNB: # line != ''
            debmake.debug.debug('Dm: C_LICNB + non-blank line: "{}"'.format(line), type='m')
            license_lines.append(line)
            content_state = C_LICN
            content_found |= {C_LICN}
        elif xcontent_state == C_AUTHB: # line != ''
            debmake.debug.debug('Dm: C_AUTHB + non-blank line: "{}"'.format(line), type='m')
            license_lines.append(line)
            content_state = C_LICN
            content_found |= {C_LICN}
        else: # should not be here
            print('W: !!!!! format={}->{}, content={}->{}, format_found={}, content_found={}: "{}"'.format(fs[xformat_state], fs[format_state], cs[xcontent_state], cs[content_state], format_string(format_found), content_string(content_found), line), file=sys.stderr)
            print('W: !!!!! assertion error, exit loop !!!!!', file=sys.stderr)
            break
        debmake.debug.debug('De: *end* format={}->{}, content={}->{}, format_found={}, content_found={}: "{}"'.format(fs[xformat_state], fs[format_state], cs[xcontent_state], cs[content_state], format_string(format_found), content_string(content_found), line), type='e')
    ##########################################################################
    # MAIN-LOOP (end)
    ##########################################################################

    ##########################################################################
    # POST-PROCESS
    ##########################################################################
    #------------------------------------------------------------------
    # analyze_copyright and clean_license
    #------------------------------------------------------------------
    copyright_data = analyze_copyright(copyright_lines, file, utf8=utf8, pedantic=pedantic)
    license_lines = clean_license(license_lines, file, utf8=utf8, pedantic=pedantic)
    debmake.debug.debug('Da: AUTHOR(s)/TRANSLATOR(s):', type='a')
    for line in author_lines:
        debmake.debug.debug('Da: {}'.format(line), type='a')
    return (copyright_data, license_lines)

###################################################################
# Check license of a text file
###################################################################
def parse_encoded_lines(file, encoding='utf-8', pedantic=False):
    ###################################################################
    # Start analyzing file (default encoding)
    ###################################################################
    try:
        with open(file, 'r', encoding=encoding) as fd:
            (copyright_data, license_lines) = parse_lines(fd.readlines(), file, utf8=True, pedantic=pedantic)
    ###################################################################
    # Fall back for analyzing file (latin-1 encoding)
    ###################################################################
    except UnicodeDecodeError as e:
        print('W: Non-UTF-8 char found, using latin-1: {}'.format(file), file=sys.stderr)
        fd.close()
        with open(file, 'r', encoding='latin-1') as fd:
            (copyright_data, license_lines) = parse_lines(fd.readlines(), file, utf8=False, pedantic=pedantic)
    return (copyright_data, license_lines)

###################################################################
# Check autogenerated files
###################################################################
re_autofiles = re.compile(r'''(
        ^Makefile.in$| # Autotools
        ^.*/Makefile\.in$| # Autotools
        ^aclocal.m4$| # Autotools
        ^build-aux/.*$| # Autotools
        ^(?:config/)?compile$| # Autotools
        ^(?:config/)?config\.guess$| # Autotools
        ^(?:config/)?config\.rpath$| # Autotools
        ^(?:config/)?config\.sub$| # Autotools
        ^(?:config/)?depcomp$| # Autotools
        ^(?:config/)?install-sh$| # Autotools
        ^(?:config/)?ltmain.sh$| # Autotools
        ^(?:config/)?missing$| # Autotools
        ^(?:config/)?mkinstalldirs$| # Autotools
        ^(?:config/)?test-driver$| # Autotools
        ^config\.status$| # Autotools
        ^configure$| # Autotools
        ^libltdl/.*$| # Autotools
        ^libtool$| # Autotools
        ^py-compile$| # Autotools
        ^po/Makefile$| # Autotools (getttext)
        ^po/Makefile\.in$| # Autotools (gettext)
        ^po/Makefile\.in\.in$| # Autotools (gettext)
        ^po/Makevars$| # Autotools (gettext)
        ^m4/.*$        # Autotools (no | at the end)
        )''', re.IGNORECASE | re.VERBOSE)
re_permissive = re.compile(r'''(
        ^PERMISSIVE$|
        ^Expat$|
        ^MIT$|
        ^ISC$|
        ^Zlib$|
        ^BSD-2-Clause$|
        ^BSD-3-Clause$|
        ^BSD-4-Clause-UC$|
        ^GFDL-[123]?(?:\.[01])?\+?\s+with\s+(?:autoconf|libtool|bison)\sexception$|
        ^[AL]?GPL-[123]?(?:\.[01])?\+?\s+with\s+(?:autoconf|libtool|bison)\s+exception$
        )''', re.IGNORECASE | re.VERBOSE)
###################################################################
# Check all appearing copyright and license texts
###################################################################
# data[*][0]: license name ID: licenseid
# data[*][1]: file name (bunched, list): files
# data[*][2]: copyright holder info (data=dictionary): copyright_lines
# data[*][3]: license text (original: list of lines): license_lines
###################################################################
def check_all_licenses(files, encoding='utf-8', mode=0, pedantic=False):
    adata = []
    license_cache = {} # (licenseid, licensetext) = license_cache[md5hashkey]
    # fake differences of hash for no license cases
    # without copyright qnd without license
    md5hash = hashlib.md5()
    md5hash.update('__NO_COPYRIGHT_NOR_LICENSE__'.encode())
    md5hashkey0 = md5hash.hexdigest()
    license_cache[md5hashkey0] = ('__NO_COPYRIGHT_NOR_LICENSE__', '')
    # with copyright but without license
    md5hash = hashlib.md5()
    md5hash.update('__NO_LICENSE__'.encode())
    md5hashkey1 = md5hash.hexdigest()
    license_cache[md5hashkey1] = ('__NO_LICENSE__', '')
    # Auto-generated file under the permissive license
    md5hash = hashlib.md5()
    md5hash.update('__AUTO_PERMISSIVE__'.encode())
    md5hashkey2 = md5hash.hexdigest()
    license_cache[md5hashkey2] = ('__AUTO_PERMISSIVE__', '\n Autogenerated files with permissive licenses.')
    if len(files) == 0:
        print('W: check_all_licenses(files) should have files', file=sys.stderr)
    if sys.hexversion >= 0x03030000: # Python 3.3 ...
        print('I: ', file=sys.stderr, end='', flush=True)
    for file in files:
        debmake.debug.debug('Df: check_all_licenses file={}'.format(file), type='f')
        if os.path.isfile(file):
            if sys.hexversion >= 0x03030000: # Python 3.3 ...
                print('.', file=sys.stderr, end='', flush=True)
            (copyright_data, license_lines) = parse_encoded_lines(file, encoding=encoding, pedantic=pedantic)
            if copyright_data == {} and license_lines == []:
                # without copyright and without license
                norm_text = ''
                md5hashkey = md5hashkey0
                copyright_data = {'__NO_COPYRIGHT_NOR_LICENSE__':(9999, 0)}
            elif license_lines == []:
                # with copyright but without license
                norm_text = ''
                md5hashkey = md5hashkey1
            else:
                if copyright_data == {}:
                    copyright_data = {'__NO_COPYRIGHT__ in: {}'.format(file):(9999, 0)}
                norm_text = debmake.lc.normalize(license_lines)
                md5hash = hashlib.md5()
                md5hash.update(norm_text.encode())
                md5hashkey = md5hash.hexdigest()
            if md5hashkey in license_cache.keys():
                (licenseid, licensetext) = license_cache[md5hashkey]
            else:
                (licenseid, licensetext) = debmake.lc.lc(norm_text, license_lines, mode)
                license_cache[md5hashkey] = (licenseid, licensetext)
            # clean up output bundling as __AUTO_PERMISSIVE__
            debmake.debug.debug('Dl: LICENSE_ID orig= {}'.format(licenseid), type='l')
            if not pedantic and re_permissive.search(licenseid) and re_autofiles.search(file):
                md5hashkey = md5hashkey2
                (licenseid, licensetext) = license_cache[md5hashkey]
            elif pedantic:
                debmake.debug.debug('Df: {} is treated as {} since pedantic'.format(file, licenseid), type='f')
            elif re_permissive.search(licenseid):
                debmake.debug.debug('Df: {} skipped since not-pedantic and matching re_autofiles'.format(file), type='f')
            elif re_autofiles.search(file):
                debmake.debug.debug('Df: {} skipped since not-pedantic and matching re_permissive'.format(file), type='f')
            else:
                debmake.debug.debug('Df: {} logically this should not happen for __AUTO_PERMISSIVE__ code: {}'.format(file, md5hashkey), type='f')
            debmake.debug.debug('Dl: LICENSE_ID = {}'.format(licenseid), type='l')
            adata.append((md5hashkey, copyright_data, licenseid, licensetext, file))
            for c in copyright_data.keys():
                debmake.debug.debug('Dc: {}-{}: {}'.format(copyright_data[c][0], copyright_data[c][1], c), type='c')
            for l in license_lines:
                debmake.debug.debug('Dl: {}'.format(l), type='l')
        elif os.path.isdir(file):
            print('W: skip check_all_licenses on directory: {}'.format(file), file=sys.stderr)
        else:
            print('W: skip check_all_licenses on non-existing file: {}'.format(file), file=sys.stderr)
    print('\nI: check_all_licenses completed for {} files.'.format(len(files)), file=sys.stderr)
    return adata

def bunch_all_licenses(adata):
    # group scan result by license
    group_by_license = []
    adata = sorted(adata, key=operator.itemgetter(0)) # sort by md5hashkey
    for k, g in itertools.groupby(adata, operator.itemgetter(0)):
        group_by_license.append(list(g))      # Store group iterator as a list
    # bunch the same license for reporting
    bdata = []
    for data_by_license in group_by_license:
        bunched_files = []
        bunched_copyright_data = {}
        for (md5hashkey, copyright_data, licenseid, licensetext, file) in data_by_license:
            bunched_files.append(file)
            for name, (year_min, year_max) in copyright_data.items():
                if name in bunched_copyright_data.keys():
                    (year_min0, year_max0) = bunched_copyright_data[name]
                    bunched_copyright_data[name] = (min(year_min0, year_min), max(year_max0, year_max))
                else:
                    bunched_copyright_data[name] = (year_min, year_max)
        sortkey = '{0:03} {1:02} {2} {3}'.format(max(0, 1000 - len(bunched_files)), min(99, len(licenseid)), licenseid, md5hashkey)
        bunched_files = sorted(bunched_files)
        copyright_list = []
        for name, (year_min, year_max) in sorted(bunched_copyright_data.items()):
            copyright_list.append((year_min, year_max, name))
        bdata.append((sortkey, bunched_files, sorted(copyright_list), licenseid, licensetext))
        debmake.debug.debug('Dk: sortkey="{}", files={}'.format(sortkey, bunched_files), type='k')
    return bdata

def format_copyright(copyright_list):
    spaces = '           ' # 11 spaces
    if copyright_list:
        copyright_lines = ''
    else:
        copyright_lines = spaces + '\n'
    for (year_min, year_max, name) in copyright_list:
        if year_max == 0: # not found
            copyright_lines += '{}{}\n'.format(spaces, name)
        elif year_min == year_max:
            copyright_lines += '{}{} {}\n'.format(spaces, year_min, name)
        else:
            copyright_lines += '{}{}-{} {}\n'.format(spaces, year_min, year_max, name)
    return copyright_lines

def format_all_licenses(bdata):
    # sort for printer ready order
    group_by_license = []
    bdata = sorted(bdata, key=operator.itemgetter(0)) # sort by sortkey (more files comes early)
    for k, g in itertools.groupby(bdata, operator.itemgetter(0)):
        group_by_license.append(list(g))      # Store group iterator as a list
    cdata = []
    for data_by_sortkey in group_by_license:
        for (sortkey, bunched_files, copyright_list, licenseid, licensetext) in data_by_sortkey:
            copyright_lines = format_copyright(copyright_list)
            cdata.append((licenseid, licensetext, bunched_files, copyright_lines))
    return cdata

def checkdep5(files, mode=0, encoding='utf-8', pedantic=False):
    print('I: check_all_licenses', file=sys.stderr)
    adata = check_all_licenses(files, encoding=encoding, mode=mode, pedantic=pedantic)
    print('I: bunch_all_licenses', file=sys.stderr)
    bdata = bunch_all_licenses(adata)
    print('I: format_all_licenses', file=sys.stderr)
    cdata = format_all_licenses(bdata)
    return cdata


#######################################################################
# Test script
#######################################################################
if __name__ == '__main__':
    utf8=True
    pedantic=False
    # parse command line
    if (sys.argv[1] == '-s'):
        mode = 'selftest'
    elif (sys.argv[1] == '-c'):
        # extract copyright
        mode = "copyright"
        file = sys.argv[2]
    elif (sys.argv[1] == '-t'):
        # extract license text
        mode = "text"
        file = sys.argv[2]
    elif (sys.argv[1] == '-i'):
        # get license ID (mode=-1)
        mode = "id"
        file = sys.argv[2]
    elif (sys.argv[1] == '-a'):
        mode = "adata"
        files = sys.argv[2:]
    elif (sys.argv[1] == '-b'):
        mode = "bdata"
        files = sys.argv[2:]
    else:
        mode = "dep5"
        if sys.argv[1] == '--':
            files = sys.argv[2:]
        else:
            files = sys.argv[1:]
    # main routine
    if mode == 'selftest':
        print ("self-test: checkdep5.py parselines()")
        (copyright_data, license_lines) = parse_lines([
        '#!/bin/sh', \
        '# COPYRIGHT (C) 2015 firstname mid secondname', \
        '# COPYRIGHT (C) 2016 firstname mid secondname ALL RIGHTS RESERVED.', \
        '', \
        '# this is license text 1', \
        '#  this is 2nd line', \
        '', \
        'REAL CODE' ], \
        'filename', True)
        print (" copyright_data: ", end='')
        print (copyright_data)
        print (" license_lines:  ", end='')
        print (license_lines)
        print ("self-test: checkdep5.py analyze_copyright():\n ", end='')
        print(analyze_copyright(["1987-90 firstname mid secondname","firstname mid secondname 2001-16", "1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009  Free Software Foundation, Inc. BOGUS DATA" ], "FILENAME", utf8=True, pedantic=False))
        print ("self-test: checkdep5.py normalize_name():i\n ", end='')
        print(normalize_name('Free Software Foundation, Inc. BOGUS TEXT'))
        print ("self-test: checkdep5.py end of test")
    else:
        if mode == 'copyright' or mode == 'text' or mode == 'id':
            (copyright_data, license_lines) = parse_encoded_lines(file)
            copyright_list = []
            for name, (year_min, year_max) in copyright_data.items():
                copyright_list.append((year_min, year_max, name))
            copyright_lines = format_copyright(sorted(copyright_list))
            if mode == 'copyright':
                print(copyright_lines)
            if mode == 'text':
                print('\n'.join(license_lines))
            if mode == 'id':
                norm_text = debmake.lc.normalize(license_lines)
                (licenseid, license_text) = debmake.lc.lc(norm_text, license_lines, -2)
                print('{}\t{}'.format(file, licenseid))
        elif mode == 'adata':
            # get adata = check_all_licenses(files, encoding=encoding, mode=mode, pedantic=pedantic)
            for (md5hashkey, copyright_data, licenseid, licensetext, file) in check_all_licenses(files, mode=-2):
                copyright_list = []
                for name, (year_min, year_max) in sorted(copyright_data.items()):
                    copyright_list.append((year_min, year_max, name))
                copyright_lines = format_copyright(sorted(copyright_list))
                print('File:      {}'.format(file))
                print('Copyright: {}'.format(copyright_lines[11:]), end='')
                print('MD5:       {}'.format(md5hashkey))
                print('License:   {}{}'.format(licenseid, licensetext))
                print()
        elif mode == 'bdata':
            # get bdata = bunch_all_licenses(adata)
            for (sortkey, bunched_files, sorted_copyright_list, licenseid, licensetext) in \
                    bunch_all_licenses(check_all_licenses(files, mode=-2)):
                copyright_lines = format_copyright(sorted_copyright_list)
                print('Files:     {}'.format('\n           '.join(bunched_files)))
                print('Copyright: {}'.format(copyright_lines[11:]), end='')
                print('Sortkey:   {}'.format(sortkey))
                print('License:   {}{}'.format(licenseid, licensetext))
                print()
        else: # mode == 'dep5':
            # get cdata = sorted, the more bunched files, the earlier it is listed
            for (licenseid, licensetext, files, copyright_lines) in checkdep5(files, mode=-2):
                print('Files:     {}'.format('\n           '.join(sorted(files))))
                print('Copyright: {}'.format(copyright_lines[11:]), end='')
                #print('Sortkey:   {}'.format(sortkey))
                print('License:   {}{}'.format(licenseid, licensetext))
                print()

