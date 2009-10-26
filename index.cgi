#!/usr/bin/perl
#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Some code (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Contributions from:
#	Sven Mosimann <sven.mosimann@ecologic.ch>
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
#    This module inherited from the Webmin Module Template 0.79.1

require '../web-lib.pl';
&init_config();
require '../ui-lib.pl';

do '../web-lib.pl'; # Webmin's lib
require 'netatalk-funcs.pl'; # Matt's lib + merges

## put in ACL checks here if needed


&header($text{'index_title'}, "", undef, 1, 1, undef());
do './netapple-lib.pl'; # Sven's lib


print "<a href=help/volumehelp.cgi>$text{volume_help}</a><br><BR>\n";

print "<hr>\n";
#print "<h3>$text{module_status}</h3>\n";
#print "<h3>$text{disclaim_power}</h3>\n";

if (!-x $config{'atalkd_d'}) {
	print &text('index_ever',"<tt> $config{'netapple'}</tt>",
	 "/config.cgi?$module_name");
	print "<p>\n<hr>\n";
	&footer("/", $text{'index'});
	exit;
	}
if (!-x $config{'papd_d'}) {
	print &text('index_ever',"<tt> $config{'netapple'}</tt>",
	 "/config.cgi?$module_name");
	print "<p>\n<hr>\n";
	&footer("/", $text{'index'});
	exit;
	}
if (!-x $config{'afpd_d'}) {
	print &text('index_ever',"<tt> $config{'netapple'}</tt>",
	 "/config.cgi?$module_name");
	print "<p>\n<hr>\n";
	&footer("/", $text{'index'});
	exit;
	}
	
$share= "shareName=";
$Path="path=";


#Test ob alle Files vorhanden sind
#mgk: Test whether all files available are

	
##Tabelle zeichnen und infos auslesen--------------------	
##mgk: Table draw and information select

print"<p>";

   print "<table width=100% border>\n";
       print "<tr $tb>"; 
           print"<td><b>$text{'index_sharename'}</b></td>";
           print"<td><b>$text{'index_path'}</b></td>\n";
       print" </tr>\n";
       foreach $s (open_afile()){
       $sharename = getShareName($s);
       $path = getPath($s);
       print"<tr $cb>\n";
           print"<td><a href=\"modi_fshare.cgi?$share$sharename&$Path$path\"><b>$sharename</b></a></td>";
           print"<td><b>$path</b></td>";
       print"</tr>";
       }
   print "</table>\n";

print"<p>";
print "<a href=\"edit_fshare.cgi\">$text{'index_create_file_share'}</a>\n&nbsp&nbsp&nbsp";
print "<a href=\"delete_fshare.cgi\">$text{'index_delete_file_share'}</a>\n";
print"<p>";
print"<hr>\n";
print"<p>\n";

print"<h3>$text{index_global}</h3>\n";

my @links = ("servers.cgi","edit_interfaces.cgi","show_users.cgi", "misc_opt.cgi");
my @titles = ($text{'index_server'},$text{'index_interfaces'},$text{'index_users'},$text{'index_misc'});
#my @icons = ("images/what.gif","images/interface.gif","images/procs.gif","images/icon_4.gif");
my @icons = ("images/server.png","images/interface.png","images/users.png","images/misc.png");
icons_table(\@links, \@titles, \@icons);
print"<br>\n";

print"<hr>\n";
#pid finden
@atlkd = &find_byname("atalkd");
if(@atlkd){
	print "<form action=restart.cgi>\n";
	print "<table width=100% align=center><tr>\n";
	print "<td width=10% align=right><input type=submit value=Restart></td>\n";
	print "<td>$text{'index_running_service'}<br>$text{'index_restart'}</td>\n";
	print "</tr></table></form>\n";
	
	print "<form action=stop.cgi>\n";
	print "<table width=100% align=center><tr>\n";
	print "<td width=10% align=right><input type=submit value=Stop></td>\n";
	print "<td>$text{'index_stop_service'}<br>$text{'index_stop'}</td>\n";
	print "</tr></table></form>\n";
	
}
else{
	print "<form action=start.cgi>\n";
	print "<table width=100% align=center><tr>\n";
	print "<td width=20% align=right><input type=submit value=\"$text{'index_start_but'}\"></td>\n";
	print "<td align=left>$text{'index_not_running'}<br>$text{'index_start_service'}</td>\n";
	print "</tr></table></form>\n";
	
}

print"<p>";
print "<hr>\n";
&footer("/", $text{'index'});

### END of index.cgi ###.
