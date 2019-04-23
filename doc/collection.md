# Collection Directory Hierarchy Specification

A collection, stored in a git repository or plain directory, gathers a set
of packaging recipes (namely `.rcp` files). Directory layout is up to the
Collection maintainer. Plus, a debian/ directory should also be acceptable
when HFT format is not prefered.

## Example layout 1: name.rcp

```
A-Certain-Collection/
    library-foo.rcp
    application-bar.rcp
    game-baz.rcp
```

## Example layout 2: name/name.rcp

```
A-Certain-Collection/
    library-foo/
        library-foo.rcp
        library-foo-ubuntu.rcp
        library-foo-avx512.rcp
    app-bar/
        app-bar.rcp
        0000-fix-blah-blah.patch
    app-xyz/
        app-xyz.rcp
        debian/*
```

See https://github.com/dupr/DefaultCollection for a real example in this layout.

## Example layout 3: category/name/name.rcp

```
A-Certain-Collection/
    dev-python/
        foobar/
            foobar.rcp
        abc/
            abc.rcp
    sci-libs/
        foo/
            foo.rcp
```
