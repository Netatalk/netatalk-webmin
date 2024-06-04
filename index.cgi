#!/usr/bin/perl
#
#    Netatalk Webmin Module
#    Copyright (C) 2000 Matthew Keller <kellermg@potsdam.edu>
#    Copyright (C) 2000 Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
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

my @Shares = getAppleVolumes();
my @Servers = getAfpdServers();
my @shares_to_list;
my $home_found;

# since we are using a different number of forms, depending on the status of the service,
# we are keeping a running index while outputting the forms
my $current_formindex = 0;

foreach $s (@Shares) {
	$path = getPath($s);
	if (getPath($s) =~ /^~/) {
		if ($home_found) {
			showMessage($text{error_dup_home});
			exit;
		}
		$home_found = $s;
	}
	elsif (getShareName($s) ne ":DEFAULT:") {
		push (@shares_to_list, $s);
	}
}

print "<h3>$text{index_volumes_title}</h3>\n";
my @volume_links = ( "<a href=\"edit_volumes.cgi?action=create\">$text{'index_create_file_share'}</a>" );

# Print AFP volumes
if (@shares_to_list) {
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
	foreach $s (@shares_to_list) {
		my $sharename = getShareName($s);
		my $path = getPath($s);
		my $options = getAllOptions($s);
		print &ui_columns_row([
			&ui_checkbox('section_index', $path),
			'<a href="edit_volumes.cgi?shareName='.html_escape($sharename)
			.'&path='.$path.'&action=edit">'.html_escape($sharename).'</a>',
			$path,
			$options ne '' ? $options : $text{'index_value_not_set'}
		], [ "width='20'" ]);
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

# Homes
print "<h3>$text{index_homes}</h3>\n";
if($home_found) {
	my $sharename = getShareName($home_found);
	my $path = getPath($home_found);
	my $options = getAllOptions($home_found);
	my $subpath;

	$subpath = $1 if ($path =~ /^~\/*([^\/]+.*)/);

	print &ui_form_start('delete_volumes.cgi?homepath='.html_escape($path), 'post', undef, "id='homes'");
	print &ui_columns_start( [
	  $text{'edit_homename'},
		$text{'index_col_title_home_path'},
		$text{'index_options'},
	] );
	print &ui_columns_row( [
  	$sharename ne '' ? '<a href="edit_volumes.cgi?shareName='.html_escape($sharename)
	  .'&path='.html_escape($path).'&action=homes">'.html_escape($sharename).'</a>' : $text{'index_value_not_set'},
		$subpath ne '' ? html_escape($subpath) : $text{'index_value_not_set'},
		$options ne '' ? html_escape($options) : $text{'index_value_not_set'},
	] );
	print &ui_columns_end();
	print &ui_form_end([[undef, $text{'index_delete_homes_button_title'}, 0, undef]]);
	$current_formindex += 1;
} else {
	print "<p><b>$text{'index_no_homes'}</b></p>\n";
	print &ui_links_row( ["<a href=\"edit_volumes.cgi?action=new_homes\">$text{'index_create_homes_link_name'}</a>"] );
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
		print &ui_columns_row([
			&ui_checkbox('section_index', $s->{servername} eq "" ? "-" : $s->{servername}),
			"<a href=\"edit_servers.cgi?action=edit&offset=".$offset."\">"
			.($s->{servername} ? $s->{servername} : &get_system_hostname())."</a>",
			$t ne '' ? $t : $text{'index_value_not_set'},
			$s->{uamlist} ne '' ? $s->{uamlist} : $text{'index_value_not_set'},
			$s->{port} ne '' ? $s->{port} : $text{'index_value_not_set'},
			$s->{ipaddr} ne '' ? $s->{ipaddr} : $text{'index_value_not_set'},
			$s->{maccodepage} ne '' ? $s->{maccodepage} : $text{'index_value_not_set'}
		], [ "width='20'" ]);
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

my @server_links = (
	"edit_volumes.cgi?shareName=:DEFAULT:&action=default",
	"edit_ldap.cgi",
	"show_users.cgi",
	"edit_configfiles_form.cgi",
	"server_status.cgi"
);
my @server_titles = (
	$text{'index_volumes_default'},
	$text{'index_edit_ldap'},
	$text{'index_users'},
	$text{'index_edit'},
	$text{'index_capabilities'}
);
my @server_icons = (
	"images/server.gif",
	"images/keys.gif",
	"images/users.gif",
	"images/edit.gif",
	"images/inspect.gif"
);
icons_table(\@server_links, \@server_titles, \@server_icons);

print &ui_hr();

# Process control Buttons
if (&find_byname($config{'afpd_d'})) {
	print "<h3>$text{'index_running_services'}</h3>\n";
	print &ui_buttons_start();
	print &ui_buttons_row(
		'control.cgi?action=restart&daemon=netatalk',
		$text{'running_restart'},
		$text{'index_process_control_restart'}
	);
	print &ui_buttons_row(
		'control.cgi?action=stop&daemon=netatalk',
		$text{'running_stop'},
		$text{'index_process_control_stop'}
	);
	print &ui_buttons_end();
	$current_formindex += 2;
} else {
	print "<h3>$text{'index_not_running_services'}</h3>\n";
	print &ui_buttons_start();
	print &ui_buttons_row(
		'control.cgi?action=start&daemon=netatalk',
		$text{'running_start'},
		$text{'index_process_control_start'}
	);
	print &ui_buttons_end();
	$current_formindex += 1;
}

# Show process control buttons for AppleTalk services
# only if atalkd init commands are defined.
# This allows for a clean UI on platforms that has a single init script
# such as OpenRC (Gentoo, Alpine, etc.) or Solaris.
if ($config{'start_atalkd'} && $config{'stop_atalkd'} && $config{'restart_atalkd'}) {

	my @daemons = (
		{atalkd => 'AppleTalk network manager'},
		{papd => 'Print server'},
		{timelord => 'Time server'},
		{a2boot => 'Apple II netboot server'}
	);

	print "<h3>$text{'index_appletalk_services'}</h3>\n";
	print "<p>$text{'index_appletalk_services_notice'}</p>";

	foreach my $daemon (@daemons) {
		foreach my $d (keys %$daemon) {
		if (-x $config{$d.'_d'}) {
			if (&find_byname($config{$d.'_d'})) {
				print "<h3>".&text('index_running_service', $daemon->{$d})."</h3>\n";
				print &ui_buttons_start();
				print &ui_buttons_row(
					'control.cgi?action=restart&daemon='.$d,
					&text('running_restart_daemon', $daemon->{$d}),
					&text('index_process_control_restart_daemon', $d)
				);
				print &ui_buttons_row(
					'control.cgi?action=stop&daemon='.$d,
					&text('running_stop_daemon', $daemon->{$d}),
					&text('index_process_control_stop_daemon', $d)
				);
				print &ui_buttons_end();
				$current_formindex += 2;
			} else {
				print "<h3>".&text('index_not_running', $daemon->{$d})."</h3>\n";
				print &ui_buttons_start();
				print &ui_buttons_row(
					'control.cgi?action=start&daemon='.$d,
					&text('running_start_daemon', $daemon->{$d}),
					&text('index_process_control_start_daemon', $d)
				);
				print &ui_buttons_end();
				$current_formindex += 1;
			}
		}
		else {
			print "<p>".&text('index_daemon_not_found', $d)."</p>";
		}
	}
	}
}

### END of index.cgi ###.
