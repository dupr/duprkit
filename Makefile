train:
	./licensecheck-ng.py --train data

test:
	for i in $$(find data -type f); do \
		echo $$i; \
		./licensecheck-ng.py --predict $$i; \
		done;

confusion:
	echo FIXME: outdated
	#./confusion.sh
