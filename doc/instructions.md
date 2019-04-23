# Instructions

### Use Existing Recipe

* Install with `make install`. Or simply copy `/bin/*` to your `$PATH`.

* Fetch your favorite recipe collection to any directory, e.g. `git clone https://github.com/dupr/DefaultCollection'.

* Browse or search in the collection, find your target `.durpkg` file.

* Review the .durpkg file to make sure it's safe.

* Start the build: `dupr build foobar.durpkg` or `dupr b foobar.durpkg`.

* The way to install resulting .deb packages is omitted. I assume you know that.

### Create New Recipe

* Install, same as above.

* Copy the [default template](./examples/template-default.durpkg) to somewhere
and modify it. Or just create a `.durpkg` header and a `debian/` directory.
**HFT Format is not mandatory.** The `HFT` format and `debian/` directory can
be bi-directionally transformed with `bin/hft`, e.g. `hft -f debian -o
debian.hft` for folding the texts, `hft -u debian.hft -d .` for unfolding the
`HFT` file.

* Make sure `dupr b mypackage.durpkg` works fine.

* Optionally submit the `.durpkg` to your favorite collection.

* The example `.durpkg` for this toolkit can be found in the `examples` directory after `cd examples; make`.
