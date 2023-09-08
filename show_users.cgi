#!/usr/bin/perl
#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Portion of code contributed from somebody-- I can't find the e-mail
#      referencing who it was though. *sigh*
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#

do '../web-lib.pl';

$|=1;

&init_config();

&header($text{users_title}, "", undef(), 1, 1,undef(),"<a href=\"help/configs.cgi\" target=\"_blank\">$text{help_configs}</a>");

&ReadParse();

print "<br><BR>\n";
print "<h3>You click \"Kill\", and they are gone.</h3>";
print "<hr>\n";

if($in{kill}) {
	$in{kill} =~ s/\D//gi;
	if(kill(15,$in{kill})) {
		print "<h4>User disconnected</h4>\n";		
	} else {
		print "<h4>User <blink>NOT</blink> disconnected !</h4>\n";
	}
}

my @users;
for (qx(ps aux)) {
	chomp;
	my @columns = split /\s+/;

	# Pick only lines that are afpd processes not owned by root
	if ($columns[10] =~ m/afpd/ && $columns[0] ne "root") {
		# Columns with index 0 username, 1 PID, and 8 date
		push @users, join(":::", $columns[0], $columns[1], $columns[8]);
	}
}

print "<h4>There are currently " . scalar(@users) . " users connected.</h4>\n";
print "<table border=\"0\" width=\"80%\">\n";
print "<tr $tb><td><b>User</b></td><td><b>Connected Since</b></td><td><b>Kill</b></td></tr>\n";
foreach my $user (sort @users) {
	#username,PID,date
	my @line = split(":::", $user);
	print "<tr $tc><td>$line[0] </td><td>$line[2]</td><td>";
	print "<form action=\"show_users.cgi\"><input type=submit name=kill value=\"Kill $line[1]\"></form>";
	print "</td></tr>\n";
}
print "</table>\n";
print "<br><br>\n";

&footer("index.cgi",$text{'edit_return'});
