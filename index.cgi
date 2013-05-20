#!/usr/bin/perl
#
# Netatalk Webmin Module
# Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list
# of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOTOC LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

require './netatalk3-lib.pl';

&header($text{'index_title'}, "", undef, 1, 1, undef, "<a href=\"help/configs.cgi\">$text{help_configs}</a>");

# check if netatalk daemon's path is configured correctly, if not: print error and footer then exit
if(!-x $config{'netatalk_d'}) {
	print &text('index_ever',"<tt>$config{'netatalk_d'}</tt>", "/config.cgi?$module_name");
	print "<p>\n<hr>\n";
	&footer("/", $text{'index'});
	exit;
}

print "<hr>\n";

# since we are using a different number of forms, depending on the status of the service,
# we are keeping a running index while outputting the forms
my $current_formindex = 0;

# Process control Buttons
if(&find_byname($config{'netatalk_d'})) {
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

# now try to read and interpret afp.conf - if this doesn't work, print error and footer then exit
my $afpconf;
eval {
	$afpconf = &read_afpconf();
};
if($@) {
	print $@;
	exit;
}

# Volumes	
print "<p>\n";
print "<h3>$text{index_volumes}</h3>\n";
print "<p>\n";
my @volume_links = ( "<a href=\"edit_vol_section.cgi?action=new_volume\">$text{'index_create_volume_link_name'}</a>" );
if(@{$$afpconf{volumeSections}}) {
	unshift @volume_links, (
		&select_all_link('section_index', $current_formindex),
		&select_invert_link('section_index', $current_formindex)
	) if(@{$$afpconf{volumeSections}} > 1);
	print &ui_links_row(\@volume_links);
	print &ui_form_start('delete_sections.cgi', 'post', undef, "id='volumes'");
	print &ui_columns_start( [
			'',
			$text{'index_col_title_vol_name'},
			$text{'index_col_title_path'},
			$text{'index_col_title_uses_preset'}
		], undef, 0, undef, undef
	);
	foreach $volumeSection (@{$$afpconf{volumeSections}}) {
		print &ui_checked_columns_row( [
				"<a href=\"edit_vol_section.cgi?action=edit_volume&index=$$volumeSection{'index'}\"><b>$$volumeSection{name}</b></a>",
				$$volumeSection{parameters}{'path'}{value},
				$$volumeSection{parameters}{'vol preset'}{value}
		], [ "width='20'" ], 'section_index', $$volumeSection{'index'});
	}
	print &ui_columns_end();
	print &ui_form_end([[undef, $text{'index_delete_volumes_button_title'}, 0, undef]]);
	print &ui_links_row(\@volume_links);
	$current_formindex += 1;
} else {
	print "<b>$text{'index_no_volumes'}</b>\n";
	print "<p>\n";
	print &ui_links_row(\@volume_links);
}
print &ui_hr();

# Volume presets	
print "<p>\n";
print "<h3>$text{index_volume_presets}</h3>\n";
print "<p>\n";
my @volume_preset_links = ( "<a href=\"edit_vol_section.cgi?action=new_volume_preset\">$text{'index_create_volume_preset_link_name'}</a>" );
if(@{$$afpconf{volumePresetSections}}) {
	# for an explanation of the following links, see above
	unshift @volume_preset_links, (
		&select_all_link('section_index', $current_formindex),
		&select_invert_link('section_index', $current_formindex)
	) if(@{$$afpconf{volumePresetSections}} > 1);
	print &ui_links_row(\@volume_preset_links);
	print &ui_form_start('delete_sections.cgi', 'post', undef, "id='volume_presets'");
	print &ui_columns_start( [
			'',
			$text{'index_col_title_preset_name'},
			$text{'index_col_title_used_by'}
		], undef, 0, undef, undef
	);
	foreach $volumeSection (@{$$afpconf{volumePresetSections}}) {
		print &ui_checked_columns_row( [
				"<a href=\"edit_vol_section.cgi?action=edit_volume_preset&index=$$volumeSection{'index'}\"><b>$$volumeSection{name}</b></a>",
				defined $$volumeSection{presetUsedBySectionNames} ? join("<br>", @{$$volumeSection{presetUsedBySectionNames}}) : ""
		], [ "width='20'" ], 'section_index', $$volumeSection{'index'});
	}
	print &ui_columns_end();
	print &ui_form_end([[undef, $text{'index_delete_volume_presets_button_title'}, 0, undef]]);
	print &ui_links_row(\@volume_preset_links);
	$current_formindex += 1;
} else {
	print "<b>$text{'index_no_volume_presets'}</b>\n";
	print "<p>\n";
	print &ui_links_row(\@volume_preset_links);
}
print &ui_hr();

# Homes	
print "<p>\n";
print "<h3>$text{index_homes}</h3>\n";
print "<p>\n";
if($$afpconf{sectionsByName}{'Homes'}) {
	print &ui_form_start('delete_sections.cgi', 'post', undef, "id='homes'");
	print &ui_columns_start( [
		$text{'index_col_title_basedir_regex'},
		$text{'index_col_title_home_path'},
		$text{'index_col_title_home_name'},
		$text{'index_col_title_uses_preset'}
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
		html_escape((get_parameter_of_section($afpconf, $volumeSection, 'vol preset'))[0])
	] );
	print &ui_columns_end();	
	print &ui_form_end([[undef, $text{'index_delete_homes_button_title'}, 0, undef]]);
} else {
	print "<b>$text{'index_no_homes'}</b>\n";
	print "<p>\n";
	print &ui_links_row( ["<a href=\"edit_vol_section.cgi?action=new_homes\">$text{'index_create_homes_link_name'}</a>"] );
}
print &ui_hr();

print"<p>\n";
print"<h3>$text{index_global}</h3>\n";
print"<p>\n";

my @links = ("edit_global_section.cgi", "show_users.cgi");
my @titles = ($text{'index_icon_text_server'}, $text{'index_icon_text_users'});
my @icons = ("images/server.png", "images/users.png");
icons_table(\@links, \@titles, \@icons, 5);
print"<br>\n";

print"<hr>\n";

&footer("/right.cgi?open=system&auto=status&open=updates", $text{'index_root'});
