Unofficial Debian User Package Repository Toolkit
===

DISCLAINMER: Everything here is totoally unrelated to the Debian Project. Take your own risk using anything here, and please review all the code before execution.

Usage

* fetch the DUR Default collection `./bin/fetch-collections`.

* install the python script `./bin/unfold` and shell script `./bin/dupr` to your PATH.

* search for your keywords in the collections `./bin/dupr search gotop`.

* change directory to, e.g. `cd ./DefaultCollection/gotop/`.

* build the gotop package, `dupr build gotop.durpkg`.

* The way to install resulting .deb packages is omitted. I assume you know that.

* FYI, the shell script `./bin/fold` can fold any existing debian directory into plain text file.

* FYI, the file format specification of .f822 and .durpkg can be found in `./bin/unfold`.
