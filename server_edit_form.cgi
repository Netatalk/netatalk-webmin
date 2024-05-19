#!/usr/bin/perl
# Display a form for editing an existing file share

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Copyright (C) 2023-4 by Daniel Markstedt <daniel@mindani.net>
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

@allServer = getAllAfpd();

local $servername = "";
local $page_title = "";

if ($in{action} =~ /create/) {
	$page_title = $text{'create_server_header'};

  # Netatalk default options defined here
	$transport = "-transall";
	$uamlist = "uams_dhx.so,uams_dhx2.so";
}
elsif ($in{action} =~ /edit/) {
	if ($in{offset}) {
		$offset = $in{offset};
	}
	else {
		$offset = 0;
	}
	$page_title = $text{'edit_server_header'};

	$servername = $allServer[$offset]{servername};
	$transport = $allServer[$offset]{transport};
	$port = $allServer[$offset]{port};
	$address = $allServer[$offset]{ipaddr};
	$loginmsg = $allServer[$offset]{loginmsg};
	$savepass = $allServer[$offset]{savepassword};
	$setpass = $allServer[$offset]{setpassword};
	$uamlist = $allServer[$offset]{uamlist};
	$icon = $allServer[$offset]{icon};
	$mimicmodel = $allServer[$offset]{mimicmodel};
	$setuplog = $allServer[$offset]{setuplog};
	$maccodepage = $allServer[$offset]{maccodepage};
	$unixcodepage = $allServer[$offset]{unixcodepage};
	$defaultvol = $allServer[$offset]{defaultvol};
	$systemvol = $allServer[$offset]{systemvol};
	$uservol = $allServer[$offset]{uservol};
	$uservolfirst = $allServer[$offset]{uservolfirst};
	$uampath = $allServer[$offset]{uampath};
	$k5keytab = $allServer[$offset]{k5keytab};
	$k5service = $allServer[$offset]{k5service};
	$k5realm = $allServer[$offset]{k5realm};
	$ntdomain = $allServer[$offset]{ntdomain};
	$ntseparator = $allServer[$offset]{ntseparator};
	$adminauthuser = $allServer[$offset]{adminauthuser};
	$passwdfile = $allServer[$offset]{passwdfile};
	$advertise_ssh = $allServer[$offset]{advertise_ssh};
	$proxy = $allServer[$offset]{proxy};
	$zeroconf = $allServer[$offset]{zeroconf};
	$slp = $allServer[$offset]{slp};
}
else {
	die("Unknown action type. Are you trying something naughty?")
}

my @tabs = ( [ 'basic', $text{'edit_tab_basic'} ],
             [ 'users', $text{'edit_tab_users'} ],
             [ 'transport', $text{'edit_tab_transport'} ],
             [ 'misc', $text{'edit_tab_misc'} ],
             [ 'advanced', $text{'edit_tab_advanced'} ]
            );

&ui_print_header(undef, $page_title, "", "servers", 1);

print &ui_form_start('server_save_action.cgi', 'POST');

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
	&ui_checkbox('uams', 'uams_dhx2.so', 'DHX2', $uamlist =~ /uams_dhx2.so/ ? 1 : 0)
	.&ui_checkbox('uams', 'uams_dhx.so', 'DHX', $uamlist =~ /uams_dhx.so/ ? 1 : 0)
	.&ui_checkbox('uams', 'uams_randnum.so', 'RandNum', $uamlist =~ /uams_randnum.so/ ? 1 : 0)
	.&ui_checkbox('uams', 'uams_clrtxt.so', 'ClearText', $uamlist =~ /uams_clrtxt.so/ ? 1 : 0)
	.&ui_checkbox('uams', 'uams_guest.so', 'Guest', $uamlist =~ /uams_guest.so/ ? 1 : 0)
	.&ui_checkbox('uams', 'uams_gss.so', 'Kerberos', $uamlist =~ /uams_gss.so/ ? 1 : 0)
);
print &ui_table_row($text{'create_server_setpass'},
	&ui_select('setpassword', $setpass, [
			['', &text('edit_default', 'no')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);
print &ui_table_row($text{'create_server_savepass'},
	&ui_select('savepassword', $savepass, [
			['', &text('edit_default', 'yes')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);
print &ui_table_row($text{'create_server_lgmesg'},
	&ui_textbox('logmesg', $loginmsg, 60)
);
print &ui_table_row($text{'create_server_icon'},
	&ui_select('icon', $icon, [
			['', &text('edit_default', 'no')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);
print &ui_table_row($text{'create_server_mimicmodel'},
	&ui_textbox('mimicmodel', $mimicmodel, 40)
	." ".$text{'create_server_mimicmodel_help'}
);
print &ui_table_row($text{'create_server_setuplog'},
	&ui_textbox('setuplog', $setuplog, 40)
	." ".$text{'create_server_setuplog_help'}
);
print &ui_table_row($text{'create_server_maccodepage'},
	&ui_select('maccodepage', $maccodepage, [
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
	&ui_textbox('unixcodepage', $unixcodepage, 20)
	." ".$text{'create_server_unixcodepage_help'}
);
print &ui_table_row($text{'create_server_defaultvol'},
	&ui_filebox('defaultvol', $defaultvol, 40)
);
print &ui_table_row($text{'create_server_systemvol'},
	&ui_filebox('systemvol', $systemvol, 40)
);
print &ui_table_row($text{'create_server_uservol'},
	&ui_select('uservol', $uservol, [
			['', &text('edit_default', 'yes')],
			['yes', $text{'global_yes'}],
			['no', $text{'global_no'}]
		])
);
print &ui_table_row($text{'create_server_uservolfirst'},
	&ui_select('uservolfirst', $uservolfirst, [
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
	&ui_filebox('uampath', $uampath, 40)
);
print &ui_table_row($text{'create_server_passwdfile'},
	&ui_filebox('passwdfile', $passwdfile, 40)
);
print &ui_table_row($text{'create_server_k5keytab'},
	&ui_filebox('k5keytab', $k5keytab, 40)
);
print &ui_table_row($text{'create_server_k5service'},
	&ui_textbox('k5service', $k5service, 20)
);
print &ui_table_row($text{'create_server_k5realm'},
	&ui_textbox('k5realm', $k5realm, 20)
);
print &ui_table_row($text{'create_server_ntdomain'},
	&ui_textbox('ntdomain', $ntdomain, 20)
);
print &ui_table_row($text{'create_server_ntseparator'},
	&ui_textbox('ntseparator', $ntseparator, 20)
);
print &ui_table_row($text{'create_server_adminauthuser'},
	&ui_user_textbox('adminauthuser', $adminauthuser, 20)
);
print &ui_table_end();

print &ui_tabs_end_tab('mode', 'users');
print &ui_tabs_start_tab('mode', 'transport');

print &ui_table_start($text{'create_server_tableheader'}, 'width="100%"', 2);
print &ui_table_row($text{'create_server_Address'},
	&ui_textbox('address', $address)
	." ".$text{'create_server_Address_help'}
);
print &ui_table_row($text{'create_server_Port'},
	'<input type="number" name="port" min="0" max="65535" value="'.$port.'">'
	." ".$text{'create_server_Port_help'}
);
print &ui_table_row($text{'create_server_ddpaddr'},
	&ui_textbox('ddpaddr', $ddpaddr)
);
print &ui_table_row($text{'create_server_fqdn'},
	&ui_textbox('fqdn', $fqdn)
);
print &ui_table_row($text{'create_server_hostname'},
	&ui_textbox('hostname', $hostname)
);
print &ui_table_row($text{'create_server_server_quantum'},
	&ui_textbox('server_quantum', $server_quantum)
	." ".$text{'create_server_server_quantum_help'}
);
print &ui_table_row($text{'create_server_dsireadbuf'},
	&ui_textbox('dsireadbuf', $dsireadbuf)
	." ".$text{'create_server_dsireadbuf_help'}
);
print &ui_table_row($text{'create_server_tcprcvbuf'},
	&ui_textbox('tcprcvbuf', $tcprcvbuf)
);
print &ui_table_row($text{'create_server_tcpsndbuf'},
	&ui_textbox('tcpsndbuf', $tcpsndbuf)
);
print &ui_table_row($text{'edit_MisceOptions'},
	&ui_checkbox('advertise_ssh', 1, $text{'create_server_advertise_ssh'}, $advertise_ssh)
);
print &ui_table_row('',
	&ui_checkbox('proxy', 1, $text{'create_server_proxy'}, $proxy)
);
print &ui_table_row('',
	&ui_checkbox('zeroconf', 1, $text{'create_server_zeroconf'}, $zeroconf)
);
print &ui_table_row('',
	&ui_checkbox('slp', 1, $text{'create_server_slp'}, $slp)
);
print &ui_table_end();

print &ui_tabs_end_tab('mode', 'transport');
print &ui_tabs_start_tab('mode', 'misc');

print &ui_table_start($text{'create_server_tableheader'}, 'width="100%"', 2);
print &ui_table_end();

print &ui_tabs_end_tab('mode', 'misc');
print &ui_tabs_start_tab('mode', 'advanced');

print &ui_table_start($text{'create_server_tableheader'}, 'width="100%"', 2);
print &ui_table_end();

print &ui_tabs_end_tab('mode', 'advanced');
print &ui_tabs_end();

if ($in{action} =~ /edit/) {
	print &ui_hidden('old_servername', $servername eq "" ? "-" : $servername);
}
print &ui_form_end([[undef, $text{'edit_save'}]]);

if ($in{action} =~ /edit/) {
	print &ui_form_start('server_delete_action.cgi', 'POST');
	print &ui_hidden('delete_servername', $servername eq "" ? "-" : $servername);
	print &ui_form_end([[undef, $text{'edit_delete'}, ]]);
}

&ui_print_footer("index.cgi", $text{'index_module'});
