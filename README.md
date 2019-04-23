Debian User Recipe Toolkit (Work-In-Progress)
===

[![CircleCI](https://circleci.com/gh/dupr/duprkit.svg?style=svg)](https://circleci.com/gh/dupr/duprkit)

DUPR Toolkit (duprkit) is a set of tools designed for Debian User Package
Repository. Similar to Archlinux User Repository (AUR), DUPR aim to ease
Debian packaging with simplified packaging recipe format, although it
still requires a good knowledge on traditional Debian packaging. DUPR only
distributes packaging recipes and doesn't distrbute any resulting `.deb`
files.

DUPR's packaging recipe is similar to AUR's PKGBUILD, or Gentoo's ebuild.
By utilizing the packaging recipe, the user will download the source tarball
and build it locally.

DUPR Toolkit includes (1) the Hatless Folded Text (HFT) utility, which
works like sort of "plain text tar"; (2) the `.durpkg` unfolder, namely
`dunfold` which separates a `.durpkg` file into a shell script and an
HFT file; (3) The DUPR helper `dupr`, which can build `.deb` packages
with a given `.durpkg`.

Hatless Folded Text (HFT) Specification HFT is an **optional** plain text format which allows to to squash packaging
scripts into a single file.
See https://github.com/dupr/duprkit/blob/master/bin/hft
for the specification.

# DISCLAIMER

Everything included in this repository is totoally unrelated to the Debian
Project, or any OFFICIAL Debian development. Debian Project is not responsible
for any consequence resulted by utilization of the D\*\*ian User Package
Repository Toolkit or any related .durpkg collections or single .durpkg files.
Please Take your own risk utilizing the toolkit, and please review every line
of code before execution.

# Documentations

* [Motivation](./doc/motivation.md)
* [Targeted Software](./doc/targets.md)
* [Usage Instructions](./doc/instructions.md)
* [Debian Packaging Reference](./doc/debpkg.md)
* [Specification: Hatless Folded Text (HFT, .hft)](./bin/hft)
* [Specification: Recipe (.rcp)](./bin/dunfold)
* [Specification: Collection](./doc/collection.md)
* [DUPR General Recommendations](./doc/general-recommendations.rst)
* [FAQ](./doc/faq.md)

# List of Known Collections

* https://github.com/dupr/DefaultCollection

# Contributing

This Toolkit and the [DefaultCollection](https://github.com/dupr/DefaultCollection)
are still experimental projects. If you can fully understand what's going on
here and be willing to participate, please feel free to submit a PR or
request for membership by opening an issue.

# LICENSE

MIT/Expat
