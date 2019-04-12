" HFT syntax file
if exists("b:current_syntax")
	finish
endif

runtime! syntax/sh.vim

syn match hftComment "^\^#.*$"
highlight hftComment term=bold ctermfg=red

syn match hftPathMode "^\^\s*\w\+.*$"
highlight hftPathMode term=bold ctermbg=green
