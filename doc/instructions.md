# Instructions

## HFT

The `HFT` format and `debian/` directory can be bi-directionally transformed
with `bin/hft`.

* Fold a directory of (hatless) plain files: `hft -v -f debian -o debian.hft`

* Unfold an HFT file into the directory: `hft -v -u debian.hft -d destdir`

## Use Existing Recipe

* Install the `.deb` package from the release page, or simply install with `make install`.

* Fetch your favorite recipe collection, or just the default collection e.g. `flink fetch'.

* Find your target `.rcp` file.

* Review the `.rcp` file to make sure it's safe.

* Build .deb packages: `flink deb xxx.rcp`. Or build the .dsc files: `flink dsc
xxx.rcp`. Or simply prepare the debianized source tree: `flink u xxx.rcp`.

## Create New Recipe

* Install `duprkit`, same as above.

* Create a new recipe for package foobar: `flink c foobar`. If you don't need
the comments in the template, use `flink m foobar`.

* Edit `foobar.rcp` until it works well.

* Optionally submit the `.rcp` to your favorite collection.

## Examples

1. Default template, self-documented: https://github.com/dupr/duprkit/blob/master/examples/template.rcp

2. Hello world example, which simply installs a hello world shell script to `/usr/bin/`:
https://github.com/dupr/duprkit/blob/master/examples/hello-world.rcp

3. Recipe for duprkit itself: https://github.com/dupr/duprkit/blob/master/examples/duprkit.rcp

4. A complex example -- `apt-nosync`, which accelerates apt with libeatmydata.
This `.rcp` file is a complete self-contained package (i.e. doesn't require external source):
https://github.com/dupr/duprkit/blob/master/examples/apt-nosync.rcp
