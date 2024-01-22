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

require 'netatalk2-lib.pl';

ui_print_header(undef, $text{'create_server_header'}, "", "servers", 1);

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
	print "<tr>\n";
	print "<td align=right><b>$text{'create_server_ServerName'}</b></td>\n";
	print "<td>\n";
	print "<input type=radio name=localhost_servername value=0>\n";
	print "<input size=20 name=servername value=\"$servername\">&nbsp;&nbsp;&nbsp;\n";
	print "<input type=radio checked name=localhost_servername value=1>$text{'create_server_localhost'}\n";
	print "</td></tr>\n";
	print "<tr>\n";
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
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_uams'}</b></td>";
		    print "<td>";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_guest\">Guest";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_clrtxt\">Cleartext";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_randnum\">Randnum";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_dhx\">DHX";
			print "<input type=\"checkbox\" name=\"uams\" checked value=\"$uams_dhx2\">DHX2";
			print "<input type=\"checkbox\" name=\"uams\" value=\"$uams_gss\">Kerberos";
			print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_Address'}</b></td>";
		print "<td><input size=15 maxlength=15 name=address value=\"\"></td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_Port'}</b></td>";
		print "<td><input type=\"number\" name=\"port\" min=\"0\" max=\"65535\" value=\"\"></td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_pass'}</b></td>";
		print "<td><input type=radio checked name=savepassword value=-savepassword>$text{'global_ON'}";
			print "<input type=radio name=savepassword value=-nosavepassword>$text{'global_OFF'}";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_setpass'}</b></td>";
		print "<td><input name=setpassword type=radio value=-setpassword>$text{'global_ON'}";
			print "<input type=radio checked name=setpassword value=-nosetpassword>$text{'global_OFF'}";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_lgmesg'}</b></td>";
		print "<td colspan=3><input size=25 maxlength=25 name=logmesg value=\"$loginmesg\"></td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_icon'}</b></td>";
		print "<td><input type=radio name=icon value=-icon>$text{'global_ON'}";
			print "<input type=radio checked name=icon value=-noicon>$text{'global_OFF'}";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_mimicmodel'}</b></td>";
		    print "<td><select name=\"mimicmodel\">";
			print "<option value=\"\">$text{'edit_default'}</option>\n";
			print "<option value=\"$text{mimicmodel_rackmac}\" %s>$text{mimicmodel_rackmac}</option>\n";
			print "<option value=\"$text{mimicmodel_powerbook}\" %s>$text{mimicmodel_powerbook}</option>\n";
			print "<option value=\"$text{mimicmodel_powermac}\" %s>$text{mimicmodel_powermac}</option>\n";
			print "<option value=\"$text{mimicmodel_macmini}\" %s>$text{mimicmodel_macmini}</option>\n";
			print "<option value=\"$text{mimicmodel_imac}\" %s>$text{mimicmodel_imac}</option>\n";
			print "<option value=\"$text{mimicmodel_macbook}\" %s>$text{mimicmodel_macbook}</option>\n";
			print "<option value=\"$text{mimicmodel_macbookpro}\" %s>$text{mimicmodel_macbookpro}</option>\n";
			print "<option value=\"$text{mimicmodel_macbookair}\" %s>$text{mimicmodel_macbookair}</option>\n";
			print "<option value=\"$text{mimicmodel_macpro}\" %s>$text{mimicmodel_macpro}</option>\n";
			print "<option value=\"$text{mimicmodel_appletv}\" %s>$text{mimicmodel_appletv}</option>\n";
			print "<option value=\"$text{mimicmodel_airport}\" %s>$text{mimicmodel_airport}</option>\n";
		    print "</select>\n";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_setuplog'}</b></td>";
		print "<td colspan=3><input size=52 name=setuplog value=\"$setuplog\"><br>$text{'create_server_setuplog_help'}</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_maccodepage'}</b></td>";
		    print "<td><select name=\"maccodepage\">";
			print "<option value=\"\">$text{'edit_default'}</option>\n";
			print "<option value=\"MAC_CENTRALEUROPE\" %s>MAC_CENTRALEUROPE</option>\n";
			print "<option value=\"MAC_CHINESE_SIMP\" %s>MAC_CHINESE_SIMP</option>\n";
			print "<option value=\"MAC_CHINESE_TRAD\" %s>MAC_CHINESE_TRAD</option>\n";
			print "<option value=\"MAC_CYRILLIC\" %s>MAC_CYRILLIC</option>\n";
			print "<option value=\"MAC_GREEK\" %s>MAC_GREEK</option>\n";
			print "<option value=\"MAC_HEBREW\" %s>MAC_HEBREW</option>\n";
			print "<option value=\"MAC_JAPANESE\" %s>MAC_JAPANESE</option>\n";
			print "<option value=\"MAC_KOREAN\" %s>MAC_KOREAN</option>\n";
			print "<option value=\"MAC_ROMAN\" %s>MAC_ROMAN</option>\n";
			print "<option value=\"MAC_TURKISH\" %s>MAC_TURKISH</option>\n";
		    print "</select>\n";
		print "</td>";
	print "</tr>\n";
print "</table>\n";

print "<div><i>$text{'create_server_notice'}</i></div>";
print "<input type=submit value=$text{'edit_create'}>\n";
print "<input type=reset value=$text{'edit_reset'}>\n";
print "</form>\n";

ui_print_footer("index.cgi", $text{'index_module'});
