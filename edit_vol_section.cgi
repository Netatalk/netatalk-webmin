#!/usr/bin/perl
#
# Netatalk Webmin Module
# Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
# Copyright (C) 2023-4 Daniel Markstedt <daniel@mindani.net>
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

# parameters:
#   action = new_volume, new_volume_preset, new_homes, edit_volume, edit_volume_preset, edit_homes
#   [index = index of related section in sectionsByIndex - only given if action=edit_...]
#   [baseOnIndex = index of section in sectionsByIndex to base this new volume or volume preset on]
#   [reload = true - if set, then values of inputs are read from the %in-Hash]

# all inputs for netatalk configuration parameters follow the naming convention "p_"+parameter name to keep the save_vol_section.cgi simple

require 'netatalk3-lib.pl';

my $subject; # what it is, we are going to edit: volume | volume_preset | homes
my $pageTitle = $text{'errmsg_title'};
my $afpconfRef;
my $sectionRef;
eval {
	&ReadParse();

	# read afp.conf and check parameters
	$afpconfRef = &read_afpconf();
	
	unless($in{'action'} =~ /^(new|edit)_(volume|volume_preset|homes)$/) {
		die &text('errmsg_parameter_error', 'action')."\n";
	}
	$subject = $2;
	$pageTitle = $text{"edit_vol_section_title_$in{'action'}"};
	
	unless(($in{'action'} =~ /^edit/ && $in{'index'} =~ /\d+/ && $$afpconfRef{sectionsByIndex}[$in{'index'}]) || ($in{'action'} =~ /^new/ && !$in{'index'})) {
		die &text('errmsg_parameter_error', 'index')."\n";
	}	
	
	if($in{'baseOnIndex'} && !($in{'action'} =~ /^new/ && $in{'baseOnIndex'} =~ /\d+/ && $$afpconfRef{sectionsByIndex}[$in{'baseOnIndex'}])) {
		die &text('errmsg_parameter_error', 'baseOnIndex')."\n";
	}
	
	if(defined $in{'index'}) {
		$sectionRef = $$afpconfRef{sectionsByIndex}[$in{'index'}];
	} elsif(defined $in{'baseOnIndex'}) {
		$sectionRef = $$afpconfRef{sectionsByIndex}[$in{'baseOnIndex'}];
	}
	
	# rejoin parameters that have been split for the user interface (as users and groups are handled in different lists within the UI, whereas they are combined in afp.conf)
	if($in{'reload'}) {
		$in{'p_valid users'} = join_users_and_groups(defined $in{'pu_valid_users'} ? $in{'pu_valid_users'} : '', defined $in{'pg_valid_users'} ? $in{'pg_valid_users'} : '');
		$in{'p_invalid users'} = join_users_and_groups(defined $in{'pu_invalid_users'} ? $in{'pu_invalid_users'} : '', defined $in{'pg_invalid_users'} ? $in{'pg_invalid_users'} : '');
		$in{'p_rolist'} = join_users_and_groups(defined $in{'pu_rolist'} ? $in{'pu_rolist'} : '', defined $in{'pg_rolist'} ? $in{'pg_rolist'} : '');
		$in{'p_rwlist'} = join_users_and_groups(defined $in{'pu_rwlist'} ? $in{'pu_rwlist'} : '', defined $in{'pg_rwlist'} ? $in{'pg_rwlist'} : '');
	}
};
if($@) {
	# preparations failed with an error message in $@ - print error

	my $msg = $@;
	
	ui_print_header(undef, $pageTitle, "", "configs", 1, 1);

	print "<p>$msg<p>";
	
	ui_print_footer("index.cgi", $text{'edit_return'});
	
	exit;
}


my @tabs = ( [ 'common', $text{'edit_vol_section_tab_common'} ],
             [ 'users', $text{'edit_vol_section_tab_users'} ]
            );

if($subject ne 'homes') {
	push @tabs, [ 'advanced', $text{'edit_vol_section_tab_advanced'} ];
}

# preparations done, start outputting page
ui_print_header(undef, $pageTitle, "", "configs", 1, 1);

print &ui_form_start('save_vol_section.cgi', 'POST', undef, 'name="configform"');

print &ui_hidden('action', $in{'action'});
print &ui_hidden('reload', 'true');
print &ui_hidden('index', $in{'index'}) if(defined $in{'index'});

print &ui_tabs_start(\@tabs, 'mode', 'common');
print &ui_tabs_start_tab('mode', 'common');

print &ui_table_start($text{'edit_vol_section_title_of_table'}, 'width="100%"', 2);

if($subject eq 'volume') {
	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'vol preset', \%in);
	my $select = "<select name='p_vol preset' onchange='document.configform.action=\"edit_vol_section.cgi\"; document.configform.submit();'>\n"
				."<option value='' ".($values[0] eq '' ? "selected" : "").">".($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : 'no preset')."</option>\n";
	for my $presetSectionRef (@{$$afpconfRef{volumePresetSections}}) {
		$select .= "<option value='".html_escape($$presetSectionRef{name})."' ".($values[0] eq $$presetSectionRef{name} ? "selected" : "").">".html_escape($$presetSectionRef{name})."</option>\n";	
	}
	$select .= "</select>";
	print &ui_table_row($text{'edit_vol_section_vol_preset'}, $select);
}

if($subject eq 'homes') {
	print &ui_hidden('name', 'Homes');
	print &ui_table_row($text{'edit_vol_section_home_name'}, &ui_textbox('p_home name', (get_parameter_of_section($afpconfRef, $sectionRef, 'home name', \%in))[0], 40));
	print &ui_table_row($text{'edit_vol_section_basedir_regex'}, &ui_textbox('p_basedir regex', (get_parameter_of_section($afpconfRef, $sectionRef, 'basedir regex', \%in))[0], 40, undef, undef, "required"));
	print &ui_table_row($text{'edit_vol_section_home_path'}, &ui_textbox('p_path', (get_parameter_of_section($afpconfRef, $sectionRef, 'path', \%in))[0], 40));
}
else {
	print &ui_table_row($text{'edit_vol_section_name'}, &ui_textbox('name', exists $in{name} ? $in{name} : ($sectionRef ? $$sectionRef{name} : ''), 40, undef, undef, "required"));
}

if($subject eq 'volume') {
	print &ui_table_row($text{'edit_vol_section_path'},
		&ui_filebox('p_path', exists $in{p_path} ? $in{p_path} : (exists $$sectionRef{parameters}{'path'} ? $$sectionRef{parameters}{'path'}{value} : ''), 40, undef, undef, "required", 1) .
		"<br /><a href=\"/filemin\" target=\"_blank\">$text{'edit_vol_section_path_note'}</a>"
	);
}

if($subject ne 'homes') {
	print &ui_table_row($text{'edit_vol_section_time_machine'}, build_select($afpconfRef, $sectionRef, \%in, 'time machine', 'leave undefined', 'yes', 'yes', 'no', 'no'));

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'vol size limit', \%in);
	print &ui_table_row($text{'edit_vol_section_vol_size_limit'},
		"<input name='p_vol size limit' type='number' value='".$values[0]."'>"
		." ".$text{edit_vol_section_vol_size_limit_help}
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'password', \%in);
	print &ui_table_row($text{'edit_vol_section_password'},
		&ui_textbox('p_password', $values[0], 10, undef, 8)
		.($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')
	);
}

print &ui_table_row($text{'edit_vol_section_ea'}, build_select($afpconfRef, $sectionRef, \%in, 'ea', 'leave undefined', 'none', 'none', 'auto', 'auto', 'sys', 'sys - use filesystem meta data', 'ad', 'ad - use .AppleDouble directories'));
print &ui_table_row($text{'edit_vol_section_read_only'}, build_select($afpconfRef, $sectionRef, \%in, 'read only', 'leave undefined', 'yes', 'yes', 'no', 'no'));
print &ui_table_row($text{'edit_vol_section_search_db'}, build_select($afpconfRef, $sectionRef, \%in, 'search db', 'leave undefined', 'yes', 'yes', 'no', 'no'));

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'login message', \%in);
print &ui_table_row($text{'edit_global_section_login_message'},
	&ui_textbox('p_login message', $values[0], 60)
);

print &ui_table_end();
print &ui_tabs_end_tab('mode', 'common');

print &ui_tabs_start_tab('mode', 'users');
print &ui_table_start($text{'edit_vol_section_title_of_table'}, 'width="100%"', 2);

print &ui_table_row($text{'edit_vol_section_unix_priv'}, build_select($afpconfRef, $sectionRef, \%in, 'unix priv', 'leave undefined', 'yes', 'yes', 'no', 'no'));
my @file_perm_values = get_parameter_of_section($afpconfRef, $sectionRef, 'file perm', \%in);
my @dir_perm_values = get_parameter_of_section($afpconfRef, $sectionRef, 'directory perm', \%in);
my @umask_values = get_parameter_of_section($afpconfRef, $sectionRef, 'directory perm', \%in);
print &ui_table_row('',
	"<i>$text{'edit_vol_section_unix_permissions_note'}</i><br>"
	."<b>$text{'edit_vol_section_file_perm'}</b> ".&ui_textbox('p_file perm', $file_perm_values[0])."<i>".($file_perm_values[2] ? html_escape($file_perm_values[1])." (".html_escape($file_perm_values[2]).")" : '')."</i><br>"
	."<b>$text{'edit_vol_section_directory_perm'}</b> ".&ui_textbox('p_directory perm', $dir_perm_values[0])."<i>".($dir_perm_values[2] ? html_escape($dir_perm_values[1])." (".html_escape($dir_perm_values[2]).")" : '')."</i><br>"
	."<b>$text{'edit_vol_section_umask'}</b> ".&ui_textbox('p_umask', $umask_values[0])."<i>".($umask_values[2] ? html_escape($umask_values[1])." (".html_escape($umask_values[2]).")" : '')."</i>"
);

print &ui_table_row($text{'edit_vol_section_valid_users'}, build_user_group_selection($afpconfRef, $sectionRef, \%in, 'valid users'));
print &ui_table_row($text{'edit_vol_section_invalid_users'}, build_user_group_selection($afpconfRef, $sectionRef, \%in, 'invalid users'));
print &ui_table_row($text{'edit_vol_section_rolist'}, build_user_group_selection($afpconfRef, $sectionRef, \%in, 'rolist'));
print &ui_table_row($text{'edit_vol_section_rwlist'}, build_user_group_selection($afpconfRef, $sectionRef, \%in, 'rwlist'));

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'hosts allow', \%in);
print &ui_table_row($text{'edit_vol_section_hosts_allow'},
	&ui_textbox('p_hosts allow', $values[0], 120)
	.($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'hosts deny', \%in);
print &ui_table_row($text{'edit_vol_section_hosts_deny'},
	&ui_textbox('p_hosts deny', $values[0], 120)
	.($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')
);

print &ui_table_end();
print &ui_tabs_end_tab('mode', 'users');

if($subject ne 'homes') {
	print &ui_tabs_start_tab('mode', 'advanced');
	print &ui_table_start($text{'edit_vol_section_title_of_table'}, 'width="100%"', 2);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'chmod request', \%in);
	print &ui_table_row($text{'edit_global_section_chmod_request'},
		&ui_radio('p_chmod request', $values[0], [['', 'preserve (default)'], ['ignore', 'ignore'], ['simple', 'simple']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'cnid server', \%in);
	print &ui_table_row($text{'edit_global_section_cnid_server'},
		&ui_textbox('p_cnid server', $values[0], 40)
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'force xattr with sticky bit', \%in);
	print &ui_table_row($text{'edit_global_section_force_xattr_with_sticky_bit'},
		&ui_radio('p_force xattr with sticky bit', $values[0], [['', 'disabled'], ['yes', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'ignored attributes', \%in);
	print &ui_table_row($text{'edit_global_section_ignored_attributes'},
		&ui_radio('p_ignored attributes', $values[0], [['', 'none (default)'], ['all', 'all'], ['nowrite', 'nowrite'], ['nodelete', 'nodelete'], ['norename', 'norename']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'spotlight', \%in);
	print &ui_table_row($text{'edit_global_section_spotlight'},
		&ui_radio('p_spotlight', $values[0], [['', 'disabled'], ['yes', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'vol dbpath', \%in);
	print &ui_table_row($text{'edit_global_section_vol_dbpath'},
		&ui_filebox('p_vol_dbpath', $values[0], 40, undef, undef, undef, 1)
		.($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'appledouble', \%in);
	print &ui_table_row($text{'edit_vol_section_appledouble'},
		&ui_radio('p_appledouble', $values[0], [['', 'ea (default)'], ['yes', 'v2']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'cnid scheme', \%in);
	print &ui_table_row($text{'edit_vol_section_cnid_scheme'},
		&ui_radio('p_cnid_scheme', $values[0], [['', 'dbd (default)'], ['last', 'last'], ['mysql', 'mysql']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'casefold', \%in);
	print &ui_table_row($text{'edit_vol_section_casefold'},
		&ui_radio('p_casefold', $values[0], [['', 'none (default)'], ['tolower', 'tolower'], ['toupper', 'toupper'], ['xlatelower', 'xlatelower'], ['xlateupper', 'xlateupper']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'preexec', \%in);
	print &ui_table_row($text{'edit_vol_section_preexec'},
		&ui_textbox('p_preexec', $values[0], 60)
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'postexec', \%in);
	print &ui_table_row($text{'edit_vol_section_postexec'},
		&ui_textbox('p_postexec', $values[0], 60)
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'veto files', \%in);
	print &ui_table_row($text{'edit_vol_section_veto_files'},
		&ui_textbox('p_veto files', $values[0], 60)
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'acls', \%in);
	print &ui_table_row($text{'edit_vol_section_acls'},
		&ui_radio('p_acls', $values[0], [['no', 'disabled'], ['', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'case sensitive', \%in);
	print &ui_table_row($text{'edit_vol_section_case_sensitive'},
		&ui_radio('p_case sensitive', $values[0], [['no', 'disabled'], ['', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'cnid dev', \%in);
	print &ui_table_row($text{'edit_vol_section_cnid_dev'},
		&ui_radio('p_cnid dev', $values[0], [['no', 'disabled'], ['', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'convert appledouble', \%in);
	print &ui_table_row($text{'edit_vol_section_convert_appledouble'},
		&ui_radio('p_convert appledouble', $values[0], [['no', 'disabled'], ['', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'delete veto files', \%in);
	print &ui_table_row($text{'edit_vol_section_delete_veto_files'},
		&ui_radio('p_delete veto files', $values[0], [['', 'disabled'], ['yes', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'follow symlinks', \%in);
	print &ui_table_row($text{'edit_vol_section_follow_symlinks'},
		&ui_radio('p_follow symlinks', $values[0], [['', 'disabled'], ['yes', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'invisible dots', \%in);
	print &ui_table_row($text{'edit_vol_section_invisible_dots'},
		&ui_radio('p_invisible dots', $values[0], [['', 'disabled'], ['yes', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'network ids', \%in);
	print &ui_table_row($text{'edit_vol_section_network_ids'},
		&ui_radio('p_network ids', $values[0], [['no', 'disabled'], ['', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'preexec close', \%in);
	print &ui_table_row($text{'edit_vol_section_preexec_close'},
		&ui_radio('p_preexec close', $values[0], [['', 'disabled'], ['yes', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'stat vol', \%in);
	print &ui_table_row($text{'edit_vol_section_stat_vol'},
		&ui_radio('p_stat vol', $values[0], [['', 'disabled'], ['yes', 'enabled']])
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'mac charset', \%in);
	print &ui_table_row($text{'edit_global_section_mac_charset'},
		&ui_textbox('p_mac charset', $values[0], 10)
		." ".($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')."\n"
	);

	@values = get_parameter_of_section($afpconfRef, $sectionRef, 'vol charset', \%in);
	print &ui_table_row($text{'edit_global_section_vol_charset'},
		&ui_textbox('p_vol charset', $values[0], 10)
		.$text{edit_global_section_vol_charset_help}
	);

	print &ui_table_end();
	print &ui_tabs_end_tab('mode', 'advanced');
}
print &ui_tabs_end();

print &ui_form_end([[undef, $text{'save_button_title'}, 0, undef]]);

ui_print_footer("index.cgi", $text{'edit_return'});

sub build_select {
	my $afpconfRef = shift;
	my $sectionRef = shift;
	my $inRef = shift;
	my $parameterName = shift;
	my $textIfNoDefault = shift;

	my @values = get_parameter_of_section($afpconfRef, $sectionRef, $parameterName, $inRef);

	my $select = "<select name='p_$parameterName'>\n";
	if(defined $textIfNoDefault) {
		$select .= "<option value='' ".($values[0] eq '' ? "selected" : "").">".($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : $textIfNoDefault)."</option>\n";	
	}

	while(@_) {
		my $value = shift;
		my $userVisibleValue = shift;
		$select .= "<option value='$value' ".($values[0] eq $value ? "selected" : "").">$userVisibleValue</option>\n";	
	}

	return $select."</select>\n";
}

sub build_user_group_selection {
	my $afpconfRef = shift;
	my $sectionRef = shift;
	my $inRef = shift;
	my $parameterName = shift;
	
	my $parameterNameUnderscored = $parameterName; $parameterNameUnderscored =~ s/ /_/g;
	
	my @values = get_parameter_of_section($afpconfRef, $sectionRef, $parameterName, $inRef);
	my $result = "<table><tr><td align=left>$text{'edit_users'}</td><td align=left>\n";
	$result .= sprintf("<input name='pu_$parameterNameUnderscored' size=40 value=\"%s\"> %s %s</td></tr>\n",
		join(' ',  html_escape(((split_into_users_and_groups($values[0]))[0]))),
		&user_chooser_button("pu_$parameterNameUnderscored", 1),
		$values[2] ? html_escape(((split_into_users_and_groups($values[1]))[0]))." (".html_escape($values[2]).")" : '');
	$result .= "<tr><td align=right>$text{'edit_groups'}</td><td align=left>\n";
	$result .= sprintf("<input name='pg_$parameterNameUnderscored' size=40 value=\"%s\"> %s %s</td></tr>\n",
		join(' ',  html_escape(((split_into_users_and_groups($values[0]))[1]))),
		&user_chooser_button("pg_$parameterNameUnderscored", 1),
		$values[2] ? html_escape(((split_into_users_and_groups($values[1]))[1]))." (".html_escape($values[2]).")" : '');
	$result .= "</table>\n";
	
	return $result;
}
