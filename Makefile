DESTDIR       ?=
PREFIX        ?= /usr
BINDIR        ?= $(PREFIX)/bin/
SHAREDIR      ?= $(PREFIX)/share/duprkit/
DOCDIR        ?= $(PREFIX)/share/doc/duprkit/
EXAMPLEDIR    ?= $(DOCDIR)/examples/
VIM           ?= $(PREFIX)/share/vim/

install: install-vim
	install -Dm0755 bin/hft $(DESTDIR)/$(BINDIR)/hft
	install -Dm0755 bin/flink $(DESTDIR)/$(BINDIR)/flink
	install -Dm0755 bin/duprCollector $(DESTDIR)/$(BINDIR)/duprCollector
	install -Dm0644 lib/duprkit $(DESTDIR)/$(SHAREDIR)/duprkit
	install -Dm0644 examples/template.rcp \
		$(DESTDIR)/$(EXAMPLEDIR)/template.rcp

install-vim:
	install -Dm0644 examples/vim/syntax/hft.vim \
		$(DESTDIR)/$(VIM)/addons/syntax/hft.vim
	install -Dm0644 examples/vim/ftdetect/hft.vim \
		$(DESTDIR)/$(VIM)/addons/ftdetect/hft.vim
	install -Dm0644 examples/vim/hft-rcp.yaml \
		$(DESTDIR)/$(VIM)/registry/hft-rcp.yaml

test:
	@echo "[48;5;92mhft-sanity[m"
	python3 bin/hft --version
	python3 bin/hft --help
	@echo "[48;5;92mhft-fold[m"
	./bin/hft -f bin -o bin.hft -v
	@echo "[48;5;92mhft-unfold[m"
	./bin/hft -u bin.hft -d junk -v
	@echo "[48;5;92mdupr-sanity[m"
	./bin/flink help
	@echo "[48;5;92mLIB-TEST[m"
	$(MAKE) -Clib test

fmt:
	for BIN in duprCollector  hft; do \
		yapf3 -i bin/$$BIN; \
	done
