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

require 'netatalk2-lib.pl';
ui_print_header(undef, $text{'index_title'}, "", "configs", 1, 1);

if (!-x $config{'afpd_d'}) {
	print &text('index_ever',"<tt> $config{'netatalk2'}</tt>", "/config.cgi?$module_name");
	print "<p>\n<hr>\n";
	ui_print_footer("/", $text{'index'});
	exit;
}

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

print &ui_hr();

# Print AFP volumes	
print "<p>";
print "    <h3>$text{index_volumes}</h3>\n";
print "    <table width=\"100%\" border>\n";
print "    <tr $tb>"; 
print "        <td><b>$text{'index_sharename'}</b></td>";
print "        <td><b>$text{'index_path'}</b></td>\n";
print "        <td><b>$text{'index_options'}</b></td>\n";
print "    </tr>\n";
foreach $s (open_afile()){
    $sharename = getShareName($s);
    $path = getPath($s);
    $options = getAllOptions($s);
    print "<tr $cb>\n";
    print "    <td><a href=\"fshare_edit_form.cgi?shareName=$sharename&path=$path\"><b>$sharename</b></a></td>";
    print "    <td><b>$path</b></td>";
    print "    <td><b>$options</b></td>";
    print "</tr>";
}
print "</table>\n";

my @volume_links = ("fshare_create_form.cgi","fshare_delete_form.cgi");
my @volume_titles = ($text{'index_create_file_share'},$text{'index_delete_file_share'});
my @volume_icons = ("images/volumes.gif","images/misc.png");
icons_table(\@volume_links, \@volume_titles, \@volume_icons);

print "<h3>$text{index_global}</h3>\n";

my @global_links = ("servers.cgi","show_users.cgi","edit_configfiles_form.cgi");
my @global_titles = ($text{'index_server'},$text{'index_users'},$text{'index_edit'});
my @global_icons = ("images/server.png","images/users.png","images/edit.gif");
icons_table(\@global_links, \@global_titles, \@global_icons);
print "</table>\n";

### END of index.cgi ###.
