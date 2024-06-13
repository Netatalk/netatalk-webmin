#!/usr/bin/perl
#
# Netatalk Webmin Module
# Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

require 'netatalk3-lib.pl';

ui_print_header(&text('index_version', version()), $text{'index_title'}, "", "configs", 1, 1);

# check if netatalk daemon's path is configured correctly, if not: print error then exit
if(!-x $config{'netatalk_d'}) {
	print &text('index_ever', "<tt>$config{'netatalk_d'}</tt>", "/config.cgi?$module_name");
	exit;
}

# try to read and interpret afp.conf - if this doesn't work, print error and footer then exit
my $afpconf;
eval {
	$afpconf = &read_afpconf();
};
if($@) {
	print $@;
	exit;
}

# Volumes
print "<h3>$text{index_volumes}</h3>\n";
my @volume_links = ( "<a href=\"edit_vol_section.cgi?action=new_volume\">$text{'index_create_volume_link_name'}</a>" );
if(@{$$afpconf{volumeSections}}) {
	unshift @volume_links, (
		&select_all_link('section_index', $current_formindex),
		&select_invert_link('section_index', $current_formindex)
	) if(@{$$afpconf{volumeSections}} > 1);
	print &ui_form_start('delete_sections.cgi', 'post', undef, "id='volumes'");
	print &ui_columns_start( [
			'',
			$text{'index_col_title_vol_name'},
			$text{'index_col_title_path'},
			$text{'index_col_title_uses_preset'}
		], undef, 0, undef, undef
	);
	foreach $volumeSection (@{$$afpconf{volumeSections}}) {
		print &ui_columns_row( [
				&ui_checkbox('section_index', $$volumeSection{'index'}),
				"<a href=\"edit_vol_section.cgi?action=edit_volume&index=$$volumeSection{'index'}\"><b>$$volumeSection{name}</b></a>",
				$$volumeSection{parameters}{'path'}{value},
				$$volumeSection{parameters}{'vol preset'}{value}
		], [ "width='20'" ]);
	}
	print &ui_columns_end();
	print &ui_links_row(\@volume_links);
	print &ui_form_end([[undef, $text{'index_delete_volumes_button_title'}, 0, undef]]);
	$current_formindex += 1;
} else {
	print "<b>$text{'index_no_volumes'}</b>\n";
	print "<p>\n";
	print &ui_links_row(\@volume_links);
}
print &ui_hr();

# Volume presets
print "<h3>$text{index_volume_presets}</h3>\n";
my @volume_preset_links = ( "<a href=\"edit_vol_section.cgi?action=new_volume_preset\">$text{'index_create_volume_preset_link_name'}</a>" );
if(@{$$afpconf{volumePresetSections}}) {
	# for an explanation of the following links, see above
	unshift @volume_preset_links, (
		&select_all_link('section_index', $current_formindex),
		&select_invert_link('section_index', $current_formindex)
	) if(@{$$afpconf{volumePresetSections}} > 1);
	print &ui_form_start('delete_sections.cgi', 'post', undef, "id='volume_presets'");
	print &ui_columns_start( [
			'',
			$text{'index_col_title_preset_name'},
			$text{'index_col_title_used_by'}
		], undef, 0, undef, undef
	);
	foreach $volumeSection (@{$$afpconf{volumePresetSections}}) {
		print &ui_columns_row( [
				&ui_checkbox('section_index', $$volumeSection{'index'}),
				"<a href=\"edit_vol_section.cgi?action=edit_volume_preset&index=$$volumeSection{'index'}\"><b>$$volumeSection{name}</b></a>",
				defined $$volumeSection{presetUsedBySectionNames} ? join("<br>", @{$$volumeSection{presetUsedBySectionNames}}) : ""
		], [ "width='20'" ]);
	}
	print &ui_columns_end();
	print &ui_links_row(\@volume_preset_links);
	print &ui_form_end([[undef, $text{'index_delete_volume_presets_button_title'}, 0, undef]]);
	$current_formindex += 1;
} else {
	print "<b>$text{'index_no_volume_presets'}</b>\n";
	print "<p>\n";
	print &ui_links_row(\@volume_preset_links);
}
print &ui_hr();

# Homes
print "<h3>$text{index_homes}</h3>\n";
if($$afpconf{sectionsByName}{'Homes'}) {
	print &ui_form_start('delete_sections.cgi', 'post', undef, "id='homes'");
	print &ui_columns_start( [
		$text{'index_col_title_basedir_regex'},
		$text{'index_col_title_home_path'},
		$text{'index_col_title_home_name'},
	] );
	my $volumeSection = $$afpconf{sectionsByName}{'Homes'};
	my @basedir_regex = get_parameter_of_section($afpconf, $volumeSection, 'basedir regex');
	my @path = get_parameter_of_section($afpconf, $volumeSection, 'path');
	my @home_name = get_parameter_of_section($afpconf, $volumeSection, 'home name');
	print &ui_columns_row( [
		"<input type='hidden' name='section_index' value='$$volumeSection{'index'}'>".
		"<a href=\"edit_vol_section.cgi?action=edit_homes&index=$$volumeSection{'index'}\"><b>".($basedir_regex[0] ne '' ? html_escape($basedir_regex[0]) : $text{'index_value_not_set'})."</b></a>",
		$path[0] ne '' ? html_escape($path[0]) : $text{'index_value_not_set'},
		$home_name[0] ne '' ? html_escape($home_name[0]) : $text{'index_value_not_set'},
	] );
	print &ui_columns_end();
	print &ui_form_end([[undef, $text{'index_delete_homes_button_title'}, 0, undef]]);
} else {
	print "<b>$text{'index_no_homes'}</b>\n";
	print "<p>\n";
	print &ui_links_row( ["<a href=\"edit_vol_section.cgi?action=new_homes\">$text{'index_create_homes_link_name'}</a>"] );
}
print &ui_hr();

print"<h3>$text{index_global}</h3>\n";

my @links = ("edit_global_section.cgi", "show_users.cgi", "server_status.cgi");
my @titles = ($text{'index_icon_text_server'}, $text{'index_icon_text_users'}, "$text{index_icon_text_capabilities}");
my @icons = ("images/server.gif", "images/users.gif", "images/inspect.gif");
icons_table(\@links, \@titles, \@icons, 5);

print &ui_hr();

# since we are using a different number of forms, depending on the status of the service,
# we are keeping a running index while outputting the forms
my $current_formindex = 0;

# Process control Buttons
if(&find_byname($config{'netatalk_d'})) {
    print "<h3>$text{'index_running_services'}</h3>\n";
	print &ui_buttons_start();
	print &ui_buttons_row(
		'restart.cgi',
		$text{'running_restart'},
		&text('index_process_control_restart_txt', $config{restart_netatalk})
	);
	print &ui_buttons_row(
		'stop.cgi',
		$text{'running_stop'},
		&text('index_process_control_stop_txt', $config{stop_netatalk})
	);
	print &ui_buttons_end();
	$current_formindex += 2;
} else {
    print "<h3>$text{'index_not_running_services'}</h3>\n";
	print &ui_buttons_start();
	print &ui_buttons_row(
		'start.cgi',
		$text{'running_start'},
		&text('index_process_control_start_txt', $config{start_netatalk})
	);
	print &ui_buttons_end();
	$current_formindex += 1;
}
