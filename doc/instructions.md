# Instructions / Usage Guides

DUPR toolkit introduces two new concepts: HFT and Recipe. It's recommended
to grasp them before starting to use this toolkit.

## Hatless Folded Text (HFT, .hft)

The `HFT` format and `debian/` directory can be bi-directionally transformed
with `bin/hft`.

* Fold a directory of (hatless) plain files: `hft -v -f debian -o debian.hft`

* Unfold an HFT file into the directory: `hft -v -u debian.hft -d destdir`

Full description on HFT can be found here: https://github.com/dupr/duprkit/blob/master/bin/hft

## Recipe (.rcp)

Full description on Recipe can be found here: https://github.com/dupr/duprkit/blob/master/bin/flink

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

# Recipe Collection

A collection, stored in a git repository or plain directory, gathers a set
of packaging recipes (namely `.rcp` files). Directory layout is up to the
Collection maintainer. Plus, a debian/ directory should also be acceptable
when HFT format is not prefered.

## Example layout 1: name.rcp

```
A-Certain-Collection/
    library-foo.rcp
    application-bar.rcp
    game-baz.rcp
```

## Example layout 2: name/name.rcp

```
A-Certain-Collection/
    library-foo/
        library-foo.rcp
        library-foo-ubuntu.rcp
        library-foo-avx512.rcp
    app-bar/
        app-bar.rcp
        0000-fix-blah-blah.patch
    app-xyz/
        app-xyz.rcp
        debian/*
```

See https://github.com/dupr/DefaultCollection for a real example in this layout.

## Example layout 3: category/name/name.rcp

```
A-Certain-Collection/
    dev-python/
        foobar/
            foobar.rcp
        abc/
            abc.rcp
    sci-libs/
        foo/
            foo.rcp
```

## General Recommendations for DUPR Packages/Collections

1. It's not encouraged to distrbute the resulting '.deb' files.
   The design of .rcp is to allow user download source tarball and compile
   the software locally. Similar to AUR's PKGBUILD or Gentoo's ebuild.

## External References

1. YAML Quick Tutorial: https://learnxinyminutes.com/docs/yaml/

List of Debian Packaging Documentations:

* https://www.debian.org/doc/devel-manuals#devref
* https://www.debian.org/doc/devel-manuals#debmake-doc
* https://www.debian.org/doc/devel-manuals#maint-guide
* https://www.debian.org/doc/devel-manuals#packaging-tutorial
