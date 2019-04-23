# Make you an explicit example on how durpkg packages itself.
duprkit.rcp:
	set -e; test -x ../debian; cd ..;\
		hft -f debian -o examples/duprkit.durpkg.hft;
	cat duprkit.durpkg.header duprkit.durpkg.hft >> duprkit.durpkg
	rm duprkit.durpkg.hft

# Make you an explicit example on how to convert existing debian pkg to .durpkg
%.rcp:
	./deb2rcp.sh $*

# for debugging
install:
	install -Dm0644 vim/syntax/hft.vim \
		/usr/share/vim/vim81/syntax/hft.vim
	install -Dm0644 vim/ftdetect/hft.vim \
		/usr/share/vim/vim81/ftdetect/hft.vim
