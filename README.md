D**ian User Package Repository Toolkit
===

[![CircleCI](https://circleci.com/gh/dupr/duprkit.svg?style=svg)](https://circleci.com/gh/dupr/duprkit)

THIS TOOLKIT ONLY FOCUSES ON GETTING SCUTWORK DONE. EVERYTHING IS VOLATILE.

D**ian may be pronounced as "Dasteriskian", i.e. "D-asterisk-ian". ([propose a better name here](https://github.com/dupr/duprkit/issues/2))

# DISCLAIMER

```
Everything included in this repository is totoally unrelated to the Debian
Project, or any OFFICIAL Debian development. Debian Project is not responsible
for any consequence resulted by utilization of the D**ian User Package
Repository Toolkit or any related .durpkg collections or single .durpkg files.
Please Take your own risk utilizing the toolkit, and please review every line
of code before execution.
```

# Insight & Motivation

```
The absense of a centralized, informal Debian package repository where
trusted users could upload their own packaging scripts has been
long-forgotten. As an inevitable result, many user packaging scripts
exist in the wild, scattered like stars in the sky, with varied
packaging quality. Their existence reflects our users' demand,
especially the experienced ones', that has not been satisfied by the
Debian archive. Such idea about informal packaging repository has been
demonstrated successful by the Archlinux User Repository (AUR). Hence,
it should be valuable to think about it for Debian.
```

# What kind of packages does the project target to?

ANY PACKAGE. However this project is very glad to accept the following special cases:

* Packages that are extremely hard to made compliant to Debian Policy. For
example, bazel the build system of TensorFlow. Or something that doesn't
worth the effort to be made so.

* Dirty but useful non-free blobs, such as nvidia's cuDNN (CUDA Deep
Neural Network) library, that doesn't make sense to be made policy-compliant.

* Packages that doesn't allow (re)distribution. For example, it's illegal
to redistribute the pre-built binaries for the CUDA version of ffmpeg.
However, this problem can be bypassed by only providing the build script.

* Repackging upstream pre-built binary tarballs into .deb format. For example,
the VisualStudio-Code upstream tarball. It costs you enourmous amount of
time and energy to build and put it to the official Debian archive. Why not
just repack and use it?

* Data or pre-trained neural networks with obscure licensing. In this
repository one doesn't need to carefully examine the underlying license.
See [Deep Learning and Free Software](https://lwn.net/Articles/760142/).

* Packages that utilizes SIMD instructions heavily and needs local build for
the optimal performance. For example the reverse dependencies of the Eigen
library. Due to the hardware compatibility reason, Debian doesn't distribute
pre-built binaries with any higher ISA baseline than the generic one.  (So this
work actually suppresses and replaces the [SIMDebian
project](https://github.com/SIMDebian/SIMDebian)).

* Packages with dirty hacks, more experimental than Debian/experimental,
or targeted on testing the water.

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

* Choose a [template](./templates), copy it to somewhere and modify it. Or you
just create `.durpkg` header and a `debian/` directory. **HFT Format is not
mandatory.** The `HFT` format and `debian/` directory can be bi-directionally
transformed with `bin/hft`, e.g. `hft -f debian -o debian.hft` for folding the
texts, `hft -u debian.hft -d .` for unfolding the `HFT` file.

* Make sure `dupr b mypackage.durpkg` works fine.

* Optionally submit the `.durpkg` to your favorite collection.

* The example `.durpkg` for this toolkit can be found in the `examples` directory after `cd examples; make`.

# List of Known Collections

* https://github.com/dupr/DefaultCollection

# Specifications

## Hatless Folded Text (HFT) Specification

See https://github.com/dupr/duprkit/blob/master/bin/hft

## DURPKG Specification

See https://github.com/dupr/duprkit/blob/master/bin/dunfold

## Collection Directory Hierarchy Specification

See https://github.com/dupr/DefaultCollection for a real example.

```
A collection, stored in a git repository or plain directory, gathers only
packaging files, e.g. .durpkg, stored in subdirectories named by the source
name. Plus, no one prevents you from submitting a debian directory.

For example:

A-Certain-Collection/
    library-foo/
        library-foo.durpkg
        library-foo-ubuntu.durpkg
        library-foo-avx512.durpkg
    app-bar/
        app-bar.durpkg
        0000-fix-blah-blah.patch
    app-xyz/
        app-xyz.durpkg
        debian/*
```

# Contributing

This Toolkit and the [DefaultCollection](https://github.com/dupr/DefaultCollection)
are still experimental projects. If you can fully understand what's going on
here and be willing to participate, please feel free to submit a PR or
request for membership by openning an issue.

# FAQ

* Why is this project hosted on GitHub instead of Debian's Salsa server?

Only 1000~2000 people on this earth have salsa account. More than a million
people have their Github accounts. Hosting this project on github makes access
and contributing easy.

* I think the HFT format is totally rubbish.

Don't use it if you don't like it, HFT is not mandatory. Please carefully
read the templates.

* Where can I submit my `.durpkg` file?

Submit a PR to https://github.com/dupr/DefaultCollection . Or setup your own collection.

* Why is "D\*\*ian" ?

This implementation and packaging recipes are ugly, and non-DFSG stuff are
allowed here. Some people think such creation taints the name of Debian.
[propose a better name here](https://github.com/dupr/duprkit/issues/2)

# LICENSE

MIT/Expat
