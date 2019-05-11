" Vim syntax file
" Language: Debian User Recipe / HFT File
" Author: M. Zhou <lumin@debian.org>
if exists("b:current_syntax")
	finish
endif

runtime! syntax/yaml.vim
let b:current_syntax = "yaml"

syn case match

syntax region rcpFields matchgroup=rcpFieldsGroup start="^\%(Source\|Version\|Description\|Source-URL\|Section\|Homepage\|Revision\|Maintainer\|License\|Standards-Version\|Build-Depends\|Build-Depends-Indep\|Depends\|Debhelper-Compat\|Debhelper-Buildsystem\|Debhelper-Plugins\|Patches\|Uscan\|Recipe-Prep-Source\|Recipe-Binaries\)" end=':' oneline
highlight rcpFieldsGroup term=bold ctermfg=yellow

syntax region rcpOverrides matchgroup=rcpOverridesGroup start="^override_dh_\%(auto_configure\|auto_test\|auto_install\|strip\|dwz\)" end=':' oneline
highlight rcpOverridesGroup term=bold ctermfg=green

syntax region rcpControlFields matchgroup=rcpControlFieldsGroup start="\%(Architecture\|Multi-Arch\|Depends\|Pre-Depends\|Provides\|Conflicts\|Replaces\|Recommends\|Suggests\)" end=':' oneline
highlight rcpControlFieldsGroup term=bold ctermfg=yellow

syntax region rcpControlFiles matchgroup=rcpControlFilesGroup start="\%(install\|lintian-overrides\|dirs\|docs\|examples\|manpages\|links\)" end=':' oneline
highlight rcpControlFilesGroup term=bold ctermfg=blue

syntax region hftComment oneline start="^\^#" end="$"
highlight hftComment term=bold ctermfg=red

syntax region hftPathMode oneline start="^\^\s*\w\+" end="$"
highlight hftPathMode term=bold ctermbg=green

syntax region hftAppend oneline start="^\^\^\s*\w\+" end="$"
highlight hftAppend term=bold ctermbg=magenta

syntax region hftMarks oneline start="^\^\$" end="$"
highlight hftMarks term=bold ctermbg=yellow
