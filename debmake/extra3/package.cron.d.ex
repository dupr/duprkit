#
# Regular cron jobs for the @PACKAGE@ package
# See dh_installcron(1) and crontab(5).
#
0 4	* * *	root	[ -x /usr/bin/@PACKAGE@_maintenance ] && /usr/bin/@PACKAGE@_maintenance
