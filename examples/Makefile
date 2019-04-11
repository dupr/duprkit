# Make you an explicit example on how durpkg packages itself.
duprkit.durpkg:
	set -e; test -x ../debian; cd ..;\
		hft -f debian -o examples/duprkit.durpkg.hft;
	cat duprkit.durpkg.header duprkit.durpkg.hft >> duprkit.durpkg
	rm duprkit.durpkg.hft

# Make you the default template.
template-default.durpkg:
	true

# Make you an explicit example on how to convert existing debian pkg to .durpkg
%.durpkg:
	apt source $*
	cd $**/; hft -f debian/ -o ../$*.hft
	sed -e "s/@SRC@/$*/g" < _.durpkg.header > $*.durpkg
	cat $*.hft >> $*.durpkg

# for debugging
install:
	install -Dm0644 vim/syntax/hft.vim \
		/usr/share/vim/vim81/syntax/hft.vim
	install -Dm0644 vim/ftdetect/hft.vim \
		/usr/share/vim/vim81/ftdetect/hft.vim
