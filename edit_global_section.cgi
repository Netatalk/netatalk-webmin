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

# all inputs for netatalk configuration parameters follow the naming
# convention "p_"+parameter name to keep the save_global_section.cgi simple

require 'netatalk3-lib.pl';

my $afpconfRef;
my $sectionRef;
eval {
	&ReadParse();

	# read afp.conf and check parameters
	$afpconfRef = &read_afpconf();

	$sectionRef = $$afpconfRef{sectionsByName}{'Global'} || die "No Global section in afp.conf.\n";	
};
if($@) {
	# preparations failed with an error message in $@ - print error

	my $msg = $@;
	
	ui_print_header(undef, $text{'errmsg_title'}, "", "configs", 1, 1);

	print "<p>$msg<p>";
	
	ui_print_footer("index.cgi", $text{'edit_return'});
	
	exit;
}

ui_print_header(undef, $text{'edit_global_section_title'}, "", "configs", 1, 1);

print &ui_form_start('save_global_section.cgi', 'POST');

print &ui_hidden('index', $$sectionRef{'index'}) if($sectionRef);
print &ui_hidden('name', 'Global');

print &ui_table_start($text{'edit_vol_section_title_of_table'}, 'width="100%"', 2);

print &ui_table_row($text{'edit_global_section_hostname'},
	&ui_textbox('p_hostname', (get_parameter_of_section($afpconfRef, $sectionRef, 'hostname', \%in))[0])." leave empty to use the host name of machine\n"
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'afp listen', \%in);
print &ui_table_row($text{'edit_global_section_afp_listen'},
	&ui_textbox('p_afp listen', $values[0])
	." ".($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')."\n"
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'afp port', \%in);
print &ui_table_row($text{'edit_global_section_afp_port'},
	&ui_textbox('p_afp port', $values[0], 5)
	." ".($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')."\n"
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'set password', \%in);
print &ui_table_row($text{'edit_global_section_set_password'},
	&ui_radio('p_set password', $values[0], [['', 'disabled'], ['yes', 'enabled']])
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'login message', \%in);
print &ui_table_row($text{'edit_global_section_login_message'},
	&ui_textbox('p_login message', $values[0], 60)
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'uam list', \%in);
my $nonstandardUAMs = @values[0];
$nonstandardUAMs =~ s/uams_dhx2?.so|uams_clrtxt.so|uams_guest.so|uams_gss.so//g;
$nonstandardUAMs =~ s/^[ ,]+//;
$nonstandardUAMs =~ s/[ ,]+$//;
$nonstandardUAMs =~ s/[ ,]+/ /g;
@values[0] = "uams_dhx.so uams_dhx2.so" if ! @values[0];
print &ui_table_row($text{'edit_global_section_uam_list'},
	&ui_checkbox('p_uam list', 'uams_dhx2.so', 'DHX2 UAM', $values[0] =~ /uams_dhx2.so/ ? 1 : 0)
	.&ui_checkbox('p_uam list', 'uams_dhx.so', 'DHX UAM', $values[0] =~ /uams_dhx.so/ ? 1 : 0)
	.&ui_checkbox('p_uam list', 'uams_clrtxt.so', 'Cleartext UAM', $values[0] =~ /uams_clrtxt.so/ ? 1 : 0)
	.&ui_checkbox('p_uam list', 'uams_guest.so', 'Guest UAM', $values[0] =~ /uams_guest.so/ ? 1 : 0)
	.&ui_checkbox('p_uam list', 'uams_gss.so', 'Kerberos UAM', $values[0] =~ /uams_gss.so/ ? 1 : 0)
	."<br>".$text{'edit_global_section_uam_list_other'} .&ui_textbox('p_uam list', $nonstandardUAMs, 40)
);

print &ui_table_row("Kerberos keytab",
	&ui_filebox('p_k5_keytab', (get_parameter_of_section($afpconfRef, $sectionRef, 'k5 keytab', \%in))[0], 40, undef, undef, undef, 1)
);
print &ui_table_row("Kerberos service",
	&ui_textbox('p_k5 service', (get_parameter_of_section($afpconfRef, $sectionRef, 'k5 service', \%in))[0], 40)
);
print &ui_table_row("Kerberos realm",
	&ui_textbox('p_k5 realm', (get_parameter_of_section($afpconfRef, $sectionRef, 'k5 realm', \%in))[0], 40)
);
print &ui_table_row("Fully-qualified domain name",
	&ui_textbox('p_fqdn', (get_parameter_of_section($afpconfRef, $sectionRef, 'fqdn', \%in))[0], 40)
);

print &ui_table_row($text{'edit_global_section_log_file'},
	&ui_filebox('p_log_file', (get_parameter_of_section($afpconfRef, $sectionRef, 'log file', \%in))[0])." leave empty to log through syslog daemon\n"
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'log level', \%in);
print &ui_table_row($text{'edit_global_section_log_level'},
	&ui_textbox('p_log level', $values[0], 30)
	." ".($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')."\n"
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'zeroconf', \%in);
print &ui_table_row($text{'edit_global_section_zeroconf'},
	&ui_radio('p_zeroconf', $values[0], [['no', 'disabled'], ['', 'enabled']])
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'spotlight', \%in);
print &ui_table_row($text{'edit_global_section_spotlight'},
	&ui_radio('p_spotlight', $values[0], [['', 'disabled'], ['yes', 'enabled']])
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'afpstats', \%in);
print &ui_table_row($text{'edit_global_section_afpstats'},
	&ui_radio('p_afpstats', $values[0], [['', 'disabled'], ['yes', 'enabled']])
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'mimic model', \%in);
my $select = "<select name='p_mimic model'>\n"
	."<option value='' ".($values[0] eq '' ? "selected" : "").">default</option>\n"
	."<option value='AirPort' ".($values[0] =~ 'AirPort' ? "selected" : "").">AirPort</option>\n"
	."<option value='AppleTV1,1' ".($values[0] =~ 'AppleTV1,1' ? "selected" : "").">Apple TV</option>\n"
	."<option value='MacPro' ".($values[0] =~ 'MacPro' ? "selected" : "").">Mac Pro</option>\n"
	."<option value='MacBookAir' ".($values[0] =~ 'MacBookAir' ? "selected" : "").">MacBook Air</option>\n"
	."<option value='MacBookPro' ".($values[0] =~ 'MacBookPro' ? "selected" : "").">MacBook Pro</option>\n"
	."<option value='MacBook' ".($values[0] =~ 'MacBook' ? "selected" : "").">MacBook</option>\n"
	."<option value='iMac' ".($values[0] =~ 'iMac' ? "selected" : "").">iMac</option>\n"
	."<option value='Macmini' ".($values[0] =~ 'Macmini' ? "selected" : "").">Mac mini</option>\n"
	."<option value='PowerMac' ".($values[0] =~ 'PowerMac' ? "selected" : "").">Power Mac</option>\n"
	."<option value='PowerBook' ".($values[0] =~ 'PowerBook' ? "selected" : "").">PowerBook</option>\n"
	."<option value='RackMac' ".($values[0] =~ 'RackMac' ? "selected" : "").">Xserve</option>\n"
	."</select>";
print &ui_table_row($text{'edit_global_section_mimic_model'}, $select);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'vol dbpath', \%in);
print &ui_table_row($text{'edit_global_section_vol_dbpath'},
	&ui_filebox('p_vol_dbpath', $values[0], 40, undef, undef, undef, 1)
	.($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : '')
);

@values = get_parameter_of_section($afpconfRef, $sectionRef, 'vol preset', \%in);
my $select = "<select name='p_vol preset'>\n"
			."<option value='' ".($values[0] eq '' ? "selected" : "").">".($values[2] ? html_escape($values[1])." (".html_escape($values[2]).")" : 'no preset')."</option>\n";
for my $presetSectionRef (@{$$afpconfRef{volumePresetSections}}) {
	$select .= "<option value='".html_escape($$presetSectionRef{name})."' ".($values[0] eq $$presetSectionRef{name} ? "selected" : "").">".html_escape($$presetSectionRef{name})."</option>\n";	
}
$select .= "</select>";
print &ui_table_row($text{'edit_global_section_vol_preset'}, $select);

print &ui_table_end(); 
print &ui_form_end([[undef, $text{'save_button_title'}, 0, undef]]);

ui_print_footer("index.cgi", $text{'edit_return'});
