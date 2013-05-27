#!/usr/bin/perl
#
# Netatalk Webmin Module
# Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list
# of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOTOC LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

require './netatalk3-lib.pl';
do '../web-lib.pl';

&header($text{users_title}, "", undef(), 1, 1,undef(),"<a href=\"help/configs.cgi\">$text{help_configs}</a>");

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

&footer("index.cgi",$text{'edit_return'});
