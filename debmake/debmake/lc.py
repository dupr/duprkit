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
###############################################################################
# The regex of devscripts: licensecheck (version  2.14.1) was referenced.
# 85 characters needed for
#     "the Apache Group for use in the Apache HTTP server project
#      (http://www.apache.org/)"
###############################################################################
LMAX_HEAD = 64*64   # max junk text in chars (head), 64lines*64chars
LMAX_TAIL = 1024*64 # max junk text in chars (tail), 1024lines*64chars
# order rules by specific to generic
list_main = [] # main rule list = [(name, regex, [variable, ...]), ...]
list_sub = []  # substring rule list for debug
###############################################################################
# match disregards all types of quotation marks and &apos;
re_drop = re.compile(r'("|`|‘|’|“|”|&apos;|' + r"')", re.IGNORECASE)
re_connect = re.compile(r'- ', re.IGNORECASE)
def pattern(text, tail=' '):
    text = text.strip()                     # drop head+tail white spaces
    text = re_drop.sub('',text)             # drop quotation marks
    text = ' '.join(text.split())           # normalize white space(s)
    text = re_connect.sub('', text) + tail  # connect hyphened words
    return text                             # pattern normally ends with ' '
###############################################################################
# regular expression (head and tail given as non-greedy match)
rhead0=r'^(?P<head>.{0,' + '{}'.format(LMAX_HEAD) + r'}?)'
rtail0=r'(?P<tail>.{0,'  + '{}'.format(LMAX_TAIL) + r'}?)$'
def regex(reg, rhead=rhead0, rtail=rtail0):
    return re.compile(rhead + reg + rtail, re.IGNORECASE)
###############################################################################
# BSD Exact
###############################################################################
list_sub += ['r_BSD0']
r_BSD0 = pattern(r'''
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    ''')
list_sub += ['r_BSD1']
r_BSD1 = pattern(r'''
    (?:..? )?Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer\.
    ''')
list_sub += ['r_BSD2']
r_BSD2 = pattern(r'''
    (?:..? )?Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/ or other materials provided with the distribution\.
    ''')
list_sub += ['r_BSD3']
r_BSD3 = pattern(r'''
    (?:..? )?All advertising materials mentioning features or use of this
    software must display the following acknowledgement: This product includes
    software developed by .{2,85}\.
    ''')
list_sub += ['r_BSD4']
r_BSD4 = pattern(r'''
    (?:..? )?Neither the name of .{2,85} nor the names of its contributors may
    be used to endorse or promote products derived from this software without
    specific prior written permission\.
    ''')
list_sub += ['r_BSDW']
r_BSDW = pattern(r'''
    THIS SOFTWARE IS PROVIDED BY (?P<name>.{2,85}) AS IS AND ANY EXPRESS OR
    IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
    NO EVENT SHALL .{2,85} BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES \(INCLUDING, BUT NOT LIMITED
    TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION\) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT \(INCLUDING
    NEGLIGENCE OR OTHERWISE\) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE\.
    ''')

### BSD-2-clause
list_main += [('BSD-2-Clause', 'EXACT',
    regex(r_BSD0 + r_BSD1 + r_BSD2 + r_BSDW),
    ['name'])]
### BSD-3-clause
list_main += [('BSD-3-Clause', 'EXACT',
    regex(r_BSD0 + r_BSD1 + r_BSD2 + r_BSD4 + r_BSDW),
    [])]
### BSD-4-clause
list_main += [('BSD-4-Clause', 'EXACT',
    regex(r_BSD0 + r_BSD1 + r_BSD2 + r_BSD3 + r_BSD4 + r_BSDW),
    ['name'])]
###############################################################################
# BSD Generic
###############################################################################
# list 'bsd3' before 'name'
list_sub += ['r_BSD0G']
r_BSD0G = pattern(r'''
    Redistribution and use in source and binary forms, with or without
    modification, are permitted (?:\(subject to the limitations in the
    disclaimer below\) )?provided that the following conditions are met.
    ''')
list_sub += ['r_BSD1G']
r_BSD1G = pattern(r'''
    (?:..? )?Redistributions of source code must retain the (?:above
    )?copyright notice, this list of conditions,? and the following
    disclaimer\.
    ''') # ,? for XFREE86 1.1 and OPENSSL
list_sub += ['r_BSD2G']
r_BSD2G = pattern(r'''
    (?:..? )?Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and(?:/ ?or)? other materials provided with the
    distribution(?:\.|, and in the same place and form as other copyright,
    license and disclaimer information\.)
    ''') # XFree86 1.1 has the last phrase
list_sub += ['r_BSD3G']
r_BSD3G = pattern(r'''
    (?:..? )?All advertising materials mentioning features or use of this
    software must display the following acknowledge?ment. This product includes
    (?:cryptographic )?software (?:developed|written) by .{2,85}(?:\.|\.
    \(http:\/\/www.OpenSSL.org\/\)|The word cryptographic can be left out if
    the rouines from the library being used are not cryptographic
    related.{0,6}\.)
    ''')
    # dropping "e" as variant, Eric Young's SSL
list_sub += ['r_BSD4G']
r_BSD4G = pattern(r'''
    (?:..? |and that )?(?:Except as contained in this notice,)?.{2,85} be used
    (?:to endorse or promote products derived from|in advertising or
    (?:publicity pertaining to distribution of|otherwise to promote the sale,
    use or other dealings in)) (?:this|the) software without (?:specific,?
    )?(?:prior written|written prior) (?:permission|authorization)(?: from
    .{2,85}| of .{2,85})?\.
    ''') # Some XFree86 variant has leading clarification with shall
list_sub += ['r_BSDPG']
r_BSDPG = pattern(r'''
    NO EXPRESS(?:ED)? OR IMPLIED LICENSES TO ANY PARTYS PATENT
    RIGHTS ARE GRANTED BY THIS LICENSE\.
    ''') # BDS-3-Clause-Clear
list_sub += ['r_BSDWG']
r_BSDWG = pattern(r'''
    THIS SOFTWARE IS PROVIDED(?: BY (?P<name>.{2,85}))? AS.IS
    AND ANY EXPRESS(?:ED)? OR IMPLIED (?:WARANTY\.|WARRANTIES, INCLUDING, BUT
    NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL .{2,85} BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES \(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION\) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT \(INCLUDING NEGLIGENCE OR OTHERWISE\) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
    DAMAGE\.)
    ''') # "EXPRESSED" is what XFREE86 1.1 uses. BSD uses "EXPRESS"
### BSD-2-clause
list_main += [('BSD-2-Clause', 'GENERIC',
    regex(r_BSD0G + r_BSD1G + r_BSD2G + r_BSDWG),
    ['name'])]
### BSD-3-clause-Clear
list_main += [('BSD-3-Clause-Clear', 'GENERIC',
    regex(r_BSD0G + r_BSD1G + r_BSD2G + r_BSD4G + r_BSDPG + r_BSDWG),
    ['name'])]
### BSD-3-clause
list_main += [('BSD-3-Clause', 'GENERIC',
    regex(r_BSD0G + r_BSD1G + r_BSD2G + r_BSD4G + r_BSDWG),
    ['name'])]
### BSD-4-clause
list_main += [('BSD-4-Clause', 'GENERIC',
    regex(r_BSD0G + r_BSD1G + r_BSD2G + r_BSD3G + r_BSD4G + r_BSDWG),
    ['name'])]
###############################################################################
# Apache family (BSD0, BSD1, BSD2 are the same one)
###############################################################################
list_sub += ['r_Apache3'] # BSD3 alternative
r_Apache3 = pattern(r'''
    (?:..? )?The end-user documentation included with the redistribution, if
    any, must include the following acknowledgment: This product includes
    software developed by .{2,85}\. Alternately, this acknowledgment
    may appear in the software itself, if and wherever such third-party
    acknowledgments normally appear.
    ''')
list_sub += ['r_Apache4'] # BSD4 alternative
r_Apache4 = pattern(r'''
    (?:..? )?The names? (?P<altname>.{2,85}) must not be used to endorse or promote products
    derived from this software without prior written permission.  For written
    permission, please contact .{2,85}.
    ''')
list_sub += ['r_Apache5'] # trade mark restriction
r_Apache5 = pattern(r'''
    (?:..? )?Products derived from this software may not be called .{3,12},?
    nor may .{3,12} appear in their name. without prior written permission of
    .{2,85}\.
    ''')
list_sub += ['r_Apache6'] # BSD3 alternative
r_Apache6 = pattern(r'''
    (?:..? )?Redistributions of any form whatsoever must retain the following
    acknowledgment: This product includes software developed by .{2,85} for use
    in .{2,85}\.
    ''')
list_sub += ['r_Apache70'] # BSDW alternative
r_Apache70 = pattern(r'''
    THIS SOFTWARE IS PROVIDED BY THE APACHE GROUP AS IS AND ANY EXPRESSED OR
    IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
    NO EVENT SHALL THE APACHE GROUP OR ITS CONTRIBUTORS BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    \(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION\) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT \(INCLUDING NEGLIGENCE OR OTHERWISE\) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
    DAMAGE\.
    ''')
list_sub += ['r_Apache71'] # BSDW alternative
r_Apache71 = pattern(r'''
    THIS SOFTWARE IS PROVIDED AS IS AND ANY EXPRESSED OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
    AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    APACHE SOFTWARE FOUNDATION OR ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    \(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION\) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT \(INCLUDING NEGLIGENCE OR OTHERWISE\) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
    DAMAGE\.
    ''')
### Apache 1.0
list_main += [('Apache-1.0', 'EXACT',
    regex(r_BSD0G + r_BSD1G + r_BSD2G + r_BSD3G + r_Apache4 + r_Apache5 + r_Apache6 + r_Apache70),
    ['altname'])]
### Apache 1.1
list_main += [('Apache-1.1', 'EXACT',
    regex(r_BSD0G + r_BSD1G + r_BSD2G + r_Apache3 + r_Apache4 + r_Apache5 + r_Apache71),
    ['altname'])]
###############################################################################
# OpenSSL
###############################################################################
list_sub += ['r_ssleay']
r_ssleay = pattern(r'''
    (?:..? )?All advertising materials mentioning features or use of this
    software must display the following acknowledgement: This product includes
    cryptographic software written by Eric Young \(eay@cryptsoft.com\) The word
    cryptographic can be left out if the rouines from the library being used
    are not cryptographic related :-\). (?:..? )?If you include any Windows
    specific code \(or a derivative thereof\) from the apps directory
    \(application code\) you must include an acknowledgement: "This product
    includes software written by Tim Hudson \(tjh@cryptsoft.com\)
    ''')
list_main += [('OpenSSL', 'SSLeay',
    regex(r_BSD0G + r_BSD1G + r_BSD2G + r_ssleay + r_BSDWG),
    ['name'])]

list_sub += ['r_openssl']
r_openssl = pattern(r'''
    (?:..? )?Redistributions of any form whatsoever must retain the following
    acknowledgment: This product includes software developed by the OpenSSL
    Project for use in the OpenSSL Toolkit \(http:\/\/www.OpenSSL.org\/\)
    ''')
list_main += [('OpenSSL', 'OpenSSL',
    regex(r_BSD0G + r_BSD1G + r_BSD2G +  r_BSD3G + r_Apache4 + r_Apache5 + r_openssl + r_BSDWG),
    ['altname', 'name'])]
### OpenSSL-like (BSD with Advertizing but not Apache nor OpenSSL)
list_main += [('BSD *** AD-Clause ***', 'GENERIC',
    regex(r_BSD0G + r_BSD1G + r_BSD2G + r_BSD3G + r'.*'),
    [])]
###############################################################################
# MIT=Expat: Exact
###############################################################################
list_sub += ['r_pemission_expat']
r_pemission_expat = pattern(r'''
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files \(the Software\),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:
    ''')
list_sub += ['r_notice_expat']
r_notice_expat = pattern(r'''
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    ''')
list_sub += ['r_disclaimer_expat']
r_disclaimer_expat = pattern(r'''
    THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY
    KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
    NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
    USE OR OTHER DEALINGS IN THE SOFTWARE\.
    ''')
### Expat
list_main += [('Expat', 'Expat-EXACT',
    regex(r_pemission_expat + r_notice_expat + r_disclaimer_expat),
    []), ]
###############################################################################
# MIT: Generic (trained with xorg source data)
###############################################################################
# Expat variants = r_pemission_expat with variants
list_sub += ['r_pemission_expatG']
r_pemission_expatG = pattern(r'''
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files \(the
    (?:Software|Materials)\), to deal in the Software without restriction,
    including without limitation(?: on)? the rights to use, copy, modify,
    (?:merge, )?(?:publish, )?distribute, (?:sub ?license, )?and(?:/ ?or)? sell
    copies of the Software[,.:](?: and to permit persons to whom the Software
    is furnished to do so(?:[,:]|, subject to the following conditions[.:]|,
    provided that))?
    ''')
# Expat variants = r_notice_expat with variants
list_sub += ['r_notice_expatG']
r_notice_expatG = pattern(r'''
    The above copyright notice(?:|s|\(s\)) (including the dates of first
    publication )?and this permission notice (?:shall be included|appear) in
    all copies(?: or substantial portions)?(?: of the Software)?(?: and that
    both the above copyright notice(?:|s|\(s\)) and this permission notice
    appear in supporting documentation)?.
    ''')
# Expat variants = r_notice_expat with variants (requiredisclaimer)
list_sub += ['r_notice_expatGRD']
r_notice_expatGRD = pattern(r'''
    The above copyright notice(?:|s|\(s\)) (including the dates of first
    publication )?and this permission notice \(including the next paragraph\)
    (?:shall be included|appear) in all copies(?: or substantial portions)?(?:
    of the Software)?(?: and that both the above copyright notice(?:|s|\(s\))
    and this permission notice appear in supporting documentation)?.
    ''')
# SGI-B-2.0 (must be before MIT:GENERIC-WITH-NOENDORSE)
list_sub += ['r_notice_sgi']
r_notice_sgi = pattern(r'''
    The above copyright notice including the dates of first publication and
    either this permission notice or a reference to
    http://oss.sgi.com/projects/FreeB/ shall be included in all copies or
    substantial portions of the Software.
    ''')
# Expat variants = r_disclaimer_expat with variants
list_sub += ['r_disclaimer_expatG']
r_disclaimer_expatG = pattern(r'''
    THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY
    KIND, EXPRESS(?:ED)? OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NON-?INFRINGEMENT(?: OF THIRD PARTY RIGHTS)?. IN NO EVENT SHALL .{2,85} BE
    LIABLE FOR ANY CLAIM,(?: OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES,
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS|
    DAMAGES,?(?: INCLUDING, BUT NOT LIMITED TO CONSEQUENTIAL OR INCIDENTAL
    DAMAGES,)? OR OTHER LIABILITY), WHETHER IN AN ACTION OF CONTRACT, (?:TORT
    OR OTHERWISE|NEGLIGENCE OR OTHER TORTIOUS ACTION), ARISING( FROM,)? OUT OF
    OR IN CONNECTION WITH(?: THE SOFTWARE OR)? THE USE OR (?:OTHER DEALINGS IN
    THE|PERFORMANCE OF THIS) SOFTWARE\.
    ''')
# noendorse (=BSD4) is not used in Expat but used in many old MIT licenses
# SGI-B-2.0 (must be before MIT:GENERIC-WITH-NOENDORSE)
list_main += [('SGI-B-2.0', 'WITH-NOENDORSE', regex(r_pemission_expatG +
    r_notice_sgi + r_disclaimer_expatG + r_BSD4G), []), ]
list_main += [('SGI-B-2.0', 'W/O-NOENDORSE', regex(r_pemission_expatG +
    r_notice_sgi + r_disclaimer_expatG), []), ]
# MIT Xorg variants with warranty
list_main += [('MIT', 'GENERIC-WITH-NOENDORSE',
    regex(r_pemission_expatG + r_notice_expatG + r_disclaimer_expatG + r_BSD4G),
    [])]
list_main += [('MIT', 'GENERIC-W/O-NOENDORSE',
    regex(r_pemission_expatG + r_notice_expatG + r_disclaimer_expatG),
    [])]
list_main += [('MIT', 'GENERIC-W/O-NOENDORSE-NOWARRANTY',
    regex(r_pemission_expatG + r_notice_expatG),
    [])]
list_main += [('MIT', 'GENERIC-WITH-NOENDORSE-REQDISCLAIMER',
    regex(r_pemission_expatG + r_notice_expatGRD + r_disclaimer_expatG + r_BSD4G),
    [])]
list_main += [('MIT', 'GENERIC-W/O-NOENDORSE-REQDISCLAIMER',
    regex(r_pemission_expatG + r_notice_expatGRD + r_disclaimer_expatG),
    [])]
###############################################################################
# ISC: Exact
###############################################################################
list_sub += ['r_pemission_isc']
r_pemission_isc = pattern(r'''
    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted,
    ''')
list_sub += ['r_notice_isc']
r_notice_isc = pattern(r'''
    provided that the above copyright notice and this permission notice appear
    in all copies.
    ''')
list_sub += ['r_disclaimer_isc']
r_disclaimer_isc = pattern(r'''
    THE SOFTWARE IS PROVIDED AS IS AND ISC DISCLAIMS ALL
    WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL (?P<name>.{2,85}) BE LIABLE
    FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
    IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
    ''')
### ISC
list_main += [('ISC', 'ISC-EXACT',
    regex(r_pemission_isc + r_notice_isc + r_disclaimer_isc),
    ['name'])]
###############################################################################
# ISC: Generic
###############################################################################
list_sub += ['r_pemission_iscG']
r_pemission_iscG = pattern(r'''
    Permission to use, copy, modify, (:?and(?:/ ?or)? distribute |distribute,
    and(?:/ ?or)? (?:sell|sublicense) )this software (:?and its documentation )?for any
    purpose (:?is hereby granted without fee,|(?:and )?(?:with or )?without fee
    is hereby granted,)
    ''')
list_sub += ['r_notice_iscG']
r_notice_iscG = pattern(r'''
    provided that the above copyright notices?(?: and this permission notice)?
    appear in all copies(:? and that both (?:that|those) copyright notices? and this
    permission notice appear in supporting documentation)?[.,]?
    ''')
list_sub += ['r_disclaimer_iscG']
r_disclaimer_iscG = pattern(r'''
    (?:No trademark license .{2,200} is hereby granted\. .{50,1000} is made\.
    )?(?:.{2,85} MAKES? NO REPRESENTATIONS .{2,80} FOR ANY PURPOSE\.
    )?(?:.{2,85} make(?:|S|\(S\)) (?:no|any) representations?
    about the suitability of this software for any purpose. )?(?:(?:It|THE
    SOFTWARE) is provided as is and )?(?:.{2,85} DISCLAIM(?:|S|\(S\)) ALL
    WARRANTIES WITH REGARD TO THIS SOFTWARE,? INCLUDING ALL IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS[,.] IN NO EVENT SHALL .{2,85} BE LIABLE FOR
    ANY SPECIAL,(?: DIRECT,)? INDIRECT,? OR CONSEQUENTIAL DAMAGES OR ANY
    DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
    AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE\.|(?:It|THE
    SOFTWARE) is provided as is without express or implied warranty\.)
    ''') # First 2 are for Adobe Display PostScript
# ISC variants with no-endorse
list_main += [('ISC', 'ISC-MID-NOENDORSE',
    regex(r_pemission_iscG + r_notice_iscG + r_BSD4G + r_disclaimer_iscG),
    [])]
# ISC variants with no-endorse
list_main += [('ISC', 'ISC-LAST-NOENDORSE',
    regex(r_pemission_iscG + r_notice_iscG + r_notice_expatG + r_disclaimer_expatG + r_BSD4G ),
    [])]
# ISC variants without no-endorse
list_main += [('ISC', 'ISC-W/O-NOENDORSE',
    regex(r_pemission_iscG + r_notice_iscG + r_disclaimer_iscG),
    [])]
###############################################################################
# Zlib: Exact
###############################################################################
list_sub += ['r_disclaimer_zlib']
r_disclaimer_zlib = pattern(r'''
    This software is provided as.is, without any express or
    implied warranty. In no event will the authors be held liable for any
    damages arising from the use of this software.
    ''')
list_sub += ['r_permission_zlib']
r_permission_zlib = pattern(r'''
    Permission is granted to anyone to use this software for any purpose,
    including commercial applications, and to alter it and redistribute it
    freely, subject to the following restrictions[:]
    ''')
list_sub += ['r_notice_zlib']
r_notice_zlib = pattern(r'''
    (?:..? )?The origin of this software must not be misrepresented; you must
    not claim that you wrote the original software. If you use this software in
    a product, an acknowledgment in the product documentation would be
    appreciated but is not required.
    (?:..? )?Altered source versions must be plainly marked as such, and must
    not be misrepresented as being the original software.
    (?:..? )?This notice may not be removed or altered from any source
    distribution.
    ''')
### Zlib
list_main += [('Zlib', 'Zlib-EXACT', regex(r_disclaimer_zlib + r_permission_zlib + r_notice_zlib),
    [])]
###############################################################################
# DEC
###############################################################################
list_sub += ['r_permission_dec']
r_permission_dec = pattern(r'''
    This software is furnished under license and may be used and copied only in
    accordance with the following terms and conditions. Subject to these
    conditions, you may download, copy, install, use, modify and distribute
    this software in source and(?:/ ?or)? binary form. No title or ownership is
    transferred hereby.
    ''')
list_sub += ['r_notice_dec']
r_notice_dec = pattern(r'''
    (?:..? )?Any source code used, modified or distributed must reproduce and
    retain this copyright notice and list of conditions as they appear in the
    source file.
    ''')
list_sub += ['r_noendorse_dec']
r_noendorse_dec = pattern(r'''
    (?:..? )?No right is granted to use any trade name,
    trademark, or logo of .{2,85}. Neither .{2,85} name nor any trademark or
    logo of .{2,85} may be used to endorse or promote products derived from
    this software without the prior written permission of .{2,85}.
    ''')
list_sub += ['r_disclaimer_dec']
r_disclaimer_dec = pattern(r'''
    (?:..? )?This software is provided AS.IS and any express or
    implied warranties, including but not limited to, any implied warranties of
    merchantability, fitness for a particular purpose, or non-infringement are
    disclaimed.  In no event shall .{2,85} be liable for any damages
    whatsoever, and in particular, .{2,85} shall not be liable for special,
    indirect, consequential, or incidental damages or damages for lost profits,
    loss of revenue or loss of use, whether such damages arise in contract,
    negligence, tort, under statute, in equity, at law or otherwise, even if
    advised of the possibility of such damage.
    ''')
# MIT DEC variants with warranty
list_main += [('MIT', 'DEC', regex(r_permission_dec + r_notice_dec + r_noendorse_dec +
    r_disclaimer_dec), []), ]
###############################################################################
# ISC/X11 hybrid with waranty
###############################################################################
list_sub += ['r_BSD3A'] # BSD3 alternative
r_BSD3A = pattern(r'''
    (?:..? )?The end-user documentation included with the redistribution, if
    any, must include the following acknowledgment: This product includes
    software developed by (?P<altname>.{2,85})(?:, in the same place and form as other
    third-party acknowledgments)?\. Alternately, this acknowledgment may appear
    in the software itself, in the same form and location as other such
    third-party acknowledgments.
    ''')
list_main += [('MIT', 'XORG+BSD', regex(r_pemission_expatG + r_BSD1G +r_BSD2G +r_BSD3A
    + r_BSD4G + r_BSDWG ), ['name', 'altname']), ]
###############################################################################
# Mozilla
###############################################################################
r_MPL1 = pattern(r'''
    The contents of this file are subject to the Mozilla Public License Version
    (?P<version>\d+(?:\.\d+)?) \(the License\); you may not use this file
    except in compliance with the License. You may obtain a copy of the License
    at http://www.mozilla.org/MPL/ Software distributed under the License is
    distributed on an AS IS basis, WITHOUT WARRANTY OF ANY KIND, either express
    or implied. See the License for the specific language governing rights and
    limitations under the License.
    ''')
r_MPL2 = pattern(r'''
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. (?P<version>\d+(?:\.\d+)?). If a copy of the MPL was not
    distributed with this file, You can obtain one at
    http://mozilla.org/MPL/(?:\d+(?:\.\d+)?)/. This Source
    Code Form is Incompatible With Secondary Licenses, as defined by the
    Mozilla Public License, v. (?:\d+(?:\.\d+)?).
    ''')
r_MPL3 = pattern(r'''
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. (?P<version>\d+(?:\.\d+)?). If a copy of the MPL was not
    distributed with this file, You can obtain one at
    http://mozilla.org/MPL/(?:\d+(?:\.\d+)?)/.
    ''')
list_main += [('MPL', 'VARIANT1', regex(r_MPL1), ['version'])]
list_main += [('MPL', 'VARIANT2-INCOMPATIBLE', regex(r_MPL2), ['version'])]
list_main += [('MPL', 'VARIANT3', regex(r_MPL3), ['version'])]
###############################################################################
# PERMISSIVE license from GNU releted sources
###############################################################################
# GNU All-Permissive License
r_PM0 = pattern(r'''
    Copying and distribution of this file, with or without modification, are
    permitted in any medium without royalty provided the copyright notice and
    this notice are preserved. This file is offered as.is, without (?:any
    warranty|warranty of any kind).
    ''')
r_PM1 = pattern(r'''
    Copying and distribution of this file, with or without modification, are
    permitted in any medium without royalty provided the copyright notice and
    this notice are preserved.
    ''')
# PERMISSIVE (aclocal.m4, libtool)
r_PM2 = pattern(r'''
    free software. (?:as a special exception )?the (Free Software
    Foundation|author|author\(s\)) gives unlimited permission to copy and(?:/ ?or)?
    distribute it, with or without modifications, as long as this notice is
    preserved. This (program|file) is distributed in the hope
    that it will be useful, but WITHOUT ANY WARRANTY, to the extent permitted
    by law; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
    A PARTICULAR PURPOSE.
    ''')
r_PM3 = pattern(r'''
    free software. (?:as a special exception )?the (Free Software
    Foundation|author|author\(s\)) gives unlimited permission to copy and(?:/ ?or)?
    distribute it, with or without modifications, as long as this notice is
    preserved.
    ''')
r_PM4 = pattern(r'''
    This file (?:may|can) be copied and used freely without restrictions.  It
    (?:may|can) be used in projects which are not available under (?:a GNU|the
    GNU General) Public License,? but which still want to provide support for
    the GNU gettext functionality.
    ''')
r_PM5 = pattern(r'''
    This configure script is free software; the Free Software Foundation gives
    unlimited permission to copy, distribute and modify it.
    ''')
list_main += [('PERMISSIVE', 'VARIANT0-NOWARRANTY', regex(r_PM0), [])]
list_main += [('PERMISSIVE', 'VARIANT1', regex(r_PM1), [])]
list_main += [('PERMISSIVE', 'VARIANT2-NOWARRANTY', regex(r_PM2), [])]
list_main += [('PERMISSIVE', 'VARIANT3', regex(r_PM3), [])]
list_main += [('PERMISSIVE', 'VARIANT4-gettext', regex(r_PM4), [])]
list_main += [('PERMISSIVE', 'VARIANT5', regex(r_PM5), [])]
###############################################################################
# Reference to license name (Generic style)
###############################################################################
# Permission clause
# under the terms of the <GNU General Public License >
list_sub += ['r_under']
r_under = pattern(r'''
    (?:you (?:can|may) redistribute it and(?:/ ?or)? modify .{2,85} under
    |Permission(?: is granted)? to copy, distribute,? and(?:/ ?or)? modify this
        document under
    |Permission(?: is granted)? to use, copy, modify,? (?:merge, )?(?:publish,
        )?distribute,? (?:sublicense,? )and(?:/ ?or)? sell .{2,85} under
    |Permission(?: is granted)? to use, copy, modify,? (?:merge,?
        )?(?:publish,? )?and(?:/ ?or)? distribute .{2,85} under
    |.{2,85} (?:is|are) licensed under
    |distribute under
    |subject to
    |Released under
    |free software .{2,85} under )
    ''', tail='') + r'(?:the (?:terms of the )?)?'
###############################################################################
# GNU version
list_sub += ['r_version1']
r_version1 = pattern(r'''
    (?:(?:as )?published by the Free Software Foundation[,;:.]?
    )?(?:either )?versions?
    (?P<version>\d+(?:\.\d+)?)(?: of the License)?[,.]?(?: \(?only\)?\.?
    | or (?:\(at your option\)? )?(?:any )?(?P<later>later)(?: versions?)?\.?|)
    (?:published by the Free Software Foundation[,;:.]? )?''', tail='')
    # wrong additional "s" is used in some software
    # GNU Free Documentation License, Version 1.1 or any later version published
# XXXXX FIXME XXXXX r_version2 not tested
list_sub += ['r_version2']
r_version2 = pattern(r'''
    (?:either )?versions?
    (?P<version>\d+(?:\.\d+)?)(?: of the License)?(?:\.|
    \(?only\)\.?|,
    or (?:\(at your option\) )?(?:any )?(?P<later>later)(?: versions?)?\.)?
    ''') + r'(?: of the\s)?'
    # wrong additional "s" is used in some software
###############################################################################
list_sub += ['r_LGPL']
r_LGPL = r'(?:GNU (?:Library|Lesser) General Public License|(?:GNU )?LGPL).? '
list_main += [('LGPL', 'VARIANT1', regex(r_under + r_LGPL + r_version1), [
    'version', 'later'])]
list_main += [ ('LGPL', 'VARIANT2', regex(r_under + r_version2 + r_LGPL), [
    'version', 'later'])]
list_main += [('LGPL', 'VARIANT3', regex(r_LGPL + r_version1), [
    'version', 'later'])]

list_sub += ['r_AGPL']
r_AGPL = r'(?:GNU Affero General Public License|(?:GNU )?AGPL).? '
list_main += [('AGPL', 'VARIANT1', regex(r_under + r_AGPL + r_version1), [
    'version', 'later'])]
list_main += [ ('AGPL', 'VARIANT2', regex(r_under + r_version2 + r_AGPL), [
    'version', 'later'])]
list_main += [('AGPL', 'VARIANT3', regex(r_AGPL + r_version1), [
    'version', 'later'])]

list_sub += ['r_GFDL']
r_GFDL = r'(?:GNU Free Documentation License|(?:GNU )?GFDL|GNU FDL).? '
list_main += [ ('GFDL', 'VARIANT1', regex(r_under + r_GFDL + r_version1), [
    'version', 'later'])]
list_main += [ ('GFDL', 'VARIANT2', regex(r_under + r_version2 + r_GFDL), [
    'version', 'later'])]
list_main += [ ('GFDL', 'VARIANT3', regex(r_GFDL + r_version1), [
    'version', 'later'])]

list_sub += ['r_GPL']
r_GPL = r'(?:GNU General Public License|(?:GNU )?GPL).? '
list_main += [ ('GPL', 'VARIANT1', regex(r_under + r_GPL + r_version1), [
    'version', 'later'])]
list_main += [ ('GPL', 'VARIANT2', regex(r_under + r_version2 + r_GPL), [
    'version', 'later'])]
list_main += [ ('GPL', 'VARIANT3', regex(r_GPL + r_version1), [
    'version', 'later'])]

list_sub += ['r_MPL']
r_MPL = r'Mozilla Public License.? '
list_main += [ ('MPL', 'VARIANT1', regex(r_under + r_MPL + r_version1), [
    'version', 'later'])]
list_main += [ ('MPL', 'VARIANT2', regex(r_under + r_version2 + r_MPL), [
    'version', 'later'])]
list_main += [ ('MPL', 'VARIANT3', regex(r_MPL + r_version1), [
    'version', 'later'])]

list_sub += ['r_Artistic']
r_Artistic = r'Artistic License.? '
list_main += [ ('Artistic', 'VARIANT1', regex(r_under + r_Artistic + r_version1),
    ['version', 'later'])]
list_main += [ ('Artistic', 'VARIANT2', regex(r_under + r_version2 + r_Artistic),
    ['version', 'later'])]
list_main += [ ('Artistic', 'VARIANT3', regex(r_Artistic + r_version1),
    ['version', 'later'])]
###############################################################################
# Reference to the package license
###############################################################################
r_SM0 = pattern(r'''
    This file is distributed under the same license as .{5,40}\.
    ''')
list_main += [('_SAME_', 'VARIANT0', regex(r_SM0), [])]
list_sub += ['r_SM0']
r_SM1 = pattern(r'''
    This program and the accompanying materials are licensed and made available
    under the terms and conditions of the Software License Agreement which
    accompanies this distribution.
    ''')
list_main += [('_SAME_ACCOMPANY_', 'VARIANT0', regex(r_SM1), [])]
list_sub += ['r_SM1']
# pre-process removes "All rights reserved."
r_SM2 = pattern(r'''
     This program and the accompanying materials are licensed and made
     available under the terms and conditions of the BSD License which
     accompanies this distribution.  The full text of the license may be found
     at .{2,85} THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN AS IS
     BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS
     OR IMPLIED.
     ''')
list_main += [('BSD_ACCOMPANY', 'VARIANT0', regex(r_SM2), [])]
list_sub += ['r_SM2']
###############################################################################
# Reference to license name (specific style)
###############################################################################
list_main += [
    ('Apache', 'EXTRA', regex(pattern(r'''
        (?:.{2,85} licenses? this file to you|licensed) under the Apache
        License, Version (?P<version>[^ ]+) \(the LICENSE\).
        ''')), ['version']),
    ('QPL', 'EXTRA', regex(pattern(r'''
        (?P<toolkit>This file is part of the .*Qt GUI Toolkit.  This file )?may
        be distributed under the terms of the Q Public License as defined.
        ''')), ['toolkit']),
    ('Perl', 'EXTRA', regex(pattern(r'''
        This program is free software; you can redistribute it and/or modify it
        under the same terms as Perl itself.
        ''')), []),
    ('Beerware', 'EXTRA', regex(r'\(THE BEER-WARE LICENSE\).'
        ), []),
    ('PHP', 'EXTRA', regex(pattern(r'''
        This source file is subject to version (?P<version>[^ ]+) of the PHP
        license.
        ''')), ['version']),
    ('CeCILL', 'EXTRA', regex(pattern(r'''
        under the terms of the CeCILL(?:-(?P<version>[^ ]+))?.
        ''')), ['version']),
    ('SGI-B', 'EXTRA', regex(pattern(r'''
        (?:permitted in|under) the SGI Free Software License B, Version (?P<version>[^ ]+) \(the License\).
        ''')), ['version']),
    ('Public domain', 'EXTRA', regex(pattern(r'''
        is in the public domain.
        ''')), []),
    ('CDDL', 'EXTRA', regex(pattern(r''''
        terms of the Common Development and Distribution License (?:, Version
        (?P<version>[^ ]+)? \(the License\)).
        ''')), ['version']),
    ('Ms-PL', 'EXTRA', regex(pattern(r'''
        Microsoft Permissive License \(Ms-PL\).
        ''')), []),
    ('BSL', 'EXTRA', regex(pattern(r'''
        Distributed under the Boost Software License, Version (?P<version>[^ ]+)\.
        ''')), ['version']),
    ('PSF', 'EXTRA', regex(pattern(r'''
        PYTHON SOFTWARE FOUNDATION LICENSE (VERSION (?P<version>[^ ]+))?.
        ''')), ['version']),
    ('libpng', 'EXTRA', regex(pattern(r'''
        This code is released under the libpng license.
        ''')), []),
    ('APSL', 'EXTRA', regex(pattern(r'''
        subject to the Apple Public
        Source License Version (?P<version>[^ ]+) \(the License\).
        ''')), ['version']),
    ('LPPL', 'EXTRA', regex(pattern(r'''
        (?:under the conditions of the LaTeX Project Public License,
        |under the terms of the LaTeX Project Public License Distributed from
        CTAN archives in directory macros/latex/base/lppl.txt; )either
        version (?P<version>[^ ]+) of (?:this|the) license,? or \(at your
        option\) any later version.
        ''')), ['version']),
    ('W3C', 'EXTRA', regex(pattern(r'''
        distributed under the W3C..? Software License in
        ''')), []), # W3C(R)
    ('WTFPL', 'EXTRA', regex(pattern(r'''
        Do What The Fuck You Want To Public License (?:, Version
        (?P<version>[^, ]+))?.
        ''')), ['version']),
    ('WTFPL', 'EXTRA', regex(pattern(r'''
        (?:License WTFPL|Under (?:the|a) WTFPL).
        ''')), []),
    ('__UNKNOWN__', '', regex(r'.*'), []), # always true
]
###############################################################################
# exceptions
###############################################################################
list_sub += ['r_autoconf1']
r_autoconf1 = pattern(r'''
    As a special exception to the GNU General Public License, if you
    distribute this file as part of a program that contains a
    configuration script generated by Autoconf, you may include it under
    the same distribution terms that you use for the rest of that
    program.(?: This Exception is an additional permission under section 7
    of the GNU General Public License, version 3 \(.?GPLv3.?\).)?''', tail='')
list_sub += ['r_autoconf2']
r_autoconf2 = pattern(r'''
    As a special exception to the GNU General Public License,
    this file may be distributed as part of a program that
    contains a configuration script generated by Autoconf, under
    the same distribution terms as the rest of that program.''', tail='')
list_sub += ['r_autoconf3']
r_autoconf3 = pattern(r'''
    Additional permission under section 7 of the GNU General Public License,
    version 3 \(.?GPLv3.?\): If you convey this file as part of a work that
    contains a configuration script generated by Autoconf, you may do so under
    terms of your choice.''', tail='')
list_sub += ['r_libtool']
r_libtool = pattern(r'''
    As a special exception to the GNU General Public License, if you distribute
    this file as part of a program or library that is built using GNU Libtool,
    you may include this file under the same distribution terms that you use
    for the rest of that program.''', tail='')
list_sub += ['r_bison']
r_bison = pattern(r'''
    As a special exception, you may create a larger work that contains part or
    all of the Bison parser skeleton and distribute that work under terms of
    your choice, so long as that work isn.t itself a parser generator
    using the skeleton or a modified version thereof as a parser skeleton.
    Alternatively, if you modify or redistribute the parser skeleton itself,
    you may \(at your option\) remove this special exception, which will cause
    the skeleton and the resulting Bison output files to be licensed under the
    GNU General Public License without this special exception.''', tail='')
list_sub += ['r_font']
r_font = pattern(r'''
    As a special exception, if you create a document which uses this font, and
    embed this font or unaltered portions of this font into the document, this
    font does not by itself cause the resulting document to be covered by the
    GNU General Public License. This exception does not however invalidate any
    other reasons why the document might be covered by the GNU General Public
    License. If you modify this font, you may extend this exception to your
    version of the font, but you are not obligated to do so. If you do not wish
    to do so, delete this exception statement from your version.''', tail='')
list_sub += ['r_efi1']
r_efi1 = pattern(r'''
    Additional terms: In addition to the forgoing, redistribution and use of
    the code is conditioned upon the FAT 32 File System Driver and all
    derivative works thereof being used for and designed only to read and\/or
    write to a file system that is directly managed by an Extensible Firmware
    Interface \(EFI\) implementation or by an emulator of an EFI
    implementation.''', tail='')
list_sub += ['r_efi2']
r_efi2 = pattern(r'''
    Additional terms: In addition to the forgoing, redistribution and use of
    the code is conditioned upon the FAT 32 File System Driver and all
    derivative works thereof being used for and designed only to read and\/or
    write to a file system that is directly managed by Intel's Extensible
    Firmware Initiative \(EFI\) Specification v. 1.0 and later and/or the
    Unified Extensible Firmware Interface \(UEFI\) Forum's UEFI Specifications
    v.2.0 and later \(together the UEFI Specifications\); only as necessary to
    emulate an implementation of the UEFI Specifications; and to create
    firmware, applications, utilities and\/or drivers.
    ''', tail='')
list_sub += ['r_add']
r_add = pattern(r'''
    Additional terms:
    ''', tail='')
list_sub += ['r_exception']
r_exception = pattern(r'exception', tail='')

list_exceptions = [
    (re.compile(r_autoconf1), 'with autoconf exception', '1'),
    (re.compile(r_autoconf2), 'with autoconf exception', '2'),
    (re.compile(r_autoconf3), 'with autoconf exception', '3'),
    (re.compile(r_libtool), 'with libtool exception', '1'),
    (re.compile(r_bison), 'with bison exception', '1'),
    (re.compile(r_font), 'with font exception', '1'),
    (re.compile(r_efi1), 'with EFI exception', '1'),
    (re.compile(r_efi2), 'with EFI exception', '2'),
    (re.compile(r_add), 'with additional term exception', '1'),
    (re.compile(r_exception), 'with unknown exception', ''),
]
###############################################################################
# attaributes
###############################################################################
r_old_fsf = pattern(r'''
    675\s+Mass\s+Ave|
    59\s+Temple\s+Place|
    51\s+Franklin\s+Steet|
    02139|
    02111-1307
    ''', tail='')
r_dual = pattern(r'''
    Dual\slicen[cs]e
    ''', tail='')

# regex, copyright addtion, license addition
list_attributes = [
    (regex(r_old_fsf), '', 'The FSF address in the above text is the old one.'),
    (regex(r_dual), '*** dual license ***', ''),
]

###############################################################################
# GNU License text
# 300 BYTES:   Most license headers included in the source
# 10000 BYTES: Full license text for GPL like license
# "Definitions": not present in normal license headers
re_FULL = re.compile(r'definition', re.IGNORECASE)
size_FULL = 500
re_LICENSE_HEADER = regex(pattern(r'''
    Standard License Header COPYRIGHT'''),
    rhead=r'^(?P<head>.*?)', rtail='(?P<tail>.*?)$')
re_LICENSE_AFFERO = regex(pattern(r'''
    software over a computer network.*Affero General Public License
    '''),
    rhead=r'^(?P<head>.*?)', rtail='(?P<tail>.*?)$')
re_LICENSE = regex(pattern(r'''
    (?:(?P<agpl>AFFERO GENERAL PUBLIC LICENSE.*)
    |(?P<gfdl>GNU Free Documentation License.*)
    |(?P<lgpl>GNU (?:Library|Lesser) General Public License.*)
    |(?P<gpl>GNU General Public License.*) )version
    (?P<version>\d+(?:\.\d+)?),? o.*later'''),
    rhead=r'^(?P<head>.*?)', rtail='(?P<tail>.*?)$')
###############################################################################
# license name: file name, licence full name
licensefiles = {
    'Apache-2.0'    : ('Apache-2.0','Apache License Version 2.0\n '),
    'Artistic'      : ('Artistic',  '"Artistic License"\n '),
    'BSD-3-Clause'  : ('BSD',       'BSD 3-clause "New" or "Revised"\n License'),
    'GFDL-1.2'      : ('GFDL-1.2',  'GNU Free Documentation License\n Version 1.2'),
    'GFDL-1.2+'     : ('GFDL-1.2',  'GNU Free Documentation License\n Version 1.2'),
    'GFDL-1.3'      : ('GFDL-1.3',  'GNU Free Documentation License\n Version 1.3'),
    'GFDL-1.3+'     : ('GFDL-1.3',  'GNU Free Documentation License\n Version 1.3'),
    'GPL-1.0'       : ('GPL-1',     'GNU General Public License\n Version 1'),
    'GPL-1.0+'      : ('GPL-1',     'GNU General Public License\n Version 1'),
    'GPL-2.0'       : ('GPL-2',     'GNU General Public License\n Version 2'),
    'GPL-2.0+'      : ('GPL-2',     'GNU General Public License\n Version 2'),
    'GPL-3.0'       : ('GPL-3',     'GNU General Public License\n Version 3'),
    'GPL-3.0+'      : ('GPL-3',     'GNU General Public License\n Version 3'),
    'LGPL-2.0'      : ('LGPL-2',    'GNU Library General Public License\n Version 2'),
    'LGPL-2.0+'     : ('LGPL-2',    'GNU Library General Public License\n Version 2'),
    'LGPL-2.1'      : ('LGPL-2.1',  'GNU Lesser General Public License\n Version 2.1'),
    'LGPL-2.1+'     : ('LGPL-2.1',  'GNU Lesser General Public License\n Version 2.1'),
    'LGPL-3.0'      : ('LGPL-3',    'GNU Lesser General Public License\n Version 3'),
    'LGPL-3.0+'     : ('LGPL-3',    'GNU Lesser General Public License\n Version 3')}
#########################################################################################
def normalize(license_lines):
    # normalize license to a single normalized line with single space
    license_data = []
    for line in license_lines:
        line = line.strip()
        license_data.extend(line.split())
    try:
        license_data.remove('') # remove empty words
    except ValueError:
        pass
    return pattern(' '.join(license_data))
#########################################################################################
def lc(norm_text, license_lines, mode):
    # norm_text: normalized license lines to be analized
    # license_lines: original license lines for output
    # mode: license check mode
    # mode = 0: mode for copyright file generation; same as mode == 2 for lc.py
    if mode == 0:
        mode = 2
    # abs(mode) = 1: mode for the license scan (1 line output; -c, -cccc)
    # abs(mode) = 2: mode for the license scan (mode = 1 + license text; -cc, -ccccc)
    # abs(mode) = 3: mode for the license scan (mode = 2 + comments; -ccc, -cccccc)
    # abs(mode) = 4: mode for the license scan (mode = 3 + match text; debug only)
    # abs(mode) = 5: mode for the partial license regex scan (debug only)
    # abs(mode) = 6: mode for the partial license regex scan (debug only)
    # mode < 0: add pattern index id (for -cccc, -ccccc, -cccccc)
    # return: text to be placed after "License: "
    #####################################################################################
    # 1st-line part
    license = '' # License type: GPL, BSD, ...
    id = ''      # "FULL_LICENSE", "EXACT", ...
    idx = ''
    version = '' # 3
    suffix = ''  #
    with_exception = ''     #  ' with ' + ... + ' exception'
    match_text = ''         # mode == 4 5 6 ... used by debug
    set_attribs = set()
    norm_text = norm_text.strip()
    if len(norm_text) == 0:
        license = '__NO_LICENSE_TEXT__'
        text = ''
    elif len(norm_text) > size_FULL and re_FULL.search(norm_text):
        # full license text (very rough guess) ... skip scanning too many regex
        norm_text = norm_text + ' ' # Ensure a tailing space
        la = re_LICENSE_AFFERO.search(norm_text)
        lh = re_LICENSE_HEADER.search(norm_text)
        if la:
            license = 'AGPL'
            version =  '-1.0'
            suffix = '+'
            id = 'FULL_LICENSE'
        elif lh:
            norm_text = lh.group('tail').strip() + ' '
            l = re_LICENSE.search(norm_text)
            if l:
                if l.group('agpl'):
                    license = 'AGPL'
                    version =  l.group('version')
                    id = 'FULL_LICENSE'
                elif l.group('lgpl'):
                    license = 'LGPL'
                    version =  l.group('version')
                    id = 'FULL_LICENSE'
                elif l.group('gfdl'):
                    license = 'GFDL'
                    version =  l.group('version')
                    id = 'FULL_LICENSE'
                elif l.group('gpl'):
                    license = 'GPL'
                    version =  l.group('version')
                    id = 'FULL_LICENSE'
                else:
                    license = '__GPL_LIKE__'
                if (len(version) == 1) and (version in '1234567890'):
                    version = version + '.0'
                if version:
                    version = '-' + version
                    suffix = '+'
            else:
                license = '__GPL_LIKE_HEADER__'
        else:
            license = '__HEADER___'
    #elif len(norm_text) > size_FULL:
        #license = '__TOO_LONG_TYPE1__'
    else:
        # normal license scan
        norm_text = norm_text + ' ' # Ensure a tailing space
        for (license, id, regex, vars) in list_main:
            r0 =regex.search(norm_text)
            if r0:
                match_text = r0.group(0)
                id += '(' + ','.join(vars)
                try:
                    xname = r0.group('name')
                    if not xname:
                        #print("ERROR: P<name> is missing", file=sys.stderr)
                        xname = ''
                    id += ':name=' + xname
                except IndexError:
                    pass
                try:
                    xname = r0.group('altname')
                    if not xname:
                        #print("ERROR: P<altname> is missing", file=sys.stderr)
                        xname = ''
                    id += ':altname=' + xname
                except IndexError:
                    pass
                id += ')'
                for v in vars:
                    try:
                        if v == 'version':
                            if r0.group(v):
                                version = r0.group('version')
                                if (len(version) == 1) and (version in '1234567890'):
                                    version = version + '.0'
                                if version:
                                    version = '-' + version
                        elif v == 'later':
                            if r0.group(v):
                                suffix = '+'
                        elif v == 'name':
                            if r0.group(v):
                                name = r0.group('name')
                                if name[4:11] == 'FREEBSD':
                                    if license == 'BSD-2-Clause':
                                        license = 'BSD-2-Clause-FreeBSD'
                                elif name[4:10] == 'NETBSD':
                                    if license == 'BSD-2-Clause':
                                        license = 'BSD-2-Clause-NETBSD'
                                elif name[4:11] == 'REGENTS':
                                    if license == 'BSD-4-Clause':
                                        license = 'BSD-4-Clause-UC'
                    except IndexError:
                        print('ERROR: {} missing: {} {}'.format(v, license, id), file=sys.stderr)

                # find only first match
                break
        if license == 'MPL' and id == 'VARIANT2-INCOMPATIBLE' and version == '-2.0':
            version = version + '-no-copyleft-exception'
        # exceptions handling
        for (re_ex, text_ex, id_ex) in list_exceptions:
            r2 = re_ex.search(norm_text)
            if r2:
                if mode >= 0:
                    with_exception = ' ' + text_ex
                else:
                    with_exception = ' ' + text_ex + id_ex
                break
        # warn multiple exception
        re_exception = re.compile(r_exception)
        n_exceptions = len(re_exception.findall(norm_text))
        if n_exceptions > 1:
            with_exception += ' *** check multiple exceptions ***'
        # attributs handling
        for (re_at, copy_at, license_at) in list_attributes:
            r2 = re_at.search(norm_text)
            if r2:
                if license_at !='':
                    set_attribs.update({license_at})
                if copy_at != '':
                    with_exception = ' ' + copy_at
        # dual license
        # if re_dual.search(norm_text)
    if mode >= 0:
        licenseid = license + version + suffix + with_exception
    else:
        # minus mode for detailed internal state
        if id =='':
            licenseid = license + version + suffix + ':' + '----' + with_exception
        else:
            licenseid = license + version + suffix + ':' + id  + with_exception
    license_text = ''
    if abs(mode) >= 3: # output comments
            pass
            # license_text += '\n### !!! C: {}'.format('\n### !!! C: '.join(list(set_subtypes)))
    if abs(mode) >= 2: # Skip if simple
        # RFC-822 complian and empty lines replaced with " ."
        for line in license_lines:
            line = line.rstrip()
            if line == '':
                license_text += '\n .'
            else:
                license_text += '\n {}'.format(line)
        for license_at in set_attribs:
            if license_at != '':
                license_text += '\n .\n ' + license_at
        if license + version + suffix in licensefiles.keys():
            (filename, licensename) = licensefiles[license + version + suffix]
            license_text += "\n .\n On Debian systems, the complete text of the " + licensename + \
                " can be found in `/usr/share/common-licenses/{}'.".format(filename)
    if abs(mode) >= 4: # output debug outputs
        if match_text:
            license_text += '\n### !!! M: {}'.format(match_text)
        if norm_text:
            license_text += '\n### !!! T: {}'.format(norm_text)
    return (licenseid, license_text)

#########################################################################################
def lc_sub(norm_text, mode):
    # check license for debug regex pattern
    # license_lines: license lines to be checked (list)
    # mode: license check mode
    # abs(mode) = 5 (single regex match check)
    # abs(mode) = 6 (combination regex match check)
    #####################################################################################
    text = ''
    for subx in list_sub:
        eval_subx = eval(subx)
        r = re.compile(eval_subx, re.IGNORECASE)
        if r.search(norm_text):
            # match with regx
            text += '>>>>>>>> {} -> "{}"\n'.format(subx, r.search(norm_text).group(0))
            if abs(mode) >= 6:
                for suby in list_sub:
                    if subx != suby:
                        try:
                            r = re.compile(eval(subx) + eval(suby), re.IGNORECASE)
                            if r.search(norm_text):
                                # match with combination of subx + suby
                                text += '==== {} + {} => "{}"\n'.format(subx, suby, r.search(norm_text).group(0))
                        except:
                            pass
    return text
#########################################################################################
if __name__ == '__main__':
    import sys
    import os
    mode = 1
    argc = len(sys.argv)
    if argc <= 1:
        print('Syntax: ' + sys.argv[0] + ' [-][123456] file1 file2 ...')
    else:
        if argc == 2:
            files = sys.argv[1:]
        elif argc >= 3:
            try:
                mode = int(sys.argv[1])
            except ValueError:
                files = sys.argv[1:]
            else:
                files = sys.argv[2:]
        for file in files:
            if os.path.isfile(file):
                with open(file, mode='r', encoding='utf-8') as f:
                    license_lines = f.readlines()
                # drop first few lines with special marks
                while(license_lines[0].strip() == ''):
                    del license_lines[0]
                while(license_lines[-1].strip() == ''):
                    del license_lines[-1]
                norm_text = normalize(license_lines)
                if abs(mode) <= 1: # like debmake -c etc.
                    (licenseid, text) = lc(norm_text, license_lines, mode)
                    print('{}\t=> {}'.format(file, licenseid))
                elif abs(mode) <= 4: # like debmake -c etc.
                    print('File:    {}'.format(file))
                    (licenseid, text) = lc(norm_text, license_lines, mode)
                    print('License: {}{}\n'.format(licenseid, text))
                else: # abs(mode> => 5 for sunstring match to debug list_sub regex
                    print('File:    {}'.format(file))
                    print(lc_sub(norm_text, mode))

