#!/usr/bin/perl
# Display a form for creating a new server configuration

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
#

require './netapple-lib.pl';

$path="NoPath";
$s="homes";

&header($text{'create_server_header'},"", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\" target=\"_blank\">$text{help_configs}</a>");
print "<p><p>\n";
print "<form action=server_save_action.cgi>\n";

print "<table width=100% >\n";
print "<tr $tb> <td><b>$text{'create_server_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td><table>\n";
	print "<tr><td align=right ><b>$text{'create_server_ServerName'}</b></td>\n";
	print "<td colspan=4>";
	print "<input type=radio name=server value=0>\n";
	print "<input size=10 name=servername value=>&nbsp;&nbsp;&nbsp;\n";
	print "<input type=radio name=server checked value=1 >&nbsp;&nbsp;&nbsp;<b>$text{'create_server_localhost'}</b>\n";
	print "</td> </tr>\n";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_TCP'}</b></td>";
		print "<td><input type=radio checked name=tcpip value=-tcp>$text{'global_ON'}";
			print "<input type=radio name=tcpip value=-notcp>$text{'global_OFF'}";
			print "</td>";
		print "<td  align=right><b>$text{'create_server_AppleTalk'}</b></td>";
		print "<td ><input type=radio name=ddp checked value=-ddp>$text{'global_ON'}";
			print "<input type=radio name=ddp value=-noddp>$text{'global_OFF'}";
			print "</td>";
	print "</tr>";
	print "<tr >";
		print "<td align=right><b>$text{'create_server_Port'}</b></td>";
		print "<td > <input type=\"number\" min=0 max=65536 name=port value=></td>\n";
		print "<td align=right><b>$text{'create_server_Address'}</b></td>";
		print "<td ><input size=15 maxlength=15 name=address value=></td>";
	print "</tr>";
	print "<tr >";
		print "<td align=right><b>$text{'create_server_pass'}</b></td>";
		print "<td ><input name=setpassword type=radio checked value=-setpassword>$text{'global_ON'}";
			print"<input type=radio name=setpassword value=-nosetpassword>$text{'global_OFF'}";
		print "</td>";
		print "<td align=right><b>$text{'create_server_setpass'}</b></td>";
		print "<td ><input type=radio checked name=savepassword value=-savepassword>$text{'global_ON'}";
			print "<input type=radio name=savepassword value=-nosavepassword>$text{'global_OFF'}";
		print "</td>";
	print "</tr>";
	print "<tr >";
		print "<td align=right><b>$text{'create_server_lgmesg'}</b></td>";
		print "<td colspan=3><input size=25 maxlength=25 name=logmesg value=></td>";
		print "</tr>";
print "</table> </td></tr></table><p>\n";

print "<table width=100%><br>\n";
print "<tr><td align=left><input type=submit value=$text{'edit_create'}></td>\n";
print "<td align=right><input type=reset value=Reset></td>\n";
print "</tr></table></form><br>\n";
print "<hr>\n";
&footer("servers.cgi",$text{'create_server_return'});
