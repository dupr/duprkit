#!/usr/bin/perl6

sub MAIN () {
  for qx/fdfind --type f/.lines {
    run 'licensecheck', $_;
    run 'flinkV', $_;
  }
}
