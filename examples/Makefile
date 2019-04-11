# Make you an explicit example on how durpkg packages itself.
duprkit.durpkg:
	set -e; test -x ../debian; cd ..;\
		hft -f debian -o examples/duprkit.durpkg.hft;
	cat duprkit.durpkg.header duprkit.durpkg.hft >> duprkit.durpkg
	rm duprkit.durpkg.hft

# Make you an explicit example on how to convert existing debian pkg to .durpkg
%.durpkg:
	apt source $*
	cd $**/; hft -f debian/ -o ../$*.hft
	sed -e "s/@SRC@/$*/g" < _.durpkg.header > $*.durpkg
	cat $*.hft >> $*.durpkg
