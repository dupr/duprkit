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

constant $SHELL_HEADER = q :heredoc/END/;
#!/bin/sh
set -e
. /usr/share/duprkit/duprkit
export DK_VERBOSE=1

END

constant $SHELL_TAILER = q :heredoc/END/;
#--- BEGIN Prepare source and debian/ directory
dk_get_source
dk_prep_source
dk_debianize
if ! test -r "$(basename ${0%.sh}).d"; then
  ln -sr $src "$(basename ${0%.sh}).d"
fi
#--- END Prepare source and debian/ directory
END

sub MAIN (Str $PATH where *.IO.f)
{
	$PATH ~~ /.*.rcp$/ || die "Unsupported file $PATH !";

	my $fp_she := open :w, $PATH.IO.basename.subst(/\.rcp$/, '.sh');
	my $fp_hft := open :w, $PATH.IO.basename.subst(/\.rcp$/, '.hft');
	my $fp = $fp_she;

	$fp_she.say: $_ for $SHELL_HEADER.lines;
	for $PATH.IO.lines {
		if m/^\^/ { $fp = $fp_hft; }
		$fp.say: $_;
	}
	$fp_she.say: $_ for $SHELL_TAILER.lines;

	close $fp_she; close $fp_hft;
}
