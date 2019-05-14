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

# Projects Related to Packaging

#### [FPM](https://github.com/jordansissel/fpm)

#### [checkinstall](http://checkinstall.izto.org/)

#### [GameDataPackager](https://wiki.debian.org/Games/GameDataPackager)

#### [EasyBuilders](https://github.com/easybuilders)

#### [Spack](https://github.com/spack)

#### [Homebrew/LinuxBrew](https://github.com/Homebrew/brew)

#### [AUR/PKGBUILD]

#### [Emerge/ebuild]

# Projects Related to Debian Packaging

#### dh-make

**Cons:**

1. Upon debian directory initialization, dh-make requires the basename of
the current working directory to be `<package>-<version>`, mandatorily.

2. dh-make's predefined package classes (s: single binary,
i: arch-independent, l: library) limited the flexibility of this tool.

3. dh-make supports controling some details through CLI. However, it doesn't
support many tweaks, and supporting too many tweaks through CLI would
definitely blow up this tool and force users to learn the command line
argument everytime before use.

4. dh-make tweaks the source format to "native" through a command line argument.

5. dh-make has a weird user interface in fully automated mode: `dh_make --email contact@example.com --copyright=bsd --file ../foo.tar.gz`.

**Pros of duprkit:**

1. `flink` doesn't force you to rename your current working directory. `flink
guess` is able to find a version string via different clues, or fallback to
use "0" if no clue was found.

2. Recipe as an YAML file, resembles some mixture of control and rules, doesn't
define any template. It tries to be as flexible as manually written debian/
directory. `flink guess` is able to scan for various clues and propose
different binary package layouts.

3. Recipe, even if it's YAML instead of DEB822, has identical field names
compared to `debian/control`. `flink` doesn't blow up the command line
interface by allowing detail tweaks. One should just edit the recipe that
`flink` will use.

4. By default, if nothing is specified, `flink` will use the `native` source
format to reduce the chance to encounter building trouble. When `Revision` or
`Patches` field is defined in a recipe, `flink` will automatically regard the
source as `quilt` format.

5. duprkit has a better user interface compared to dh-make. `flink guess` will
automatically generate a recipe according to clues from the current working
directory. `flink boldguess` stacks upon `flink guess`, and will directly
generate the `debian/` directory from the guessed recipe.

#### debmake

# Projects Related to flinkV (license detector)

https://wiki.debian.org/CopyrightReviewTools

#### licensecheck

#### scan-copyrights

#### cme

#### licensecheck2dep5

#### license-reconcile

#### debmake

#### decopy

#### license

#### check-all-the-things

#### cargo-lichking

#### python-debian

#### license finder

#### licensed

#### ninka

#### scancode

#### dlt

#### deb-pkg-tools

#### jninka

#### apache-rat

#### fossology

#### OSLCv3

#### scancode-toolkit

The core algorithm is similar to what scancode-toolkit called "match set":
https://github.com/nexB/scancode-toolkit/blob/develop/src/licensedcode/match_set.py
