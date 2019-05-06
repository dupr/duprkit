# Insight & Motivation

The absence of a centralized, informal Debian package repository where
trusted users could upload their own packaging scripts has been
long-forgotten. As an inevitable result, many user packaging scripts
exist in the wild, scattered like stars in the sky, with varied
packaging quality. Their existence reflects our users' demand,
especially the experienced ones', that has not been satisfied by the
Debian archive. Such idea about informal packaging repository has been
demonstrated successful by the Archlinux User Repository (AUR). Hence,
it should be valuable to think about it for Debian.

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
the VisualStudio-Code upstream tarball. It costs you enormous amount of
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

# Releated Projects

* [FPM](https://github.com/jordansissel/fpm)

* [checkinstall](http://checkinstall.izto.org/)

* [GameDataPackager](https://wiki.debian.org/Games/GameDataPackager)

* [EasyBuilders](https://github.com/easybuilders)

* [Spack](https://github.com/spack)

* [Homebrew/LinuxBrew](https://github.com/Homebrew/brew)

* [AUR/PKGBUILD]

* [Emerge/ebuild]
