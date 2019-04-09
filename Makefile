DESTDIR ?=
PREFIX  ?= /usr/local
BINDIR  ?= $(PREFIX)/bin/

main:
	install -Dm0755 bin/hft $(DESTDIR)/$(BINDIR)/hft
	install -Dm0755 bin/dunfold $(DESTDIR)/$(BINDIR)/dunfold
	install -Dm0755 bin/dupr $(DESTDIR)/$(BINDIR)/dupr

fmt:
	yapf3 -i bin/unfold
	yapf3 -i bin/hft
