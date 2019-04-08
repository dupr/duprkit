D**ian User Package Repository Toolkit
===

THIS TOOLKIT ONLY FOCUSES ON GETTING SCUTWORK DONE.

D**ian may be pronounced as "Dasteriskian", i.e. "D-asterisk-ian".

# DISCLAIMER

```

Everything included in this repository is totoally unrelated to the Debian
Project, or any OFFICIAL Debian development. Debian Project is not responsible
for any consequence resulted by utilization of the D**ian User Package
Repository Toolkit or any related .durpkg collections or single .durpkg files.
Please Take your own risk utilizing the toolkit, and please review every line
of code before execution.

```

# Usage

* fetch the DUR Default collection `./bin/fetch-collections`.

* install the python script `./bin/unfold` and shell script `./bin/dupr` to your PATH.

* search for your keywords in the collections `./bin/dupr search gotop`.

* change directory to, e.g. `cd ./DefaultCollection/gotop/`.

* build the gotop package, `dupr build gotop.durpkg`.

* The way to install resulting .deb packages is omitted. I assume you know that.

* FYI, the shell script `./bin/fold` can fold any existing debian directory into plain text file.

* FYI, the file format specification of .f822 and .durpkg can be found in `./bin/unfold`.

* FYI, the template/example of .durpkg file is [here](./template.durpkg)

# Contributing

This Toolkit and the [DefaultCollection](https://github.com/dupr/DefaultCollection)
are still experimental projects. If you can fully understand what's going on
here and be willing to participate, please feel free to submit a PR or
request for membership by openning an issue.

# LICENSE

MIT/Expat
