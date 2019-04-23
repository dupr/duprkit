DESTDIR       ?=
PREFIX        ?= /usr
BINDIR        ?= $(PREFIX)/bin/
SHAREDIR      ?= $(PREFIX)/share/duprkit/
DOCDIR        ?= $(PREFIX)/share/doc/duprkit/
EXAMPLEDIR    ?= $(DOCDIR)/examples/
VIMADDON      ?= $(PREFIX)/share/vim/addons/
VIM81         ?= $(PREFIX)/share/vim/vim81/

install: install-vim
	install -Dm0755 bin/hft $(DESTDIR)/$(BINDIR)/hft
	install -Dm0755 bin/dunfold $(DESTDIR)/$(BINDIR)/dunfold
	install -Dm0755 bin/dupr $(DESTDIR)/$(BINDIR)/dupr
	install -Dm0755 bin/duprCollector $(DESTDIR)/$(BINDIR)/duprCollector
	install -Dm0644 lib/duprkit $(DESTDIR)/$(SHAREDIR)/duprkit
	install -Dm0644 examples/template.rcp \
		$(DESTDIR)/$(EXAMPLEDIR)/template.rcp

install-vim:
	install -Dm0644 examples/vim/syntax/hft.vim \
		$(DESTDIR)/$(VIM81)/syntax/hft.vim
	install -Dm0644 examples/vim/ftdetect/hft.vim \
		$(DESTDIR)/$(VIM81)/ftdetect/hft.vim

test:
	@echo "[48;5;92mhft-sanity[m"
	python3 bin/hft --version
	python3 bin/hft --help
	@echo "[48;5;92mdunfold-sanity[m"
	python3 bin/dunfold --help
	@echo "[48;5;92mdupr-sanity[m"
	./bin/dupr help
	@echo "[48;5;92mhft-fold[m"
	./bin/hft -f bin -o bin.hft -v
	@echo "[48;5;92mhft-unfold[m"
	./bin/hft -u bin.hft -d junk -v
	@echo "[48;5;92mLIB-TEST[m"
	$(MAKE) -Clib test

fmt:
	for BIN in dunfold duprCollector  hft; do \
		yapf3 -i bin/$$BIN; \
	done
