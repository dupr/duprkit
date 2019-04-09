D**ian User Package Repository Toolkit
===

THIS TOOLKIT ONLY FOCUSES ON GETTING SCUTWORK DONE.

D**ian may be pronounced as "Dasteriskian", i.e. "D-asterisk-ian". (Although ugly. [Put your suggestion here.](https://github.com/dupr/duprkit/issues/2))

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

* Repackging upstream pre-built binary tarballs into .deb format.

* Data or pre-trained neural networks with obscure licensing. In this
repository one doesn't need to carefully examine the underlying license.

* Packages with dirty hacks, or targeted on testing the water.

* Packages that are more experimental than Debian/experimental.

* Packages that utilizes SIMD instructions heavily. Due to the hardware
compatibility reason, Debian doesn't distribute pre-built binaries with any
higher ISA baseline than the generic one.  (So this work actually
suppresses and replaces the [SIMDebian project](https://github.com/SIMDebian/SIMDebian)).

# Demo

* fetch the DUR Default collection `./bin/fetch-collections`.

* install the python script `./bin/unfold` and shell script `./bin/dupr` to your PATH.

* search for your keywords in the collections `./bin/dupr search gotop`.

* change directory to, e.g. `cd ./DefaultCollection/gotop/`.

* build the gotop package, `dupr build gotop.durpkg`.

* The way to install resulting .deb packages is omitted. I assume you know that.

* FYI, the shell script `./bin/fold` can fold any existing debian directory into plain text file.

* FYI, the file format specification of .f822 and .durpkg can be found in `./bin/unfold`.

* FYI, 4 templates of .durpkg in different styles are available [here](./templates/)

# Specifications

## Hatless Folded Text (HFT) Specification

See https://github.com/dupr/duprkit/blob/master/bin/hft

## DURPKG Specification

see bin/unfold

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
        app-xyz.durpkg  # This file contains an empty f822 part
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

# LICENSE

MIT/Expat
