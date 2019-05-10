HFT=../bin/hft
FLINK=../bin/flink
FLINKH=../bin/flinkH

tests: hft-tests flink-tests flinkh-tests
hft-tests: hft-sanity hft-fold hft-unfold hft-variable
flink-tests: flink-sanity
flinkh-tests: flinkh-sanity

hft-sanity:
	@echo "[48;5;92mhft-sanity[m"
	$(HFT) --help
	$(HFT) --version

hft-fold:
	@echo "[48;5;92mhft-fold[m"
	$(HFT) -v -f ../debian -d junk.hft
	-$(RM) -rf junk.hft

hft-unfold:
	@echo "[48;5;92mhft-unfold[m"
	$(HFT) -v -f ../debian -d junk.hft
	$(HFT) -v -u junk.hft -d junk/junk
	$(HFT) -v -u junk.hft -d junk/junk -F
	-$(RM) -rf junk.hft junk

hft-variable:
	@echo "[48;5;92mhft-variable[m"
	echo "^$$ HFT:UNAME "uname -r"" > junk.hft
	echo "^$$ HFT:UNAME `uname -r`" > junk.hft
	$(HFT) -v -u junk.hft
	-$(RM) junk.hft

flink-sanity:
	@echo "[48;5;92mflink-sanity[m"
	$(FLINK)

flinkh-sanity:
	@echo "[48;5;92mflinkh-sanity[m"
	$(FLINKH)
