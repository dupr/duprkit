" HFT syntax file
if exists("b:current_syntax")
	finish
endif

runtime! syntax/sh.vim
let b:current_syntax = "sh"


syntax region hftComment oneline start="^\^#" end="$"
highlight hftComment term=bold ctermfg=red

syntax region hftPathMode oneline start="^\^\s*\w\+" end="$"
highlight hftPathMode term=bold ctermbg=green


let s:current_syntax = b:current_syntax
unlet b:current_syntax
syntax include @MAKE syntax/make.vim
syntax region hftEmbMake start="\^.*debian/rules" skip="\^#" end="\^\@=" contains=@MAKE
let b:current_syntax = s:current_syntax

let s:current_syntax = b:current_syntax
unlet b:current_syntax
syntax include @DEBCONTROL syntax/debcontrol.vim
syntax region hftEmbMake start="\^.*debian/control" skip="\^#" end="\^\@=" contains=@DEBCONTROL
let b:current_syntax = s:current_syntax
