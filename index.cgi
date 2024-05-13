#!/usr/bin/perl
#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Copyright (C) 2023-4 Daniel Markstedt <daniel@mindani.net>
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

require 'netatalk2-lib.pl';
ui_print_header(version(), $text{'index_title'}, "", "configs", 1, 1);

if (!-x $config{'afpd_d'}) {
	print &text('index_ever',"<tt> $config{'netatalk2'}</tt>", "/config.cgi?$module_name");
	ui_print_footer("/", $text{'index'});
	exit;
}

@Shares = open_afile();

print "<h3>$text{index_volumes_title}</h3>\n";

# Print AFP volumes
if((scalar @Shares > 1) || (scalar @Shares eq 1 && ! $Shares[0] =~ "^:DEFAULT:")){
	print "    <table width=\"100%\" border>\n";
	print "    <tr $tb>";
	print "        <td>$text{'index_sharename'}</td>";
	print "        <td>$text{'index_path'}</td>\n";
	print "        <td>$text{'index_options'}</td>\n";
	print "    </tr>\n";
	foreach $s (@Shares) {
		$sharename = getShareName($s);
		$path = getPath($s);
		$options = getAllOptions($s);
		if ($sharename ne ":DEFAULT:") {
			print "<tr $cb>\n";
			print "    <td><a href=\"fshare_edit_form.cgi?shareName=$sharename&path=$path&action=edit\">$sharename</a></td>";
			print "    <td>$path</td>";
			print "    <td>$options</td>";
			print "</tr>";
		}
	}
	print "</table>\n";
} else {
	print "<p><b>$text{'index_no_file_shares'}</b></p>";
}
print ui_buttons_start();
print ui_buttons_row('fshare_edit_form.cgi?action=create', $text{'index_create_file_share'});
print ui_buttons_end();

print &ui_hr();

# Print Netatalk Server Configurations
print "<h3>$text{'index_servers_title'}</h3>\n";

@Servers = readAfpd();
if(@Servers[1] ne ""){
	print "<table width=100% border>\n";
	print "<tr $tb>";
	print "<td>$text{'index_servername'}</td>";
	print "<td>$text{'index_protocols'}</td>";
	print "<td>$text{'index_auth'}</td>";
	print "<td>$text{'index_port'}</td>";
	print "<td>$text{'index_address'}</td>";
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
			print"<td>$Servers[$i]</td></tr><tr>";
			$i++;
			$pointer=$i;
			$offset++;
			print"<td><a href=\"server_edit_form.cgi?action=edit&$offsetStr$offset\">$Servers[$i]</a></td>\n";
		}
		elsif($i ne 0 && $i >1){
			print"<td>$Servers[$i]</td>\n";
		}
		elsif($i ne 0 && $i eq 1){
			$pointer=$i;
			print"<td><a href=\"server_edit_form.cgi?action=edit&$offsetStr$offset\">$Servers[$i]</a></td>\n";
		}
	}
	print "</tr>\n";
	print "</table>\n";
} else {
	print "<p><b>".&text('index_server_default_active', &get_system_hostname())."</b></p>";
}
print ui_buttons_start();
print ui_buttons_row('server_edit_form.cgi?action=create', $text{'index_create_server'});
print ui_buttons_end();

print &ui_hr();

print"<h3>$text{index_global}</h3>\n";

my @server_links = ("fshare_edit_form.cgi?shareName=:DEFAULT:&action=default", "show_users.cgi", "edit_configfiles_form.cgi", "server_status.cgi");
my @server_titles = ($text{'index_volumes_default'}, $text{'index_users'}, $text{'index_edit'}, "$text{index_capabilities}");
my @server_icons = ("images/volumes.gif", "images/users.gif", "images/edit.gif", "images/server.gif");
icons_table(\@server_links, \@server_titles, \@server_icons);

print &ui_hr();

# since we are using a different number of forms, depending on the status of the service,
# we are keeping a running index while outputting the forms
my $current_formindex = 0;

# Process control Buttons
if(&find_byname($config{'afpd_d'})) {
    print "<h3>$text{'index_running_services'}</h3>\n";
	print &ui_buttons_start();
	print &ui_buttons_row('restart.cgi', $text{'index_process_control_restart'}, &text('index_process_control_restart_txt', $config{restart_netatalk}));
	print &ui_buttons_row('stop.cgi', $text{'index_process_control_stop'}, &text('index_process_control_stop_txt', $config{stop_netatalk}));
	print &ui_buttons_end();
	$current_formindex += 2;
} else {
    print "<h3>$text{'index_not_running_services'}</h3>\n";
	print &ui_buttons_start();
	print &ui_buttons_row('start.cgi', $text{'index_process_control_start'}, &text('index_process_control_start_txt', $config{start_netatalk}));
	print &ui_buttons_end();
	$current_formindex += 1;
}

### END of index.cgi ###.
