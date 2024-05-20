#!/usr/bin/perl
# Display a form for editing a file share

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
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

# This module is mostly Sven's with my overhaul additions and changed.
# I had written one as well, but liked his O-O approach to things (after
#   some tweaking).

require 'netatalk2-lib.pl';

&ReadParse();

local $page_title;

if ($in{action} =~ /create/) {
	$page_title = $text{'edit_header'};
}
elsif ($in{action} =~ /edit/) {
	$page_title = $text{'edit_file_share_title'};
}
elsif ($in{action} =~ /home/) {
	$page_title = $text{'edit_file_share_home_title'};
}
elsif ($in{action} =~ /default/) {
	$page_title = $text{'edit_file_share_default_title'};
}

getAppleVolumes();

if($in{shareName}){
	$Old_shareName = $in{shareName};
}
if($in{path}){
	$Old_path = $in{path};
}

$Options = getAllOptions($Old_shareName);
$Adouble = getAdouble($Old_shareName);
$Volsizelimit = getVolsizelimit($Old_shareName);
$AllowedHosts = getAllowedHosts($Old_shareName);
$DeniedHosts = getDeniedHosts($Old_shareName);
$CnidScheme = getCnidScheme($Old_shareName);
$CnidServer = getCnidServer($Old_shareName);
$Database = getDatabase($Old_shareName);
$Ea = getEa($Old_shareName);
$MacCharset = getMacCharset($Old_shareName);

$Allow = getAllow($Old_shareName);
while( $Allow =~ /([A-Za-z0-9@\$]+)/g) {
	if($1 =~ /^([@].*)/){
		if($1 =~ /([A-Za-z0-9\$]+)/){
			push(@allow_groups,$1);
		}
	}
	else{
		push(@allow_users,$1);
	}

}
$Deny = getDeny($Old_shareName);
while( $Deny =~ /([A-Za-z0-9@\$]+)/g) {
        if($1 =~ /^([@].*)/){
                if($1 =~ /([A-Za-z0-9\$]+)/){
                        push(@deny_groups,$1);
                }
        }
        else{
                push(@deny_users,$1);
        }
}

while( $Options =~ /\b([A-Za-z]+)\b/g) {
	if($1 eq "searchdb"){
		$searchdb=1;
	}
	elsif($1 eq "tm"){
		$tm=1;
	}
	elsif($1 eq "invisibledots"){
		$invisibledots=1;
	}
	elsif($1 eq "nonetids"){
		$nonetids=1;
	}
	elsif($1 eq "limitsize"){
		$limitsize=1;
	}
	elsif($1 eq "ro"){
		$ro=1;
	}
	elsif($1 eq "upriv"){
		$upriv=1;
	}
	elsif($1 eq "usedots"){
		$usedots=1;
	}
	elsif($1 eq "followsymlinks"){
		$followsymlinks=1;
	}
	elsif($1 eq "caseinsensitive"){
		$caseinsensitive=1;
	}
	elsif($1 eq "crlf"){
		$crlf=1;
	}
	elsif($1 eq "illegalseq"){
		$illegalseq=1;
	}
	elsif($1 eq "mswindows"){
    $mswindows=1;
  }
	elsif($1 eq "noadouble"){
		$noadouble=1;
	}
	elsif($1 eq "nocnidcache"){
	  $nocnidcache=1;
  }
	elsif($1 eq "nodev"){
    $nodev=1;
  }
	elsif($1 eq "nofileid"){
    $nofileid=1;
  }
	elsif($1 eq "nohex"){
    $nohex=1;
  }
	elsif($1 eq "prodos"){
		$prodos=1;
	}
}

$Password = getPassword($Old_shareName);
$Perm = getPerm($Old_shareName);
$FPerm = getFPerm($Old_shareName);
$DPerm = getDPerm($Old_shareName);
$Umask = getUmask($Old_shareName);

$Rolist = getRolist($Old_shareName);
while( $Rolist =~ /([A-Za-z0-9@\$]+)/g) {
        if($1 =~ /^([@].*)/){
                if($1 =~ /([A-Za-z0-9\$]+)/){
                        push(@rolist_groups,$1);
                }
        }
        else{
                push(@rolist_users,$1);
        }

}
$Rwlist = getRwlist($Old_shareName);
while( $Rwlist =~ /([A-Za-z0-9@\$]+)/g) {
        if($1 =~ /^([@].*)/){
                if($1 =~ /([A-Za-z0-9\$]+)/){
                        push(@rwlist_groups,$1);
                }
        }
        else{
                push(@rwlist_users,$1);
        }

}

$Veto = getVeto($Old_shareName);
$VolCharset = getVolCharset($Old_shareName);
$Casefold = getCasefold($Old_shareName);

my @tabs = ( [ 'basic', $text{'edit_tab_basic'} ],
             [ 'users', $text{'edit_tab_users'} ],
             [ 'advanced', $text{'edit_tab_advanced'} ]
            );

ui_print_header(undef, $page_title, "", "shares", 1);
print &ui_form_start('save_volumes.cgi', 'POST');

if ($in{action} =~ /edit|homes/) {
	print &ui_hidden('oldpath', $Old_path);
}

print &ui_tabs_start(\@tabs, 'mode', 'basic');
print &ui_tabs_start_tab('mode', 'basic');

print &ui_table_start($text{'edit_tableheader'}, 'width="100%"', 2);

if ($in{action} =~ /homes/) {
	$subpath = $1 if ($Old_path =~ /^~\/*([^\/]+.*)/);
	print &ui_hidden('ishome', 1);
	print &ui_table_row($text{'edit_homename'},
		&ui_textbox('sharename', $Old_shareName, 44, undef, undef, 'required')
	);
	print &ui_table_row($text{'index_col_title_home_path'},
		&ui_textbox('homepath', $subpath, 44)
	);
}
elsif ($in{action} =~ /create|edit/) {
	print &ui_table_row($text{'edit_sharename'},
		&ui_textbox('sharename', $Old_shareName, 44, undef, undef, 'required')
	);
	print &ui_table_row($text{'edit_sharedvolume'},
		&ui_filebox('path', $Old_path, 44, undef, undef, 'required', 1)
	);
}

print &ui_table_row($text{'edit_Adouble'},
	&ui_select('adouble_options', $Adouble, [
			['', &text('edit_default', 'v2')],
			['v1', $text{'edit_Adoublev1'}],
			['v2', $text{'edit_Adoublev2'}]
		])
);
print &ui_table_row($text{'edit_Volsizelimit'},
	"<input type=\"number\" name=volsizelimit min=\"1\" max=\"99999\" value="
	.$Volsizelimit.">\n"
);
print &ui_table_row($text{'edit_AllowedHosts'},
	&ui_textbox('allowed_hosts', $AllowedHosts, 20)
);
print &ui_table_row($text{'edit_DeniedHosts'},
	&ui_textbox('denied_hosts', $DeniedHosts, 20)
);
print &ui_table_row($text{'edit_CnidScheme'},
	&ui_textbox('cnidscheme', $CnidScheme, 10)
	." ".$text{'edit_CnidScheme_help'}
);
print &ui_table_row($text{'edit_CnidServer'},
	&ui_textbox('cnidserver', $CnidServer, 20)
);
print &ui_table_row($text{'edit_DataBase'},
	&ui_filebox('dbpath', $Database, 30, undef, undef, undef, 1)
);
print &ui_table_row($text{'edit_Ea'},
	&ui_select('ea_options', $Ea, [
			['', &text('edit_default', 'autodetect')],
			['auto', $text{'edit_Eaauto'}],
			['sys', $text{'edit_Easys'}],
			['ad', $text{'edit_Eaad'}],
			['none', $text{'edit_Eanone'}]
		])
);
print &ui_table_row($text{'edit_MacCharset'},
	&ui_select('maccharset', $MacCharset, [
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
print &ui_table_row($text{'edit_VolCharset'},
	&ui_textbox('volcharset', $VolCharset, 20)
	." ".$text{'edit_VolCharset_help'}
);
print &ui_table_row($text{'edit_Veto'},
	&ui_textbox('veto', $Veto, 20)
	." ".$text{'edit_Veto_help'}
);
print &ui_table_row($text{'edit_MisceOptions'},
	&ui_checkbox('misc_options', 'searchdb', $text{'edit_Optionssearchdb'}, $searchdb)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'tm', $text{'edit_Optionstm'}, $tm)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'limitsize', $text{'edit_Optionslimitsize'}, $limitsize)
);

print &ui_table_end();

print &ui_tabs_end_tab('mode', 'basic');
print &ui_tabs_start_tab('mode', 'users');
print &ui_table_start($text{'edit_tableheader'}, 'width="100%"', 2);

print &ui_table_row($text{'edit_Password'},
	&ui_textbox('password', $Password, 10, undef, 8)
	." ".$text{'edit_Password_help'}
);
print &ui_table_row($text{'edit_Perm'},
	&ui_textbox('perm', $Perm, 6)
);
print &ui_table_row($text{'edit_FPerm'},
	&ui_textbox('fperm', $FPerm, 6)
);
print &ui_table_row($text{'edit_DPerm'},
	&ui_textbox('dperm', $DPerm, 6)
);
print &ui_table_row($text{'edit_Umask'},
	&ui_textbox('umask', $Umask, 6)
);
print &ui_table_row($text{'edit_Allow'},
	"<table><tr>"
	."<td>$text{'edit_users'}</td>"
	."<td><input name=allow_users size=40 value="
	.join(' ', @allow_users)."> "
	.&user_chooser_button("allow_users", 1)."</td>"
	."</tr><tr>"
	."<td>$text{'edit_groups'}</td>"
	."<td><input name=allow_groups size=40 value="
	.join(' ', grep { !/^@/ } @allow_groups)."> "
	.&group_chooser_button("allow_groups", 1)."</td>"
	."</tr></table>"
);
print &ui_table_row($text{'edit_Deny'},
	"<table><tr>"
	."<td>$text{'edit_users'}</td>"
	."<td><input name=deny_users size=40 value="
	.join(' ', @deny_users)."> "
	.&user_chooser_button("deny_users", 1)."</td>"
	."</tr><tr>"
	."<td>$text{'edit_groups'}</td>"
	."<td><input name=deny_groups size=40 value="
	.join(' ', grep { !/^@/ } @deny_groups)."> "
	.&group_chooser_button("deny_groups", 1)."</td>"
	."</tr></table>"
);
print &ui_table_row($text{'edit_Rolist'},
	"<table><tr>"
	."<td>$text{'edit_users'}</td>"
	."<td><input name=rolist_users size=40 value="
	.join(' ', @rolist_users)."> "
	.&user_chooser_button("rolist_users", 1)."</td>"
	."</tr><tr>"
	."<td>$text{'edit_groups'}</td>"
	."<td><input name=rolist_groups size=40 value="
	.join(' ', grep { !/^@/ } @rolist_groups)."> "
	.&group_chooser_button("rolist_groups", 1)."</td>"
	."</tr></table>"
);
print &ui_table_row($text{'edit_Rwlist'},
	"<table><tr>"
	."<td>$text{'edit_users'}</td>"
	."<td><input name=rwlist_users size=40 value="
	.join(' ', @rwlist_users)."> "
	.&user_chooser_button("rwlist_users", 1)."</td>"
	."</tr><tr>"
	."<td>$text{'edit_groups'}</td>"
	."<td><input name=rwlist_groups size=40 value="
	.join(' ', grep { !/^@/ } @rwlist_groups)."> "
	.&group_chooser_button("rwlist_groups", 1)."</td>"
	."</tr></table>"
);

print &ui_table_end();

print &ui_tabs_end_tab('mode', 'users');
print &ui_tabs_start_tab('mode', 'advanced');

print &ui_table_start($text{'edit_tableheader'}, 'width="100%"', 2);

print &ui_table_row($text{'edit_Casefold'},
	&ui_select('casefold_options', $Casefold, [
			['', $text{'edit_Casefolddefault'}],
			['tolower', $text{'edit_Casefoldtolower'}],
			['toupper', $text{'edit_Casefoldtoupper'}],
			['xlatelower', $text{'edit_Casefoldxlatelower'}],
			['xlateupper', $text{'edit_Casefoldxlateupper'}]
		])
);
print &ui_table_row($text{'edit_MisceOptions'},
	&ui_checkbox('misc_options', 'nonetids', $text{'edit_Optionsnonetids'}, $nonetids)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'ro', $text{'edit_Optionsro'}, $ro)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'upriv', $text{'edit_Optionsupriv'}, $upriv)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'usedots', $text{'edit_Optionsusedots'}, $usedots)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'invisibledots', $text{'edit_Optionsinvisibledots'}, $invisibledots)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'followsymlinks', $text{'edit_Optionsfollowsymlinks'}, $followsymlinks)
);
print &ui_table_row($text{'edit_AdvOptions'},
	&ui_checkbox('misc_options', 'caseinsensitive', $text{'edit_Optionscaseinsensitive'}, $caseinsensitive)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'crlf', $text{'edit_Optionscrlf'}, $crlf)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'illegalseq', $text{'edit_Optionsillegalseq'}, $illegalseq)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'mswindows', $text{'edit_Optionsmswindows'}, $mswindows)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'noadouble', $text{'edit_Optionsnoadouble'}, $noadouble)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'nocnidcache', $text{'edit_Optionsnocnidcache'}, $nocnidcache)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'nodev', $text{'edit_Optionsnodev'}, $nodev)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'nofileid', $text{'edit_Optionsnofileid'}, $nofileid)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'nohex', $text{'edit_Optionsnohex'}, $nohex)
);
print &ui_table_row('',
	&ui_checkbox('misc_options', 'prodos', $text{'edit_Optionsprodos'}, $prodos)
);

print &ui_table_end();

print &ui_tabs_end_tab('mode', 'advanced');
print &ui_tabs_end();

if ($in{action} =~ /default/) {
	print &ui_hidden('default_options', 1);
}
print &ui_form_end([[undef, $text{'edit_save'}]]);

&ui_print_footer("index.cgi", $text{'index_module'});
