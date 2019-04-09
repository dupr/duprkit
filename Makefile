DESTDIR ?=
PREFIX  ?= /usr/local
BINDIR  ?= $(PREFIX)/bin/
SHAREDIR ?= $(PREFIX)/share/duprkit/

install:
	install -Dm0755 bin/hft $(DESTDIR)/$(BINDIR)/hft
	install -Dm0755 bin/dunfold $(DESTDIR)/$(BINDIR)/dunfold
	install -Dm0755 bin/dupr $(DESTDIR)/$(BINDIR)/dupr
	install -Dm0644 lib/duprkit $(DESTDIR)/$(SHAREDIR)/duprkit

fmt:
	yapf3 -i bin/unfold
	yapf3 -i bin/hft
