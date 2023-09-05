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

&ReadParse();

&header($text{'editexist_server_header'},"", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\" target=\"_blank\">$text{help_configs}</a>");

print"<p>\n";


$ddpon="-ddp";
$tcp="-tcp";


$hostname=getHostName();#$hostli;#chomp($host);
#$hostname="dellux";

if($in{offset}){
	#print"Offset: $in{offset}<br>\n";
	$offset=$in{offset};
	#print"Port : $port <br>\n";
}
else{
	 #print"Offset: 0<br>\n";
	 $offset=0;
}

@allServer =   getAllAfpd();
$off= $offset*7;
$off= $off+$offset;
for($i=0;$i<=7;$i++){
	if($i eq 0){
		 $servername= @allServer[$off];
	}
	elsif($i eq 1){
		 $tcpip= @allServer[$off];
	}
	elsif($i eq 2){
		 $ddp= @allServer[$off];
	}
	elsif($i eq 3){
		 $address= @allServer[$off];
	}
	elsif($i eq 4){
		 $port= @allServer[$off];
	}
	elsif($i eq 5){
		 $loginmesg= @allServer[$off];
	}
	elsif($i eq 6){
		 $savepassw= @allServer[$off];
	}
	elsif($i eq 7){
		 $setpass= @allServer[$off];
	}
     $off++;
}

print "<hr>\n";
print"<p><p>\n";
print "<form action=save_newServer.cgi>\n";

print "<table  width=100% >\n";
print "<tr $tb> <td><b>$text{'editexist_server_table_header'}</b></td></tr>\n";
print "<tr $cb> <td><table >\n";
	print "<tr><td align=right><b>$text{'create_server_ServerName'}</b></td>\n";
	print "<td colspan=4>";
	printf "<input  type=radio name=server %s value=0>\n",
		$servername =~ /$hostname*/ ? "" : "checked";
	
	print "<input size=10 name=servername value=$servername>&nbsp;&nbsp;&nbsp;\n";
	#print "<input type=radio name=server checked  value=1 >&nbsp;&nbsp;&nbsp;<b>$text{'create_server_localhost'}</b>\n";
	printf "<input  type=radio name=server %s value=1>&nbsp;&nbsp;&nbsp;<b>$text{'create_server_localhost'}</b>\n",
		$servername =~  /$hostname*/  ? "checked" : "";
	print "</td> </tr>\n";
	print"<tr>";
		print"<td  align=right><b>$text{'create_server_TCP'}</b></td>";
		    print"<td>";
			printf"<input type=radio %s name=tcpip value=-tcp>$text{'global_ON'}",
				   $tcpip =~ /$tcp*/ ? "checked" : "";
			printf"<input type=radio name=tcpip %s value=-notcp>$text{'global_OFF'}",
					$tcpip =~ /$tcp*/ ? "" : "checked";
			print"</td>";
		print"<td align=right><b>$text{'create_server_AppleTalk'}</b></td>";
		print"<td >";
		printf"<input type=radio name=ddp %s value=-ddp>$text{'global_ON'}",
				$ddp =~ /$ddpon*/ ? "checked" : "";
			printf"<input type=radio name=ddp %s value=-noddp>$text{'global_OFF'}",
				 $ddp =~ /$ddpon*/ ? "" : "checked";
			print"</td>";
	print"</tr>";
	print"<tr >";
		print"<td align=right><b>$text{'create_server_Port'}</b></td>";
		printf"<td > <input size=10 name=port value=%s></td>",
				$port =~ /[0-9]/ ? $port : "";
		print"<td align=right><b>$text{'create_server_Address'}</b></td>";
		printf"<td><input size=15 maxlength=15 name=address value=%s></td>",
				$address =~ /[0-9.]/ ? $address : "";
	print"</tr>";
	print"<tr >";
		print"<td align=right><b>$text{'create_server_pass'}</b></td>";$setpassw="setpassword";
		printf"<td ><input name=setpassword type=radio %s  value=setpassword>$text{'global_ON'}",
		          $setpass =~ /$setpassw/ ? "checked" : "";	
			printf"<input type=radio  %s name=setpassword value=>$text{'global_OFF'}",
				  $setpass =~ /$setpassw/ ? "" : "checked";
		print"</td>";
		print"<td align=right><b>$text{'create_server_setpass'}</b></td>";$savepass="savepassword";
		printf"<td ><input type=radio %s name=savepassword value=savepassword>$text{'global_ON'}",
				$savepassw =~ /$savepass*/ ? "checked" : "";
			printf"<input type=radio %s name=savepassword value=>$text{'global_OFF'}",
				    $savepassw =~ /$savepass*/ ? "" : "checked";
		print"</td>";
	print"</tr>";
	print"<tr >";
		print"<td align=right><b>$text{'create_server_lgmesg'}</b></td>";
		 print"<td colspan=3><input size=25 maxlength=25 name=logmesg value=\"$loginmesg\"></td>";
	print"</tr>";
print "</table> </td></tr></table><p>\n";

print "<table  width=100% >\n";
print"<tr>";
print "<input type=hidden name=old_servername value=$servername>\n";
print "<input type=hidden name=old_tcpip value=$tcpip>\n";
print "<input type=hidden name=old_ddp value=$ddp>\n";
print "<input type=hidden name=old_port value=$port>\n";
print "<input type=hidden name=old_adress value=$address>\n";
print "<input type=hidden name=link value=\"servers.cgi\">\n";

print "<td align=left><input type=submit value=$text{'global_Save'}></td></form>\n";

print"<form action=delete_server.cgi>";
print "<input type=hidden name=servername value=$servername>\n";
print "<input type=hidden name=tcpip value=$tcpip>\n";
print "<input type=hidden name=ddp value=$ddp>\n";
print "<input type=hidden name=port value=$port>\n";
print "<input type=hidden name=adress value=$address>\n";
print "<td align=right><input type=submit value=$text{'edit_delete'}></td>\n";
print"</tr></table></form>";

print "<hr>\n";
print"<p><p>\n";
&footer("servers.cgi","Servers");
