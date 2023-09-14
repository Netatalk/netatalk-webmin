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

require './netatalk2-lib.pl';

$path="NoPath";
$s="homes";

$uams_guest = "uams_guest.so";
$uams_clrtxt = "uams_clrtxt.so";
$uams_randnum = "uams_randnum.so";
$uams_dhx = "uams_dhx.so";
$uams_dhx2 = "uams_dhx2.so";
$uams_gss = "uams_gss.so";

&header($text{'create_server_header'},"", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\" target=\"_blank\">$text{help_configs}</a>");
print "<p><p>\n";
print "<form action=server_save_action.cgi>\n";

print "<table width=100% >\n";
print "<tr $tb> <td><b>$text{'edit_server_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td><table>\n";
	print "<tr><td align=right ><b>$text{'create_server_ServerName'}</b></td>\n";
	print "<td colspan=4>";
	print "<input type=radio name=server value=0>\n";
	print "<input size=20 name=servername value=$servername>&nbsp;&nbsp;&nbsp;\n";
	print "<input type=radio checked name=server value=1>$text{'create_server_localhost'}\n";
	print "</td></tr>\n";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_TCP'}</b></td>";
		    print "<td>";
			print "<input type=radio checked name=tcpip value=-tcp>$text{'global_ON'}";
			print "<input type=radio name=tcpip value=-notcp>$text{'global_OFF'}";
			print "</td></tr>";
		print "<tr><td align=right><b>$text{'create_server_AppleTalk'}</b></td>";
		print "<td>";
		print "<input type=radio checked name=ddp value=-ddp>$text{'global_ON'}";
			print "<input type=radio name=ddp value=-noddp>$text{'global_OFF'}";
			print"</td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_uams'}</b></td>";
		    print "<td>";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_guest\">Guest";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_clrtxt\">Cleartext";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_randnum\">Randnum";
			print "<input type=\"checkbox\" name=\"uams\" checked value=\"$uams_dhx\">DHX";
			print "<input type=\"checkbox\" name=\"uams\" checked value=\"$uams_dhx2\">DHX2";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_gss\">Kerberos";
			print "</td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_Address'}</b></td>";
		print "<td><input size=15 maxlength=15 name=address value=></td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_Port'}</b></td>";
		print "<td><input type=\"number\" name=\"port\" min=\"0\" max=\"65535\" value=\"\"></td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_pass'}</b></td>";
		print "<td><input name=setpassword type=radio checked value=-setpassword>$text{'global_ON'}";
			print "<input type=radio name=setpassword value=-nosetpassword>$text{'global_OFF'}";
		print "</td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_setpass'}</b></td>";
		print "<td><input type=radio name=savepassword checked value=-savepassword>$text{'global_ON'}";
			print "<input type=radio name=savepassword value=-nosavepassword>$text{'global_OFF'}";
		print "</td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_lgmesg'}</b></td>";
		print "<td colspan=3><input size=25 maxlength=25 name=logmesg value=\"$loginmesg\"></td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_icon'}</b></td>";
		print "<td><input type=radio checked name=icon value=-icon>$text{'global_ON'}";
			print "<input type=radio name=icon value=-noicon>$text{'global_OFF'}";
		print "</td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_mimicmodel'}</b></td>";
		    print "<td><select name=\"mimicmodel\">";
			print "<option value=>$text{'edit_default'}";
			print "<option value=\"$text{mimicmodel_rackmac}\" %s>$text{mimicmodel_rackmac}";
			print "<option value=\"$text{mimicmodel_powerbook}\" %s>$text{mimicmodel_powerbook}";
			print "<option value=\"$text{mimicmodel_powermac}\" %s>$text{mimicmodel_powermac}";
			print "<option value=\"$text{mimicmodel_macmini}\" %s>$text{mimicmodel_macmini}";
			print "<option value=\"$text{mimicmodel_imac}\" %s>$text{mimicmodel_imac}";
			print "<option value=\"$text{mimicmodel_macbook}\" %s>$text{mimicmodel_macbook}";
			print "<option value=\"$text{mimicmodel_macbookpro}\" %s>$text{mimicmodel_macbookpro}";
			print "<option value=\"$text{mimicmodel_macbookair}\" %s>$text{mimicmodel_macbookair}";
			print "<option value=\"$text{mimicmodel_macpro}\" %s>$text{mimicmodel_macpro}";
			print "<option value=\"$text{mimicmodel_appletv}\" %s>$text{mimicmodel_appletv}";
			print "<option value=\"$text{mimicmodel_airport}\" %s>$text{mimicmodel_airport}";
print "</table> </td></tr></table><p>\n";

print "<table width=100%><br>\n";
print "<tr><td align=left><input type=submit value=$text{'edit_create'}></td>\n";
print "<td align=right><input type=reset value=Reset></td>\n";
print "</tr></table></form><br>\n";
print "<hr>\n";
&footer("servers.cgi",$text{'create_server_return'});
