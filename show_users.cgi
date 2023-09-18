#!/usr/bin/perl
# Show users with an active afpd session
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

require 'netatalk2-lib.pl';

ui_print_header(undef, $text{'users_title'}, "", "configs", 1);

&ReadParse();

print "<br><h4>Click \"Disconnect\" to disconnect a user.</h4><hr>\n";

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
print "<tr $tb><td><b>User</b></td><td><b>Connected Since</b></td><td><b>Disconnect</b></td></tr>\n";
foreach my $user (sort @users) {
	#username,PID,date
	my @line = split(":::", $user);
	print "<tr $tc><td>$line[0] </td><td>$line[2]</td><td>";
	print "<form action=\"show_users.cgi\"><input type=submit name=kill value=\"$line[1]\"></form>";
	print "</td></tr>\n";
}
print "</table>\n";
print "<br><br>\n";

ui_print_footer("index.cgi", $text{'index_module'});
