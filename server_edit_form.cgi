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

ui_print_header(undef, $text{'edit_server_header'}, "", "configs", 1);

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

$hostname=getHostName();

if($in{offset}){
	$offset=$in{offset};
}
else{
	$offset=0;
}

@allServer = getAllAfpd();
$off = $offset*10;
$off = $off+$offset;
for($i=0; $i<=10; $i++){
	if($i eq 0){
		 $servername = @allServer[$off];
	}
	elsif($i eq 1){
		 $tcpip = @allServer[$off];
	}
	elsif($i eq 2){
		 $ddp = @allServer[$off];
	}
	elsif($i eq 3){
		 $port = @allServer[$off];
	}
	elsif($i eq 4){
		 $address = @allServer[$off];
	}
	elsif($i eq 5){
		 $loginmesg = @allServer[$off];
	}
	elsif($i eq 6){
		 $savepass = @allServer[$off];
	}
	elsif($i eq 7){
		 $setpass = @allServer[$off];
	}
	elsif($i eq 8){
		 $uamlist = @allServer[$off];
	}
	elsif($i eq 9){
		 $icon = @allServer[$off];
	}
	elsif($i eq 10){
		 $mimicmodel = @allServer[$off];
	}
	$off++;
}

print "<p><p>\n";
print "<form action=server_save_action.cgi>\n";

print "<table width=100%>\n";
print "<tr $tb> <td><b>$text{'edit_server_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td>\n";
print "<table>\n";
	print "<tr><td align=right><b>$text{'create_server_ServerName'}</b></td>\n";
	print "<td colspan=4>";
	printf "<input type=radio name=server %s value=0>\n",
		$servername =~ /$hostname*/ ? "" : "checked";
	printf "<input size=20 name=servername value=\"%s\">&nbsp;&nbsp;&nbsp;\n",
		$servername =~ /$hostname*/ ? "" : $servername;
	printf "<input type=radio name=server %s value=1>$text{'create_server_localhost'}\n",
		$servername =~ /$hostname*/ ? "checked" : "";
	print "</td></tr>\n";
	print "<tr>";
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
	print "</tr>";
	print "<tr>";
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
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_Address'}</b></td>";
		printf "<td><input size=15 maxlength=15 name=address value=%s></td>",
				$address =~ /[0-9.]/ ? $address : "";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_Port'}</b></td>";
		printf" <td><input type=\"number\" name=\"port\" min=\"0\" max=\"65535\" value=\"%s\"></td>",
				$port =~ /[0-9]/ ? $port : "";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_pass'}</b></td>";
		printf "<td><input name=setpassword type=radio %s value=-setpassword>$text{'global_ON'}",
				$setpass =~ /$setpasswon/ ? "checked" : "";
			printf "<input type=radio %s name=setpassword value=-nosetpassword>$text{'global_OFF'}",
				$setpass =~ /$setpasswon/ ? "" : "checked";
		print "</td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_setpass'}</b></td>";
		printf "<td><input type=radio %s name=savepassword value=-savepassword>$text{'global_ON'}",
				$savepass =~ /$savepasswon*/ ? "checked" : "";
			printf "<input type=radio %s name=savepassword value=-nosavepassword>$text{'global_OFF'}",
				$savepass =~ /$savepasswon*/ ? "" : "checked";
		print "</td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_lgmesg'}</b></td>";
		print "<td colspan=3><input size=25 maxlength=25 name=logmesg value=\"$loginmesg\"></td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_icon'}</b></td>";
		printf "<td><input type=radio %s name=icon value=-icon>$text{'global_ON'}",
				$icon =~ /$iconon*/ ? "checked" : "";
			printf "<input type=radio %s name=icon value=-noicon>$text{'global_OFF'}",
				$icon =~ /$iconon*/ ? "" : "checked";
		print "</td>";
	print "</tr>";
	print "<tr>";
		print "<td align=right><b>$text{'create_server_mimicmodel'}</b></td>";
		    print "<td><select name=\"mimicmodel\">";
			printf "<option value=>$text{'edit_default'}";
			printf "<option value=\"$text{mimicmodel_rackmac}\" %s>$text{mimicmodel_rackmac}",
				$mimicmodel =~ /$text{mimicmodel_rackmac}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_powerbook}\" %s>$text{mimicmodel_powerbook}",
				$mimicmodel =~ /$text{mimicmodel_powerbook}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_powermac}\" %s>$text{mimicmodel_powermac}",
				$mimicmodel =~ /$text{mimicmodel_powermac}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_macmini}\" %s>$text{mimicmodel_macmini}",
				$mimicmodel =~ /$text{mimicmodel_macmini}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_imac}\" %s>$text{mimicmodel_imac}",
				$mimicmodel =~ /$text{mimicmodel_imac}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_macbook}\" %s>$text{mimicmodel_macbook}",
				$mimicmodel =~ /$text{mimicmodel_macbook}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_macbookpro}\" %s>$text{mimicmodel_macbookpro}",
				$mimicmodel =~ /$text{mimicmodel_macbookpro}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_macbookair}\" %s>$text{mimicmodel_macbookair}",
				$mimicmodel =~ /$text{mimicmodel_macbookair}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_macpro}\" %s>$text{mimicmodel_macpro}",
				$mimicmodel =~ /$text{mimicmodel_macpro}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_appletv}\" %s>$text{mimicmodel_appletv}",
				$mimicmodel =~ /$text{mimicmodel_appletv}*/ ? "selected" : "";
			printf "<option value=\"$text{mimicmodel_airport}\" %s>$text{mimicmodel_airport}",
				$mimicmodel =~ /$text{mimicmodel_airport}*/ ? "selected" : "";
			print "</td>";
	print "</tr>";
print "</table> </td></tr></table><p>\n";

print "<table width=100%>\n";
print "<tr>";
print "<input type=\"hidden\" name=\"old_servername\" value=\"$servername\">\n";
print "<td align=left><input type=\"submit\" value=\"$text{'global_Save'}\"></td></form>\n";

print "<table><tr><form action=\"server_delete_action.cgi\">";
print "<input type=\"hidden\" name=\"delete_servername\" value=\"$servername\">\n";
print "<td align=right><input type=\"submit\" value=\"$text{'edit_delete'}\"></td>\n";
print "</form></tr></table>";

ui_print_footer("servers.cgi", $text{'create_server_return'});
