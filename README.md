Debian User Recipe Toolkit (Work-In-Progress; pre-alpha)
===

[![CircleCI](https://circleci.com/gh/dupr/duprkit.svg?style=svg)](https://circleci.com/gh/dupr/duprkit)

DUR Toolkit (durkit) is a set of tools designed for creating and utilizing user
packaging recipe, which aims to simplify the source tree debianization process.
A recipe defines how to get the source package and how to debianize the source
tree, and can be transformed into a `debianized` source tree, `.dsc` files, or
`.deb` files directly, at user's option.  A set of recipe files form a
Collection, namely a Debian User Repository.

This toolkit try to provide an experience resembles AUR's PKGBUILD or Gentoo's
ebuild, although it still requires a good knowledge about traditional Debian
packaging. The following tools are provided by this toolkit:

1. [Hatless Folded Text (HFT) utility](./bin/hft). HFT is in fact sort of
   "plain text tar format", which allows one to squash multiple text files into
   a single file, or restore the multiple files from a single HFT file.

2. [DUPR Main Utility: flink](./bin/flink). The top-level utility used to build `.deb`,
   `.dsc` or debianized source tree from a given recipe file.

# Highlights

TODO

# Documentations

* [Motivation, Targeted Software, and Related Projects](./doc/motivation.md)
* [Usage Instructions and Examples](./doc/instructions.md)
* [FAQ](./doc/faq.md)

# List of Known Collections

* https://github.com/dupr/DefaultCollection

# Contributing

This Toolkit and the [DefaultCollection](https://github.com/dupr/DefaultCollection)
are still experimental projects. If you can fully understand what's going on
here and be willing to participate, please feel free to submit a PR or
request for membership by opening an issue.

# DISCLAIMER

This project is totoally unrelated to  OFFICIAL Debian development.  Debian
Project is not responsible for any consequence incured by utilizing the
toolkit.  Please Take your own risk and please review every line of code before
execution.

# LICENSE

MIT/Expat
