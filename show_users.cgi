#!/usr/bin/perl
#
# Netatalk Webmin Module
# Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

require 'netatalk3-lib.pl';

ui_print_header(undef, $test{users_title}, "", "configs", 1, 1);

&ReadParse();

print "<br><h4>Click \"Disconnect\" to disconnect a user.</h4><hr>\n";

if ($in{kill}) {
	if (kill('TERM', $in{kill})) {
		print "<h4>User successfully disconnected</h4>\n";
	} else {
		print "<h4>User <blink>NOT</blink> disconnected!</h4>\n";
	}
}

open(USERS, "/bin/ps aucx|");

while (<USERS>) {
    chop;
    next if !/afpd/;
    @_=split;
    next if $_[0] eq "root";
    push(@users, join(":::", $_[0], $_[1], $_[8]));
}
close USERS;

print "<h4>There are currently " . scalar(@users) . " users connected.</h4>\n";
print "<table border=\"0\" width=\"80%\">\n";
print "<tr $tb><td><b>User</b></td><td><b>Connected Since</b></td><td><b>Kill</b></td></tr>\n";
print "<form METHOD=\"POST\"  ENCTYPE=\"application/x-www-form-urlencoded\">";
foreach (sort @users) {
    @_=split ":::";
    print "<tr $tc><td>$_[0] </td><td>$_[2]</td><td><input type=submit name=kill value=\"$_[1]\"></td></tr>\n";
}
print "</form>\n";
print "</table>\n";
print "<br><br>\n";

ui_print_footer("index.cgi", $text{'edit_return'});
