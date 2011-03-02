#!/usr/bin/perl
# edit_fshare.cgi
# Display a form for creating a new file share
#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Some code (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
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

require './netapple-lib.pl';
require 'netatalk-funcs.pl';

&header($text{'misc_options_header'},"", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\">$text{help_configs}</a>");

print"<p><p>\n";


print "<hr>\n";
print"<p><p>\n";
print "<form action=settings.cgi>\n";

print "<table  width=100% >\n";
print "<tr $tb> <td><b>$text{'misc_options_header'}</b></td></tr>\n";
print "<tr $cb> <td><table >\n";
	print "<tr><td width=30% align=left><b>$text{'index_max_users'}<br>$text{'index_max_users_2'}</b></td>\n";
	print "<td>";
		@users = getMaxUser();
		$maxUsers=$config{'select_maxUsers'};
		print"<select align=left  name=maxClients>n";
		for($s=1;$s<=$maxUsers;$s++){
		        printf "<option   value=$s %s> $s\n",
					@users[0] eq $s ? "selected" : "";
		}
		print"</select></td>\n";
	print "</td> </tr>\n";	
print "</table> </td></tr></table><p>\n";
print "<input type=submit value=$text{'edit_Save'}></form>\n";


print "<hr>\n";
print"<p><p>\n";
&footer("","$text{'edit_return'}");
