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
	$(HFT) -v -f ../vim -d junk1.hft
	-$(RM) -rf junk1.hft

hft-unfold:
	@echo "[48;5;92mhft-unfold[m"
	$(HFT) -v -f ../vim -d junk2.hft
	$(HFT) -v -u junk2.hft -d junk/junk
	$(HFT) -v -u junk2.hft -d junk/junk -F
	-$(RM) -rf junk2.hft junk

hft-variable:
	@echo "[48;5;92mhft-variable[m"
	echo "^$$ HFT:UNAME 'uname -r'" >> junk3.hft
	echo "^$$ HFT:UNAME `uname -r`" >> junk3.hft
	$(HFT) -v -u junk3.hft
	-$(RM) junk3.hft

flink-sanity:
	@echo "[48;5;92mflink-sanity[m"
	$(FLINK)

flinkh-sanity:
	@echo "[48;5;92mflinkh-sanity[m"
	$(FLINKH)
