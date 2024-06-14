#!/usr/bin/perl
# Display a form for editing an existing file share

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Copyright (C) 2000 Matthew Keller <kellermg@potsdam.edu>
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

require 'netatalk2-lib.pl';

&ReadParse();

my @allServer;

my $servername = "";
my $page_title = "";
my $transport = "";
my $uamlist = "";

if ($in{action} =~ /create/) {
	$page_title = $text{'create_server_header'};

  # Netatalk default options defined here
	$transport = "-transall";
	$uamlist = "uams_dhx.so,uams_dhx2.so";
}
elsif ($in{action} =~ /edit/) {
	@allServer = getAfpdServers();
	$page_title = $text{'edit_server_header'};

	$servername = $allServer[$in{index}]{servername};
	$transport = $allServer[$in{index}]{transport};
	$uamlist = $allServer[$in{index}]{uamlist};
}
else {
	die("Unknown action type. Are you trying something naughty?")
}

my @tabs = ( [ 'basic', $text{'edit_tab_basic'} ],
             [ 'users', $text{'edit_tab_users'} ],
             [ 'transport', $text{'edit_tab_transport'} ],
             [ 'advanced', $text{'edit_tab_advanced'} ]
            );

&ui_print_header(undef, $page_title, "", "servers", 1);

print &ui_form_start('save_servers.cgi', 'POST');

print &ui_tabs_start(\@tabs, 'mode', 'basic');
print &ui_tabs_start_tab('mode', 'basic');

print &ui_table_start($text{'create_server_tableheader'}, 'width="100%"', 2);
print &ui_table_row($text{'create_server_ServerName'},
	&ui_textbox('servername', $servername, 30)
	." ".$text{'create_server_localhost'}
);
print &ui_table_row($text{'create_server_transport'},
	&ui_checkbox('transport_ddp', 'ddp', 'AppleTalk', $transport =~ /-transall*|-ddp*/ ? 1 : 0)
	.&ui_checkbox('transport_tcp', 'tcp', 'TCP/IP', $transport =~ /-transall*|-tcp*/ ? 1 : 0)
);
print &ui_table_row($text{'create_server_uams'},
	&ui_checkbox('uamlist', 'uams_dhx2.so', 'DHX2', $uamlist =~ /uams_dhx2.so/ ? 1 : 0)
	.&ui_checkbox('uamlist', 'uams_dhx.so', 'DHX', $uamlist =~ /uams_dhx.so/ ? 1 : 0)
	.&ui_checkbox('uamlist', 'uams_randnum.so', 'RandNum', $uamlist =~ /uams_randnum.so/ ? 1 : 0)
	.&ui_checkbox('uamlist', 'uams_clrtxt.so', 'ClearText', $uamlist =~ /uams_clrtxt.so/ ? 1 : 0)
	.&ui_checkbox('uamlist', 'uams_guest.so', 'Guest', $uamlist =~ /uams_guest.so/ ? 1 : 0)
	.&ui_checkbox('uamlist', 'uams_gss.so', 'Kerberos', $uamlist =~ /uams_gss.so/ ? 1 : 0)
);
print &ui_table_row($text{'create_server_setpass'},
	&ui_select('setpassword', @allServer ? $allServer[$in{index}]{setpassword} : '', [
			['', &text('edit_default', 'no')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);
print &ui_table_row($text{'create_server_savepass'},
	&ui_select('savepassword', @allServer ? $allServer[$in{index}]{savepassword} : '', [
			['', &text('edit_default', 'yes')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);
print &ui_table_row($text{'create_server_icon'},
	&ui_select('icon', @allServer ? $allServer[$in{index}]{icon} : '', [
			['', &text('edit_default', 'no')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);
print &ui_table_row($text{'create_server_mimicmodel'},
	&ui_textbox('mimicmodel', @allServer ? $allServer[$in{index}]{mimicmodel} : '', 40)
	." ".$text{'create_server_mimicmodel_help'}
);
print &ui_table_row($text{'create_server_loginmesg'},
	&ui_textbox('loginmesg', @allServer ? $allServer[$in{index}]{loginmesg} : '', 60)
);
print &ui_table_row($text{'create_server_maccodepage'},
	&ui_select('maccodepage', @allServer ? $allServer[$in{index}]{maccodepage} : '', [
			['', &text('edit_default', 'MAC_ROMAN')],
			['MAC_CENTRALEUROPE'],
			['MAC_CHINESE_SIMP'],
			['MAC_CHINESE_TRAD'],
			['MAC_CYRILLIC'],
			['MAC_GREEK'],
			['MAC_HEBREW'],
			['MAC_JAPANESE'],
			['MAC_KOREAN'],
			['MAC_ROMAN'],
			['MAC_TURKISH']
		])
);
print &ui_table_row($text{'create_server_unixcodepage'},
	&ui_textbox('unixcodepage', @allServer ? $allServer[$in{index}]{unixcodepage} : '', 20)
	." ".$text{'create_server_unixcodepage_help'}
);
print &ui_table_row($text{'create_server_defaultvol'},
	&ui_filebox('defaultvol', @allServer ? $allServer[$in{index}]{defaultvol} : '', 40)
);
print &ui_table_row($text{'create_server_systemvol'},
	&ui_filebox('systemvol', @allServer ? $allServer[$in{index}]{systemvol} : '', 40)
);
print &ui_table_row($text{'create_server_uservol'},
	&ui_select('uservol', @allServer ? $allServer[$in{index}]{uservol} : '', [
			['', &text('edit_default', 'yes')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);
print &ui_table_row($text{'create_server_uservolfirst'},
	&ui_select('uservolfirst', @allServer ? $allServer[$in{index}]{uservolfirst} : '', [
			['', &text('edit_default', 'no')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);

print &ui_table_end();

print &ui_tabs_end_tab('mode', 'basic');
print &ui_tabs_start_tab('mode', 'users');

print &ui_table_start($text{'create_server_tableheader'}, 'width="100%"', 2);
print &ui_table_row($text{'create_server_uampath'},
	&ui_filebox('uampath', @allServer ? $allServer[$in{index}]{uampath} : '', 40, undef, undef, 1)
);
print &ui_table_row($text{'create_server_passwdfile'},
	&ui_filebox('passwdfile', @allServer ? $allServer[$in{index}]{passwdfile} : '', 40)
);
print &ui_table_row($text{'create_server_k5keytab'},
	&ui_filebox('k5keytab', @allServer ? $allServer[$in{index}]{k5keytab} : '', 40)
);
print &ui_table_row($text{'create_server_k5service'},
	&ui_textbox('k5service', @allServer ? $allServer[$in{index}]{k5service} : '', 20)
);
print &ui_table_row($text{'create_server_k5realm'},
	&ui_textbox('k5realm', @allServer ? $allServer[$in{index}]{k5realm} : '', 20)
);
print &ui_table_row($text{'create_server_ntdomain'},
	&ui_textbox('ntdomain', @allServer ? $allServer[$in{index}]{ntdomain} : '', 20)
);
print &ui_table_row($text{'create_server_ntseparator'},
	&ui_textbox('ntseparator', @allServer ? $allServer[$in{index}]{ntseparator} : '', 20)
);
print &ui_table_row($text{'create_server_adminauthuser'},
	&ui_user_textbox('adminauthuser', @allServer ? $allServer[$in{index}]{adminauthuser} : '', 20)
);
print &ui_table_row($text{'create_server_admingroup'},
	&ui_group_textbox('admingroup', @allServer ? $allServer[$in{index}]{admingroup} : '')
);
print &ui_table_row($text{'create_server_guestname'},
	&ui_user_textbox('guestname', @allServer ? $allServer[$in{index}]{guestname} : '')
	." ".$text{'create_server_guestname_help'}
);
print &ui_table_end();

print &ui_tabs_end_tab('mode', 'users');
print &ui_tabs_start_tab('mode', 'transport');

print &ui_table_start($text{'create_server_tableheader'}, 'width="100%"', 2);
print &ui_table_row($text{'create_server_Address'},
	&ui_textbox('ipaddr', @allServer ? $allServer[$in{index}]{ipaddr} : '')
	." ".$text{'create_server_Address_help'}
);
print &ui_table_row($text{'create_server_Port'},
	'<input type="number" name="port" min="0" max="65535" value="'
	.(@allServer ? $allServer[$in{index}]{port} : '').'">'
	." ".$text{'create_server_Port_help'}
);
print &ui_table_row($text{'create_server_ddpaddr'},
	&ui_textbox('ddpaddr', @allServer ? $allServer[$in{index}]{ddpaddr} : '')
);
print &ui_table_row($text{'create_server_fqdn'},
	&ui_textbox('fqdn', @allServer ? $allServer[$in{index}]{fqdn} : '')
);
print &ui_table_row($text{'create_server_hostname'},
	&ui_textbox('hostname', @allServer ? $allServer[$in{index}]{hostname} : '')
);
print &ui_table_row($text{'create_server_server_quantum'},
	&ui_textbox('server_quantum', @allServer ? $allServer[$in{index}]{server_quantum} : '')
	." ".$text{'create_server_server_quantum_help'}
);
print &ui_table_row($text{'create_server_dsireadbuf'},
	&ui_textbox('dsireadbuf', @allServer ? $allServer[$in{index}]{dsireadbuf} : '')
	." ".$text{'create_server_dsireadbuf_help'}
);
print &ui_table_row($text{'create_server_tcprcvbuf'},
	&ui_textbox('tcprcvbuf', @allServer ? $allServer[$in{index}]{tcprcvbuf} : '')
);
print &ui_table_row($text{'create_server_tcpsndbuf'},
	&ui_textbox('tcpsndbuf', @allServer ? $allServer[$in{index}]{tcpsndbuf} : '')
);
print &ui_table_row($text{'edit_MisceOptions'},
	&ui_checkbox(
		'advertise_ssh',
		1,
		$text{'create_server_advertise_ssh'},
		@allServer ? $allServer[$in{index}]{advertise_ssh} : 0
	)
);
print &ui_table_row('',
	&ui_checkbox(
		'proxy',
		1,
		$text{'create_server_proxy'},
		@allServer ? $allServer[$in{index}]{proxy} : 0
	)
);
print &ui_table_row('',
	&ui_checkbox(
		'nozeroconf',
		1,
		$text{'create_server_nozeroconf'},
		@allServer ? $allServer[$in{index}]{nozeroconf} : 0
	)
);
print &ui_table_row('',
	&ui_checkbox(
		'slp',
		1,
		$text{'create_server_slp'},
		@allServer ? $allServer[$in{index}]{slp} : 0
	)
);
print &ui_table_end();

print &ui_tabs_end_tab('mode', 'transport');
print &ui_tabs_start_tab('mode', 'advanced');

print &ui_table_start($text{'create_server_tableheader'}, 'width="100%"', 2);

print &ui_table_row($text{'create_server_authprintdir'},
	&ui_filebox('authprintdir', @allServer ? $allServer[$in{index}]{authprintdir} : '', 40, undef, undef, 1)
);
print &ui_table_row($text{'create_server_cnidserver'},
	&ui_textbox('cnidserver', @allServer ? $allServer[$in{index}]{cnidserver} : '')
	." ".$text{'create_server_cnidserver_help'}
);
print &ui_table_row($text{'create_server_dircachesize'},
		'<input type="number" name="dircachesize" min="0" max="131072" value="'
		.(@allServer ? $allServer[$in{index}]{dircachesize} : '').'">'
		." ".$text{'create_server_dircachesize_help'}
);
print &ui_table_row($text{'create_server_fcelistener'},
	&ui_textbox('fcelistener', @allServer ? $allServer[$in{index}]{fcelistener} : '')
	." ".$text{'create_server_fcelistener_help'}
);
print &ui_table_row($text{'create_server_fceevents'},
	&ui_textbox('fceevents', @allServer ? $allServer[$in{index}]{fceevents} : '')
	." ".$text{'create_server_fceevents_help'}
);
print &ui_table_row($text{'create_server_fcecoalesce'},
	&ui_select('fcecoalesce', @allServer ? $allServer[$in{index}]{fcecoalesce} : '', [
			['', ''],
			['all'],
			['delete'],
			['create']
		])
);
print &ui_table_row($text{'create_server_fceholdfmod'},
		'<input type="number" name="fceholdfmod" min="0" max="" value="'
		.(@allServer ? $allServer[$in{index}]{fceholdfmod} : '').'">'
		." ".$text{'create_server_fceholdfmod_help'}
);
print &ui_table_row($text{'create_server_sleep'},
		'<input type="number" name="sleep" min="0" max="" value="'
		.(@allServer ? $allServer[$in{index}]{sleep} : '').'">'
		." ".$text{'create_server_sleep_help'}
);
print &ui_table_row($text{'create_server_signature'},
	&ui_textbox('signature', @allServer ? $allServer[$in{index}]{signature} : '', undef, undef, 16)
);
print &ui_table_row($text{'create_server_volnamelen'},
		'<input type="number" name="volnamelen" min="0" max="" value="'
		.(@allServer ? $allServer[$in{index}]{volnamelen} : '').'">'
);
print &ui_table_row($text{'create_server_setuplog'},
	&ui_textbox('setuplog', @allServer ? $allServer[$in{index}]{setuplog} : '', 40)
	." ".$text{'create_server_setuplog_help'}
);
print &ui_table_row($text{'create_server_unsetuplog'},
	&ui_textbox('unsetuplog', @allServer ? $allServer[$in{index}]{unsetuplog} : '', 40)
	." ".$text{'create_server_unsetuplog_help'}
);
print &ui_table_row($text{'create_server_tickleval'},
		'<input type="number" name="tickleval" min="0" max="" value="'
		.(@allServer ? $allServer[$in{index}]{tickleval} : '').'">'
		." ".$text{'create_server_tickleval_help'}
);
print &ui_table_row($text{'create_server_timeout'},
		'<input type="number" name="timeout" min="0" max="" value="'
		.(@allServer ? $allServer[$in{index}]{timeout} : '').'">'
		." ".$text{'create_server_timeout_help'}
);
print &ui_table_row($text{'edit_MisceOptions'},
	&ui_checkbox(
		'closevol',
		1,
		$text{'create_server_closevol'},
		@allServer ? $allServer[$in{index}]{closevol} : 0
	)
);
print &ui_table_row('',
	&ui_checkbox(
		'keepsessions',
		1,
		$text{'create_server_keepsessions'},
		@allServer ? $allServer[$in{index}]{keepsessions} : 0
	)
);
print &ui_table_row('',
	&ui_checkbox(
		'noacl2maccess',
		1,
		$text{'create_server_noacl2maccess'},
		@allServer ? $allServer[$in{index}]{noacl2maccess} : 0
	)
);
print &ui_table_end();

print &ui_tabs_end_tab('mode', 'advanced');
print &ui_tabs_end();

if ($in{action} =~ /edit/) {
	print &ui_hidden('old_servername', $servername eq "" ? "-" : $servername);
}
print &ui_form_end([[undef, $text{'edit_save'}]]);

&ui_print_footer("index.cgi", $text{'index_module'});
