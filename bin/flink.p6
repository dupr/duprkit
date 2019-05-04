#!/usr/bin/perl6
=begin DESCRIPTION
FLINK: Debian User Recipes
Copyright (C) 2019 M. Zhou <lumin@debian.org>
=end DESCRIPTION
# FIXME To be merged into flink
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

constant $SHELL_HEADER = q :to/END/;
#!/bin/sh
set -e
. /usr/share/duprkit/duprkit
export DK_VERBOSE=1

END

constant $SHELL_TAILER = q :to/END/;
#--- BEGIN Prepare source and debian/ directory
dk_get_source
dk_prep_source
dk_debianize
if ! test -r "$(basename ${0%.sh}).d"; then
  ln -sr $src "$(basename ${0%.sh}).d"
fi
#--- END Prepare source and debian/ directory
END

constant $SH = '/bin/sh';
constant $DUPR_DEFCOLL = "$*HOME/.defcoll";
constant $COLLECTOR = '/usr/bin/duprCollector';
constant $GIT = '/usr/bin/git';
constant $TEMPLATE = '/usr/share/doc/duprkit/examples/template.rcp';
constant $_C162 = "\x1b[1;38;5;162m";
constant $_C36  = "\x1b[1;36m";
constant $_c    = "\x1b[0m";

sub flink_fetch () {
	if $DUPR_DEFCOLL.IO.d {
		say "{$_C162}→ Cloning {$_C36}DefaultCollection{$_C162} ...{$_c}";
		chdir $DUPR_DEFCOLL;
		run $GIT, 'pull';
	} else {
		say "{$_C162}→ Pulling {$_C36}DefaultCollection{$_C162} ...{$_c}";
		run $GIT, 'clone', 'https://github.com/dupr/DefaultCollection',  $DUPR_DEFCOLL;
	}
}

sub flink_split (Str $PATH)
{
	$PATH.IO.f || die "Non-existent file [$PATH]!" ;
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

sub flink_unfold (Str $PATH)
{
	print "{$_C162}→ Unfolding {$_C36} $PATH {$_C162}into";
    say "{$_C36}.sh {$_C162}and {$_C36}.hft {$_C162}...{$_c}";
	flink_split $PATH;
	my $shell_file = $PATH.IO.basename.subst(/\.rcp$/, '.sh');
	my $hft_file = $PATH.IO.basename.subst(/\.rcp$/, '.hft');
	say "{$_C162}→ Executing {$_C36}{$shell_file} {$_C162}...{$_c}";
	run $SH, $shell_file;
	$shell_file.IO.unlink; $hft_file.IO.unlink;
}

sub flink_create (Str $NAME)
{
	run 'cp','-v', $TEMPLATE, $NAME ~ '.rcp';
}

sub flink_minimal (Str $NAME)
{
	my $fp = open :w, $NAME ~ '.rcp';
	for $TEMPLATE.IO.lines {
		if !m/^\^\#/ && !m/^\s*\#/ || m/^\#\!/ {
			$fp.say: $_;
		} #else { .say }
	}
}

sub flink_deb (Str $PATH)
{
	flink_unfold $PATH;
	my $workdir = $PATH.IO.basename.subst(/\.rcp$/, '.d');
	chdir $workdir;
	run 'dpkg-buildpackage', '-us', '-uc';
}

sub flink_dsc (Str $PATH)
{
	flink_unfold $PATH;
	my $workdir = $PATH.IO.basename.subst(/\.rcp$/, '.d');
	chdir $workdir;
	run 'dpkg-buildpackage', '-us', '-uc', '-nc', '-S';
}

sub flink_sbuild (Str $PATH)
{
	flink_unfold $PATH;
	my $workdir = $PATH.IO.basename.subst(/\.rcp$/, '.d');
	chdir $workdir;
	run 'sbuild', '--no-clean-source';
}

sub MAIN ( Str $ACTION, Str $TARGET = "" )
{
	given $ACTION {
		when 'f' | 'fetch' {
			flink_fetch;
		}
		when 'l' | 'ls' | 'list' {
			if $TARGET.chars {
				run $COLLECTOR, '-s', $TARGET, $DUPR_DEFCOLL;
			} else {
				run $COLLECTOR, $DUPR_DEFCOLL;
			}
		}
		when 's' | 'split' {
			flink_split $TARGET;
		}
		when 'u' | 'unfold' {
			flink_unfold $TARGET;
		}
		when 'c' | 'create' {
			flink_create $TARGET;
		}
		when 'm' | 'minimal' {
			flink_minimal $TARGET;
		}
		when 'dsc' {
			flink_dsc $TARGET;
		}
		when 'deb' {
			flink_deb $TARGET;
		}
		when 'sb' | 'sbuild' {
			flink_sbuild $TARGET;
		}
		default {
			die "???"
		}
	}
}
