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

# NOTE: 

require './netapple-lib.pl';
require 'netatalk-funcs.pl';

$path="NoPath";
$s="homes";

&header($text{'create_server_header'},"", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\">$text{help_configs}</a>");

print"<p><p>\n";


print "<hr>\n";
print"<p><p>\n";
print "<form action=>\n";

print "<table  width=100% >\n";
print "<tr $tb> <td><b>$text{'create_server_tabelheader'}</b></td></tr>\n";
print "<tr $cb> <td><table >\n";
	print "<tr><td align=right><b>$text{'create_server_ServerName'}</b></td>\n";
	print "<td colspan=4>";
	print "<input  type=radio name=server value=0>\n";
	print "<input size=10 name=servername value=>&nbsp;&nbsp;&nbsp;\n";
	print "<input type=radio name=server value=1 >&nbsp;&nbsp;&nbsp;<b>$text{'create_server_localhost'}</b>\n";
	print "</td> </tr>\n";
	print"<tr>";
		print"<td  align=right><b>TCP/IP</b></td>";
		print"<td colspan=2><input type=radio name=tcpip value=-tcp>ON";
			print"<input type=radio name=tcpip value=-notcp>OFF";
			print"</td>";
	#print" </tr> ";
	#print"<tr>";
		print"<td align=right><b>Apple Talk</b></td>";
		print"<td ><input type=radio name=ddp value=-ddp>ON";
			print"<input type=radio name=ddp value=-noddp>OFF";
			print"</td>";
	print"</tr>";
	print"<tr >";
		print"<td align=right><b>Port</b></td>";
		print"<td colspan=2> <input size=10 name=port value=></td>";
	#print"</tr>";
	#print"<tr >";
		print"<td align=right><b>Address</b></td>";
		print"<td><input size=13 name=adress value=></td>";
	print"</tr>";	
print "</table> </td></tr></table><p>\n";

print "<table  width=100% >\n";
print"<tr>";
print "<td align=left><input type=submit value=$text{'edit_create'}> </td>\n";
print "<td align=right><input type=submit value=delete> </td></form>\n";
print"</tr>";
print"</table>";

print "<hr>\n";
print"<p><p>\n";
&footer("servers.cgi","Servers");
