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


test:
	@echo "[48;5;92mhft-sanity[m"
	python3 bin/hft --version
	python3 bin/hft --help
	@echo "[48;5;92mdunfold-sanity[m"
	python3 bin/dunfold --help
	@echo "[48;5;92mdupr-sanity[m"
	./bin/dupr help
	@echo "[48;5;92mhft-fold[m"
	./bin/hft -f debian -o debian.hft -v
	@echo "[48;5;92mhft-unfold[m"
	./bin/hft -u debian.hft -d junk -v
	@echo "[48;5;92mLIB-TEST[m"
	$(MAKE) -Clib test

fmt:
	yapf3 -i bin/unfold
	yapf3 -i bin/hft
