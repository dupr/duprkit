# Make you an explicit example on how to convert existing debian pkg to .rcp
%.rcp:
	./deb2rcp.sh $*

# for debugging
install:
	install -Dm0644 vim/syntax/hft.vim \
		/usr/share/vim/vim81/syntax/hft.vim
	install -Dm0644 vim/ftdetect/hft.vim \
		/usr/share/vim/vim81/ftdetect/hft.vim
