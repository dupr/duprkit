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

