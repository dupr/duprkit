#!/usr/bin/perl6
=begin Description
Debian User Package Repository Toolkit: Recipe Unfolder
Copyright (C) 2019 M. Zhou <lumin@debian.org>
=end Description
constant $version = '0.0h';

=begin Recipe-Specification
A .rcp file is a concatenation of a shell script and an HFT file.
It defines how to get and prepare the source tree, as well as how to
debianize the source tree.

Recipe Example
--------------

::
    src="foobar"
    ^ debian/compat
    11
    ^ debian/source/format
    3.0 (native)
=end Recipe-Specification

constant @SHELL_HEADER =
	"#!/bin/sh",
	"set -e",
	". /usr/share/duprkit/duprkit",
	"export DK_VERBOSE=1",
	"";

constant @SHELL_TAILER =
	"#--- BEGIN Prepare source and debian/ directory",
	"dk_get_source",
	"dk_prep_source",
	"dk_debianize",
	'if ! test -r "$(basename ${0%.sh}).d"; then',
	'  ln -sr $src "$(basename ${0%.sh}).d"',
	"fi",
	"#--- END Prepare source and debian/ directory";

sub MAIN (Str $PATH)
{
	my $path = IO::Path.new($PATH);
	if not $path.path ~~ /.*.rcp$/ {
		die "Unsupported file $path !";
	}

	my $fp_she := open :w, $path.basename.subst(/\.rcp$/, '.sh');
	my $fp_hft := open :w, $path.basename.subst(/\.rcp$/, '.hft');
	my $status = "she";

	# write shell header
	for @SHELL_HEADER -> $line {
		$fp_she.say: $line;
	}

	for (slurp $path.path).lines -> $line {
		if $line ~~ /^\^/ { $status = "hft"; }
		given $status {
			when /she/ { $fp_she.say: $line; }
			when /hft/ { $fp_hft.say: $line; }
		}
	}

	# write shell tailer
	for @SHELL_TAILER -> $line {
		$fp_she.say: $line;
	}
	
	close $fp_she;
	close $fp_hft;
}
