" HFT syntax file
" Author: M. Zhou
if exists("b:current_syntax")
	finish
endif

runtime! syntax/yaml.vim
let b:current_syntax = "yaml"

syntax region hftComment oneline start="^\^#" end="$"
highlight hftComment term=bold ctermfg=red

syntax region hftPathMode oneline start="^\^\s*\w\+" end="$"
highlight hftPathMode term=bold ctermbg=green

syntax region hftAppend oneline start="^\^\^\s*\w\+" end="$"
highlight hftAppend term=bold ctermbg=magenta
