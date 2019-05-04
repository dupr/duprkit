# Generate template files of MIT license collection
# 1. Place "copyright" file from xorg-common package in the same directory
# 2. Run "make" to check sanity

PWD=$(shell pwd)

TEST_FILE ?= @1_c.txt

PYTHONPATH:=$(shell pwd)/../..
export PYTHONPATH

PATH:=$(shell pwd)/../../debmake:$(PATH)
export PATH

LC_ALL=C.UTF-8
export LC_ALL

all: test

# Please place data from SPDX in src/dspdx/*
spdx:
	for x in dspdx/* ; do \
	y=$$(basename $$x).txt; \
	: > ../$$y ;\
	echo '#%#%#%# This is copyright analyser test data by Osamu Aoki.' >> ../$$y ;\
	echo '#%#%#%# The following lines shall not be considered copyright statement.' >> ../$$y ;\
	echo '#%#%#%# ' >> ../$$y ;\
	cat   $$x >> ../$$y ;\
	done

# Please place external data in src/dpick/*
pick:
	for x in dpick/* ; do \
	y="@$$(basename $$x).txt"; \
	: > ../$$y ;\
	echo '#%#%#%# This is copyright analyser test data by Osamu Aoki.' >> ../$$y ;\
	echo '#%#%#%# The following lines shall not be considered copyright statement.' >> ../$$y ;\
	echo '#%#%#%# ' >> ../$$y ;\
	cat   $$x >> ../$$y ;\
	done

# Please place "copyright" file from xorg-common package" in src/
mit:
	@if [ ! -f copyright ]; then \
	echo "Please place "copyright" file from xorg-common package"; \
	fi
	cd .. ; \
	sed -n -e '1,47p' -e '53,$$p' src/copyright | \
	grep -v "^SGI FREE SOFTWARE LICENSE B" > copyright-clean
	cd ..; src/split copyright-clean
	rm -f ../copyright-clean

test: test-dep5

test-dep5:
	echo $$PATH
	echo $$PYTHONPATH
	cd .. ;\
	: 2> $(PWD)/../.FULL_LICENSE.STDERR; \
	(for x in $$(ls *.txt); do \
	echo "File: $$x " >&2; \
	checkdep5.py $$x 2>> $(PWD)/../.FULL_LICENSE.STDERR; \
	done ) > $(PWD)/../.FULL_LICENSE.LOG
	diff -u $(PWD)/../.FULL_LICENSE.KEEP $(PWD)/../.FULL_LICENSE.LOG > $(PWD)/../.FULL_LICENSE.DIFF
	# If different, above line returns non-zero(=ERROR) and exit
	@echo "=== SUCCESS ==="

test-id:
	echo $$PATH
	echo $$PYTHONPATH
	cd .. ;\
	: 2> $(PWD)/../.LICENSE.STDERR; \
	(for x in $$(ls *.txt); do \
	echo "File: $$x " >&2; \
	checkdep5.py -i $$x 2>> $(PWD)/../.LICENSE.STDERR; \
	done ) > $(PWD)/../.LICENSE.LOG
	diff -u $(PWD)/../.LICENSE.KEEP $(PWD)/../.LICENSE.LOG > $(PWD)/../.LICENSE.DIFF
	# If different, above line returns non-zero(=ERROR) and exit
	@echo "=== SUCCESS ==="

test1:
	echo $$PATH
	echo $$PYTHONPATH
	cd .. ;\
	echo "File: $(TEST_FILE) "; \
	checkdep5.py $(TEST_FILE)
	@echo "=== SUCCESS ==="


clean:
	rm -f $(PWD)/../.LICENSE.LOG $(PWD)/../.LICENSE.DIFF $(PWD)/../.FULL_LICENSE.STDERR

distclean: clean

