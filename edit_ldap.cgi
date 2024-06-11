#!/usr/bin/perl
# Display a form for editing an existing file share

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Copyright (C) 2000 Matthew Keller <kellermg@potsdam.edu>
#    Copyright (C) 2024 Daniel Markstedt <daniel@mindani.net>
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

require 'netatalk2-lib.pl';

&ReadParse();

local %ldap = getAfpdLdap();

&ui_print_header(undef, $text{'index_edit_ldap'}, "", "ldap", 1);

print &ui_form_start('save_ldap.cgi', 'POST');

print &ui_table_start($text{'edit_ldap_table_heading'}, 'width="100%"', 2);
print &ui_table_row($text{'edit_ldap_uri'},
	&ui_textbox('ldap_uri', $ldap{ldap_uri})
	." ".$text{'edit_ldap_uri_help'}
);
print &ui_table_row($text{'edit_ldap_auth_method'},
	&ui_select('ldap_auth_method', $ldap{ldap_auth_method}, [
			['none'],
			['simple']
		])
);
print &ui_table_row($text{'edit_ldap_auth_dn'},
	&ui_textbox('ldap_auth_dn', $ldap{ldap_auth_dn})
);
print &ui_table_row($text{'edit_ldap_auth_pw'},
	&ui_textbox('ldap_auth_pw', $ldap{ldap_auth_pw})
);
print &ui_table_row($text{'edit_ldap_userbase'},
	&ui_textbox('ldap_userbase', $ldap{ldap_userbase})
);
print &ui_table_row($text{'edit_ldap_userscope'},
	&ui_select('ldap_userscope', $ldap{ldap_userscope}, [
			['base'],
			['one'],
			['sub']
		])
);
print &ui_table_row($text{'edit_ldap_groupbase'},
	&ui_textbox('ldap_groupbase', $ldap{ldap_groupbase})
);
print &ui_table_row($text{'edit_ldap_groupscope'},
	&ui_select('ldap_groupscope', $ldap{ldap_groupscope}, [
			['base'],
			['one'],
			['sub']
		])
);
print &ui_table_row($text{'edit_ldap_uuid_attr'},
	&ui_textbox('ldap_uuid_attr', $ldap{ldap_uuid_attr})
);
print &ui_table_row($text{'edit_ldap_name_attr'},
	&ui_textbox('ldap_name_attr', $ldap{ldap_name_attr})
);
print &ui_table_row($text{'edit_ldap_group_attr'},
	&ui_textbox('ldap_group_attr', $ldap{ldap_group_attr})
);
print &ui_table_end();

print &ui_form_end([[undef, $text{'edit_save'}]]);

&ui_print_footer("index.cgi", $text{'index_module'});
