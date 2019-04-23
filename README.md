Debian User Recipe Toolkit (Work-In-Progress)
===

[![CircleCI](https://circleci.com/gh/dupr/duprkit.svg?style=svg)](https://circleci.com/gh/dupr/duprkit)

DUR Toolkit (durkit) is a set of tools designed for creating and utilizing user
packaging recipe, which aims to simplify the source tree debianization process.
A recipe can be transformed into a `debianized` source tree, `.dsc` files, or
`.deb` files directly, at your option.  A set of recipe files form a
Collection, namely a Debian User Repository.

This toolkit try to provide an experience resembles AUR's PKGBUILD or Gentoo's
ebuild, although it still requires a good knowledge about traditional Debian
packaging. The following tools are provided by this toolkit:

1. [Hatless Folded Text (HFT) utility](./bin/hft). HFT is in fact sort of
   "plain text tar format", which allows one to squash multiple text files into
   a single file, or restore the multiple files from a single HFT file.

2. [Recipe Unfolding Utility](./bin/dunfold). It splits a recipe into a shell
   script and an HFT file.

3. [DUPR Utility](./bin/dupr). The top-level utility used to build `.deb`,
   `.dsc` or debianized source tree from a given recipe file.

# DISCLAIMER

This project is totoally unrelated to  OFFICIAL Debian development.  Debian
Project is not responsible for any consequence incured by utilizing the
toolkit.  Please Take your own risk and please review every line of code before
execution.

# Documentations

* [Motivation](./doc/motivation.md)
* [Targeted Software](./doc/targets.md)
* [Usage Instructions](./doc/instructions.md)
* [Examples and Templates](./examples)
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
