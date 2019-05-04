train:
	./licensecheck-ng.py --train data

validate:
	for i in $$(find data -type f); do \
		echo $$i; \
		./licensecheck-ng.py --predict $$i; \
		done;

confusion:
	echo FIXME: outdated
	#./confusion.sh
