#!/usr/bin/perl6
=begin DESCRIPTION
FLINK: Debian User Recipes
=end DESCRIPTION

constant $SH = '/bin/sh';
constant $DUPR_DEFCOLL = "$*HOME/.defcoll";
constant $GIT = '/usr/bin/git';
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

sub MAIN ( Str $ACTION, Str $TARGET = "" )
{
	given $ACTION {
		when 'f' | 'fetch' {
			flink_fetch;
		}
		when 'l' | 'ls' | 'list' {
			die 'listing or searching';
		}
		when 's' | 'split' {
			die 'splitting';
		}
		when 'u' | 'unfold' {
			die 'unfolding';
		}
		when 'c' | 'create' {
			die 'create template';
		}
		when 'm' | 'minimal' {
			die 'create template without comments';
		}
		when 'dsc' {
			die 'dsc';
		}
		when 'deb' {
			die 'deb';
		}
		when 'sb' | 'sbuild' {
			die 'sbuild';
		}
		default {
			die "???"
		}
	}
}
