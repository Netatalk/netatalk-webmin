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
	$savepass = "-savepassword";
	$setpass = "-nosetpassword";
	$icon = "-noicon";
	$uamlist = "uams_dhx2.so";
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
}
else {
	die("Unknown action type. Are you trying something naughty?")
}

&ui_print_header(undef, $page_title, "", "servers", 1);

print &ui_form_start('server_save_action.cgi', 'POST');
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
print &ui_table_row($text{'create_server_Address'},
	&ui_textbox('address', $address)
	." ".$text{'create_server_Address_help'}
);
print &ui_table_row($text{'create_server_Port'},
	'<input type="number" name="port" min="0" max="65535" value="'.$port.'">'
	." ".$text{'create_server_Port_help'}
);
print &ui_table_row($text{'create_server_setpass'},
	&ui_yesno_radio('setpassword', $setpass, '-setpassword', '-nosetpassword')
);
print &ui_table_row($text{'create_server_pass'},
	&ui_yesno_radio('savepassword', $savepass, '-savepassword', '-nosavepassword')
);
print &ui_table_row($text{'create_server_lgmesg'},
	&ui_textbox('logmesg', $loginmsg, 60)
);
print &ui_table_row($text{'create_server_icon'},
	&ui_yesno_radio('icon', $icon, '-icon', '-noicon')
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
	'<select name="maccodepage">'
	.'<option value="">'.$text{'edit_default'}.'</option>'
	.'<option value="MAC_CENTRALEUROPE" '
	.($maccodepage =~ /MAC_CENTRALEUROPE/ ? 'selected' : '')
	.'>MAC_CENTRALEUROPE'.'</option>'
	.'<option value="MAC_CHINESE_SIMP" '
	.($maccodepage =~ /MAC_CHINESE_SIMP/ ? 'selected' : '')
	.'>MAC_CHINESE_SIMP'.'</option>'
	.'<option value="MAC_CHINESE_TRAD" '
	.($maccodepage =~ /MAC_CHINESE_TRAD/ ? 'selected' : '')
	.'>MAC_CHINESE_TRAD'.'</option>'
	.'<option value="MAC_CYRILLIC" '
	.($maccodepage =~ /MAC_CYRILLIC/ ? 'selected' : '')
	.'>MAC_CYRILLIC'.'</option>'
	.'<option value="MAC_GREEK" '
	.($maccodepage =~ /MAC_GREEK/ ? 'selected' : '')
	.'>MAC_GREEK'.'</option>'
	.'<option value="MAC_HEBREW" '
	.($maccodepage =~ /MAC_HEBREW/ ? 'selected' : '')
	.'>MAC_HEBREW'.'</option>'
	.'<option value="MAC_JAPANESE" '
	.($maccodepage =~ /MAC_JAPANESE/ ? 'selected' : '')
	.'>MAC_JAPANESE'.'</option>'
	.'<option value="MAC_KOREAN" '
	.($maccodepage =~ /MAC_KOREAN/ ? 'selected' : '')
	.'>MAC_KOREAN'.'</option>'
	.'<option value="MAC_ROMAN" '
	.($maccodepage =~ /MAC_ROMAN/ ? 'selected' : '')
	.'>MAC_ROMAN'.'</option>'
	.'<option value="MAC_TURKISH" '
	.($maccodepage =~ /MAC_TURKISH/ ? 'selected' : '')
	.'>MAC_TURKISH'.'</option>'
	.'</select>'
	." ".$text{'create_server_maccodepage_help'}
);

print &ui_table_end();
print "<div><i>$text{'create_server_notice'}</i></div>";
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
