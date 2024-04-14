#!/usr/bin/perl
# Display a form for editing an existing file share

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

require 'netatalk2-lib.pl';

&ReadParse();

ui_print_header(undef, $text{'edit_server_header'}, "", "servers", 1);

local $servername = "";
$ddpon = "-ddp";
$tcpon = "-tcp";
$savepasswon = "-savepassword";
$setpasswon = "-setpassword";
$iconon = "-icon";

$uams_guest = "uams_guest.so";
$uams_clrtxt = "uams_clrtxt.so";
$uams_randnum = "uams_randnum.so";
$uams_dhx = "uams_dhx.so";
$uams_dhx2 = "uams_dhx2.so";
$uams_gss = "uams_gss.so";

if($in{offset}){
	$offset=$in{offset};
}
else{
	$offset=0;
}

%allServer = getAllAfpd();
$servername = $allServer{$offset}[0];
$tcpip = $allServer{$offset}[1];
$ddp = $allServer{$offset}[2];
$port = $allServer{$offset}[3];
$address = $allServer{$offset}[4];
$loginmsg = $allServer{$offset}[5];
$savepass = $allServer{$offset}[6];
$setpass = $allServer{$offset}[7];
$uamlist = $allServer{$offset}[8];
$icon = $allServer{$offset}[9];
$mimicmodel = $allServer{$offset}[10];
$setuplog = $allServer{$offset}[11];
$maccodepage = $allServer{$offset}[12];

print "<p><p>\n";
print "<form action=server_save_action.cgi>\n";

print "<table width=100%>\n";
	print "<tr>\n";
	print "<td align=right><b>$text{'create_server_ServerName'}</b></td>\n";
	print "<td colspan=4>";
	printf "<input type=radio name=localhost_servername %s value=0>\n",
		$servername eq "" ? "" : "checked";
	print "<input size=20 name=servername value=\"$servername\">&nbsp;&nbsp;&nbsp;\n";
	printf "<input type=radio name=localhost_servername %s value=1>$text{'create_server_localhost'}\n",
		$servername eq "" ? "checked" : "";
	print "</td>\n";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_TCP'}</b></td>";
		    print "<td>";
			printf "<input type=radio %s name=tcpip value=-tcp>$text{'global_ON'}",
				$tcpip =~ /$tcpon*/ ? "checked" : "";
			printf "<input type=radio %s name=tcpip value=-notcp>$text{'global_OFF'}",
				$tcpip =~ /$tcpon*/ ? "" : "checked";
			print "</td></tr>";
		print "<tr><td align=right><b>$text{'create_server_AppleTalk'}</b></td>";
		print "<td>";
		printf "<input type=radio name=ddp %s value=-ddp>$text{'global_ON'}",
				$ddp =~ /$ddpon*/ ? "checked" : "";
			printf "<input type=radio name=ddp %s value=-noddp>$text{'global_OFF'}",
				$ddp =~ /$ddpon*/ ? "" : "checked";
			print"</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_uams'}</b></td>";
		    print "<td>";
			printf "<input type=\"checkbox\" %s name=\"uams\" value=\"$uams_guest\">Guest",
				$uamlist =~ /$uams_guest*/ ? "checked" : "";
			printf "<input type=\"checkbox\" %s name=\"uams\" value=\"$uams_clrtxt\">Cleartext",
				$uamlist =~ /$uams_clrtxt*/ ? "checked" : "";
			printf "<input type=\"checkbox\" %s name=\"uams\" value=\"$uams_randnum\">Randnum",
				$uamlist =~ /$uams_randnum*/ ? "checked" : "";
			printf "<input type=\"checkbox\" %s name=\"uams\" value=\"$uams_dhx\">DHX",
				$uamlist =~ /$uams_dhx*/ ? "checked" : "";
			printf "<input type=\"checkbox\" %s name=\"uams\" value=\"$uams_dhx2\">DHX2",
				$uamlist =~ /$uams_dhx2*/ ? "checked" : "";
			printf "<input type=\"checkbox\" %s name=\"uams\" value=\"$uams_gss\">Kerberos",
				$uamlist =~ /$uams_gss*/ ? "checked" : "";
			print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_Address'}</b></td>";
		printf "<td><input size=15 maxlength=15 name=address value=\"%s\"></td>",
				$address =~ /[0-9.]/ ? $address : "";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_Port'}</b></td>";
		printf" <td><input type=\"number\" name=\"port\" min=\"0\" max=\"65535\" value=\"%s\"></td>",
				$port =~ /[0-9]/ ? $port : "";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_pass'}</b></td>";
		printf "<td><input name=setpassword type=radio %s value=-setpassword>$text{'global_ON'}",
				$setpass =~ /$setpasswon/ ? "checked" : "";
			printf "<input type=radio %s name=setpassword value=-nosetpassword>$text{'global_OFF'}",
				$setpass =~ /$setpasswon/ ? "" : "checked";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_setpass'}</b></td>";
		printf "<td><input type=radio %s name=savepassword value=-savepassword>$text{'global_ON'}",
				$savepass =~ /$savepasswon*/ ? "checked" : "";
			printf "<input type=radio %s name=savepassword value=-nosavepassword>$text{'global_OFF'}",
				$savepass =~ /$savepasswon*/ ? "" : "checked";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_lgmesg'}</b></td>";
		print "<td colspan=3><input size=35 name=logmesg value=\"$loginmesg\">";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_icon'}</b></td>";
		printf "<td><input type=radio %s name=icon value=-icon>$text{'global_ON'}",
				$icon =~ /$iconon*/ ? "checked" : "";
			printf "<input type=radio %s name=icon value=-noicon>$text{'global_OFF'}",
				$icon =~ /$iconon*/ ? "" : "checked";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_mimicmodel'}</b></td>";
		print "<td><input size=35 name=\"mimicmodel\" value=\"$mimicmodel\">";
		print "<br><i>$text{'create_server_mimicmodel_help'}</i>";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_setuplog'}</b></td>";
		print "<td colspan=3><input size=52 name=setuplog value=\"$setuplog\">";
		print "<br><i>$text{'create_server_setuplog_help'}</i>";
		print "</td>";
	print "</tr>\n";
	print "<tr>\n";
		print "<td align=right><b>$text{'create_server_maccodepage'}</b></td>";
		    print "<td><select name=\"maccodepage\">";
			printf "<option value=\"\">$text{'edit_default'}";
		    print "</option>\n";
			printf "<option value=\"MAC_CENTRALEUROPE\" %s>MAC_CENTRALEUROPE",
				$maccodepage =~ /MAC_CENTRALEUROPE/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_CHINESE_SIMP\" %s>MAC_CHINESE_SIMP",
				$maccodepage =~ /MAC_CHINESE_SIMP/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_CHINESE_TRAD\" %s>MAC_CHINESE_TRAD",
				$maccodepage =~ /MAC_CHINESE_TRAD/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_CYRILLIC\" %s>MAC_CYRILLIC",
				$maccodepage =~ /MAC_CYRILLIC/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_GREEK\" %s>MAC_GREEK",
				$maccodepage =~ /MAC_GREEK/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_HEBREW\" %s>MAC_HEBREW",
				$maccodepage =~ /MAC_HEBREW/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_JAPANESE\" %s>MAC_JAPANESE",
				$maccodepage =~ /MAC_JAPANESE/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_KOREAN\" %s>MAC_KOREAN",
				$maccodepage =~ /MAC_KOREAN/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_ROMAN\" %s>MAC_ROMAN",
				$maccodepage =~ /MAC_ROMAN/ ? "selected" : "";
		    print "</option>\n";
			printf "<option value=\"MAC_TURKISH\" %s>MAC_TURKISH",
				$maccodepage =~ /MAC_TURKISH/ ? "selected" : "";
		    print "</option>\n";
		    print "</select>\n";
			print "</td>";
	print "</tr>\n";
print "</table>\n";

print "<div><i>$text{'create_server_notice'}</i></div>";
printf "<input type=\"hidden\" name=\"old_servername\" value=\"%s\">\n",
		$servername eq "" ? "-" : $servername;
print "<input type=\"submit\" value=\"$text{'global_Save'}\">\n";
print "</form>\n";

print "<form action=\"server_delete_action.cgi\">";
printf "<input type=\"hidden\" name=\"delete_servername\" value=\"$servername\">\n",
		$servername eq "" ? "-" : $servername;
print "<input type=\"submit\" value=\"$text{'edit_delete'}\">\n";
print "</form>\n";

ui_print_footer("index.cgi", $text{'index_module'});
