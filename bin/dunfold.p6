#!/usr/bin/perl6
=begin Description
Debian User Package Repository Toolkit: Recipe Unfolder
Copyright (C) 2019 M. Zhou <lumin@debian.org>
=end Description

constant @SHELL_HEADER =
	"#!/bin/sh\n",
	"set -e\n",
	". /usr/share/duprkit/duprkit\n",
	"export DK_VERBOSE=1\n",
	"\n";

constant @SHELL_TAILER =
	"#--- BEGIN Prepare source and debian/ directory\n",
	"dk_get_source\n",
	"dk_prep_source\n",
	"dk_debianize\n",
	'if ! test -r "$(basename ${0%.sh}).d"; then'~"\n",
	'  ln -sr $src "$(basename ${0%.sh}).d"'~"\n",
	"fi\n",
	"#--- END Prepare source and debian/ directory\n";

sub MAIN (Str $path)
{
	if not $path ~~ /.*.rcp$/ {
		die "Unsupported file $path !";
	}

	my $fp_she := open :w, $path.subst(/\.rcp$/, '.sh');
	my $fp_hft := open :w, $path.subst(/\.rcp$/, '.hft');
	my $status = "she";

	# write shell header
	for @SHELL_HEADER -> $line {
		$fp_she.print: $line;
	}

	for (slurp $path).lines -> $line {
		if $line ~~ /^\^/ { $status = "hft"; }
		given $status {
			when /she/ { $fp_she.say: $line; }
			when /hft/ { $fp_hft.say: $line; }
		}
		#say $status, ": ", $line;
	}

	# write shell tailer
	for @SHELL_TAILER -> $line {
		$fp_she.print: $line;
	}
	
	close $fp_she;
	close $fp_hft;
}
