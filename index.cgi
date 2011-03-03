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

## put in ACL checks here if needed


&header($text{'index_title'}, "", undef, 1, 1, undef(), "<a href=\"help/configs.cgi\">$text{help_configs}</a>");
do './netapple-lib.pl'; # Sven's lib

if (!-x $config{'afpd_d'}) {
	print &text('index_ever',"<tt> $config{'netapple'}</tt>", "/config.cgi?$module_name");
	print "<p>\n<hr>\n";
	&footer("/", $text{'index'});
	exit;
}

print "<hr>\n";

# Print start/stop part
@afpd = &find_byname($config{'afpd_d'});
if(@afpd){
    print qq|<h3>$text{'index_running_services'}</h3>|;
	print qq|	<table width="100%" cellspacing="8" cellpadding="8" border="0">
					<tr height="20">
						<td width="165" align="center"><form action="restart.cgi"><input type="submit" value="$text{'index_restart'}"></form></td>
						<td>Click this button to restart netatalk services using <code>$config{restart_netatalk}</code></td>
					</tr>
					<tr height="20">
						<td width="165" align="center"><form action="stop.cgi"><input type="submit" value="$text{'index_stop'}"></form></td>
						<td>Click this button to stop netatalk services using <code>$config{'stop_netatalk'}</code></td>
					</tr>
				</table>
			|;
} else{
    print qq|<h3>$text{'index_not_running_services'}</h3>|;
	print qq|	<table width="100%" cellspacing="8" cellpadding="8" border="0">
					<tr height="20">
						<td width="165" align="center"><form action="start.cgi"><input type="submit" value="$text{'index_start_service'}"></form></td>
						<td>Click this button to start netatalk services using <code>$config{'start_netatalk'}</code></td>
					</tr>
				</table>
			|;
}

print "<hr>\n";

# Print AFP volumes	
$share= "shareName=";
$Path="path=";
print "<p>";
print "    <h3>$text{index_volumes}</h3>\n";
print "    <table width=\"100%\" border>\n";
print "    <tr $tb>"; 
print "        <td><b>$text{'index_sharename'}</b></td>";
print "        <td><b>$text{'index_path'}</b></td>\n";
print "    </tr>\n";
foreach $s (open_afile()){
    $sharename = getShareName($s);
    $path = getPath($s);
    print "<tr $cb>\n";
    print "    <td><a href=\"modi_fshare.cgi?$share$sharename&$Path$path\"><b>$sharename</b></a></td>";
    print "    <td><b>$path</b></td>";
    print "</tr>";
}
print "</table>\n";

print"<p>";
print "<a href=\"edit_fshare.cgi\">$text{'index_create_file_share'}</a>\n&nbsp&nbsp&nbsp";
print "<a href=\"delete_fshare.cgi\">$text{'index_delete_file_share'}</a>\n";
print"<p>";
print"<hr>\n";
print"<p>\n";

print"<h3>$text{index_global}</h3>\n";

my @links = ("servers.cgi","show_users.cgi","misc_opt.cgi","edit_configfiles_form.cgi");
my @titles = ($text{'index_server'},$text{'index_users'},$text{'index_misc'},$text{'index_edit'});
my @icons = ("images/server.png","images/users.png","images/misc.png","images/edit.gif");
icons_table(\@links, \@titles, \@icons);
print"<br>\n";

print"<hr>\n";

print "</table>\n";
print"<p>";
print "<hr>\n";

&footer("/right.cgi?open=system&auto=status&open=updates", $text{'index_root'});

### END of index.cgi ###.
