Debian User Recipe Toolkit (WIP)
===

[![CircleCI](https://circleci.com/gh/dupr/duprkit.svg?style=svg)](https://circleci.com/gh/dupr/duprkit)

**Everything on the master branch is broken due to the ongoing redesign.
Use the latest release if you want try out the old design.**

DUPR Toolkit (duprkit) provides a set of tools for creating and utilizing user
packaging recipe, aiming at reducing the source tree debianization workload.
A recipe can be directly translated into a `debian/` directory, and helper
utilities are provided to directly build `.deb` or `.dsc` from a recipe file.

# Highlights

* Recipe is a light-weight DSL (Domain Specific Language) combining YAML and HFT.

* More.

# Documentations

* [Motivation, Targeted Software, and Related Projects](./doc/motivation.md)
* [Usage Instructions, Examples, FAQ](./doc/instructions.md)

# List of Known Collections

* Miscellaneous: https://github.com/dupr/DefaultCollection
* Source-based Recipe: https://github.com/dupr/DefaultCookbook
* Binary-based Recipe: https://github.com/dupr/DefaultRepacks
* Pure-Trick Recipe: https://github.com/dupr/DefaultTricks

# Contributing

This Toolkit is still a highly experimental project.
If you can fully understand what's going on here and be willing to participate,
please feel free to submit a PR or request for membership by opening an issue.

# DISCLAIMER

This project is unrelated to OFFICIAL Debian development.  Debian Project is
not responsible for any consequence incured by utilizing the toolkit.  Please
take your own risk and review every line of code before execution.

# LICENSE

MIT/Expat
