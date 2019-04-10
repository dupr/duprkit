DESTDIR       ?=
PREFIX        ?= /usr/local
BINDIR        ?= $(PREFIX)/bin/
SHAREDIR      ?= $(PREFIX)/share/duprkit/
DOCDIR        ?= $(PREFIX)/share/doc/duprkit/
EXAMPLEDIR    ?= $(DOCDIR)/examples/

install:
	install -Dm0755 bin/hft $(DESTDIR)/$(BINDIR)/hft
	install -Dm0755 bin/dunfold $(DESTDIR)/$(BINDIR)/dunfold
	install -Dm0755 bin/dupr $(DESTDIR)/$(BINDIR)/dupr
	install -Dm0644 lib/duprkit $(DESTDIR)/$(SHAREDIR)/duprkit
	install -Dm0644 templates/template-default.durpkg $(DESTDIR)/$(EXAMPLEDIR)/template-default.durpkg
	install -Dm0644 templates/template-headonly.durpkg $(DESTDIR)/$(EXAMPLEDIR)/template-headonly.durpkg
	install -Dm0644 templates/template-explicit.durpkg $(DESTDIR)/$(EXAMPLEDIR)/template-explicit.durpkg

fmt:
	yapf3 -i bin/unfold
	yapf3 -i bin/hft
