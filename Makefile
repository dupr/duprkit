train:
	./licensecheck-ng.py --train data

test:
	for i in $$(find data); do \
		echo $$i; \
		./licensecheck-ng.py --predict $$i; \
		done;
