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

@Shares = getAppleVolumes();
@Servers = getAfpdServers();
local $current_formindex = 0;

print "<h3>$text{index_volumes_title}</h3>\n";
my @volume_links = ( "<a href=\"edit_volumes.cgi?action=create\">$text{'index_create_file_share'}</a>" );

# Print AFP volumes
if ((scalar @Shares > 1) || (scalar @Shares eq 1 && ! $Shares[0] =~ "^:DEFAULT:")) {
	unshift @volume_links, (
		&select_all_link('section_index', $current_formindex),
		&select_invert_link('section_index', $current_formindex)
	);
	print &ui_form_start('delete_volumes.cgi', 'POST', undef, "id='volumes'");
	print &ui_columns_start([
			'',
			$text{'index_sharename'},
			$text{'index_path'},
			$text{'index_options'}
		], undef, 0, undef, undef);
	foreach $s (@Shares) {
		$sharename = getShareName($s);
		$path = getPath($s);
		$options = getAllOptions($s);
		if ($sharename ne ":DEFAULT:") {
			print &ui_checked_columns_row([
				"<a href=\"edit_volumes.cgi?shareName=$sharename&path=$path&action=edit\">$sharename</a>",
				$path,
				$options
			], [ "width='20'" ], 'section_index', $path);
		}
	}
	print &ui_columns_end();
	print &ui_form_end([[undef, $text{'index_delete_file_share'}, 0, undef]]);
	print &ui_links_row(\@volume_links);
	$current_formindex += 1;
} else {
	print "<p><b>$text{'index_no_file_shares'}</b></p>\n";
	print &ui_links_row(\@volume_links);
}

print &ui_hr();

# Print Netatalk Server Configurations
print "<h3>$text{'index_servers_title'}</h3>\n";
my @server_links = ( "<a href=\"edit_servers.cgi?action=create\">$text{'index_create_server'}</a>" );

if (@Servers) {
	unshift @server_links, (
		&select_all_link('section_index', $current_formindex),
		&select_invert_link('section_index', $current_formindex)
	);
	print &ui_form_start('delete_servers.cgi', 'POST', undef, "id='servers'");
	print &ui_columns_start([
			'',
			$text{'index_servername'},
			$text{'index_protocols'},
			$text{'index_auth'},
			$text{'index_port'},
			$text{'index_address'},
			$text{'index_maccodepage'}
		], undef, 0, undef, undef);
	local $offset = 0;
	foreach $s (@Servers){
		local $t = "";
		if($s->{transport} =~ /-transall/ || $s->{transport} =~ /-(ddp|tcp)\s+-(ddp|tcp)/ ){
			$t = "AppleTalk, TCP/IP";
		}
		elsif($s->{transport} =~ /-(ddp|notcp)\s+-(notcp|ddp)/ ){
			$t = "AppleTalk";
		}
		elsif($s->{transport} =~ /-(noddp|tcp)\s+-(tcp|noddp)/ ){
			$t = "TCP/IP";
		}
		print &ui_checked_columns_row([
			"<a href=\"edit_servers.cgi?action=edit&offset=".$offset."\">"
			.($s->{servername} ? $s->{servername} : &get_system_hostname())."</a>",
			$t,
			$s->{uamlist},
			$s->{port},
			$s->{ipaddr},
			$s->{maccodepage}
		], [ "width='20'" ], 'section_index', $s->{servername} eq "" ? "-" : $s->{servername});
		$offset++;
	}
	print &ui_columns_end();
	print &ui_form_end([[undef, $text{'index_delete_server'}, 0, undef]]);
	print &ui_links_row(\@server_links);
	$current_formindex += 1;
} else {
	print "<p><b>".&text('index_server_default_active', &get_system_hostname())."</b></p>";
	print &ui_links_row(\@server_links);
}

print &ui_hr();

print"<h3>$text{index_global}</h3>\n";

my @server_links = ("edit_volumes.cgi?shareName=:DEFAULT:&action=default", "edit_ldap.cgi", "show_users.cgi", "edit_configfiles.cgi", "server_status.cgi");
my @server_titles = ($text{'index_volumes_default'}, $text{'index_edit_ldap'}, $text{'index_users'}, $text{'index_edit'}, "$text{index_capabilities}");
my @server_icons = ("images/volumes.gif", "images/root.gif", "images/users.gif", "images/edit.gif", "images/server.gif");
icons_table(\@server_links, \@server_titles, \@server_icons);

print &ui_hr();

# since we are using a different number of forms, depending on the status of the service,
# we are keeping a running index while outputting the forms
my $current_formindex = 0;

# Process control Buttons
if (&find_byname($config{'afpd_d'})) {
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
