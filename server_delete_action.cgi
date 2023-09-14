#!/usr/bin/perl
# Delete a server configuration

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
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

use CGI qw/:standard/;
require './netatalk2-lib.pl';


&ReadParse();
$hostname=getHostName();
	
$filetoedit = $config{'afpd_c'};
if($in{delete_servername}){
	$server=$in{delete_servername};
	$server =~ /$hostname*/ ? $server="-" : "";
}
else {
	die "No server to delete";
}

deleteSpezLine($filetoedit, $server);

redirect("servers.cgi");
