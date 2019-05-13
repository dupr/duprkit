DESTDIR       ?=
PREFIX        ?= /usr
BINDIR        ?= $(PREFIX)/bin/
DOCDIR        ?= $(PREFIX)/share/doc/duprkit/
EXAMPLEDIR    ?= $(DOCDIR)/examples/
VIM           ?= $(PREFIX)/share/vim/

all:

install: install-vim install-bin install-examples install-pretrained

install-bin:
	install -Dm0755 bin/hft $(DESTDIR)/$(BINDIR)/hft
	install -Dm0755 bin/flinkH $(DESTDIR)/$(BINDIR)/flinkH
	install -Dm0755 bin/flinkV $(DESTDIR)/$(BINDIR)/flinkV
	install -Dm0755 bin/flinkG $(DESTDIR)/$(BINDIR)/flinkG
	install -Dm0755 bin/flink $(DESTDIR)/$(BINDIR)/flink

install-examples:
	install -Dm0644 examples/template.rcp $(DESTDIR)/$(EXAMPLEDIR)/template.rcp

install-vim:
	install -Dm0644 vim/syntax/hft.vim $(DESTDIR)/$(VIM)/addons/syntax/hft.vim
	install -Dm0644 vim/ftdetect/hft.vim $(DESTDIR)/$(VIM)/addons/ftdetect/hft.vim
	install -Dm0644 vim/hft-rcp.yaml $(DESTDIR)/$(VIM)/registry/hft-rcp.yaml

install-pretrained: license-cls-knn.json
	install -Dm0644 license-cls-knn.json $(DESTDIR)/$(EXAMPLEDIR)/license-cls-knn.json

license-cls-knn.json:
	./bin/flinkV --train ./data/common-licenses --savepath license-cls-knn.json

test:
	$(MAKE) -Ctests

fmt:
	for BIN in flinkH hft; do \
		yapf3 -i bin/$$BIN; \
	done
