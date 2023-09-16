#!/usr/bin/perl
# List of the different server configurations

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

ui_print_header(undef, $text{'servers_title'}, "", "configs", 1);

@Servers = readAfpd();
if(@Servers[1] ne ""){
	print "<table width=100% border>\n";
	print "<tr $tb>";
	print "<td><b>$text{'index_servername'}</b></td>";
	print "<td><b>$text{'index_tcp'}</b></td>";
	print "<td><b>$text{'index_ddp'}</b></td>";
	print "<td><b>$text{'index_port'}</b></td>";
	print "<td><b>$text{'index_address'}</b></td>";
	print "</tr>\n";
	print "<tr>";
	$offset = 0;
	$servername="servername=";
	$tcp="tcpip=";
	$ddp="ddp=";
	$port="port=";
	$address="address=";
	$offsetStr="offset=";
	for($i=0;$i<=$#Servers;$i++){
		if( ($i%5 ==0) && ($i ne 0)){
			print"<td><b>$Servers[$i]</b></td></tr><tr>";
			$i++;
			$pointer=$i;
			$offset++;
			print"<td><a href=\"server_edit_form.cgi?$offsetStr$offset\"><b>$Servers[$i]</b></a></td>";
		}
		elsif($i ne 0 && $i >1){
			print"<td><b>$Servers[$i]</b></td>";
		}
		elsif($i ne 0 && $i eq 1){
			$pointer=$i;
			print"<td><a href=\"server_edit_form.cgi?$offsetStr$offset\"><b>$Servers[$i]</b></a></td>";
		}
	}
	print "</tr></table>\n";
}
print "<p>";		
print "<a href=\"server_create_form.cgi\">$text{'index_newServer'}</a>\n&nbsp&nbsp&nbsp";
print "<p>";

ui_print_footer("index.cgi", $text{'edit_return'});

### END of servers.cgi ###.
