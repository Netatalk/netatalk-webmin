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

if ($in{action} =~ /create/) {
	ui_print_header(undef, $text{'edit_header'}, "", "shares", 1);
}
elsif ($in{action} =~ /edit/) {
	ui_print_header(undef, $text{'edit_file_share_title'}, "", "shares", 1);
}

open_afile();

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

print &ui_form_start('fshare_save_action.cgi', 'POST');

if ($in{action} =~ /edit/) {
	print "<input type=\"hidden\" name=\"oldpath\" value=\"$Old_path\">\n";
}

print &ui_tabs_start(\@tabs, 'mode', 'basic');
print &ui_tabs_start_tab('mode', 'basic');

print &ui_table_start($text{'edit_tableheader'}, 'width="100%"', 2);
print &ui_table_row($text{'edit_sharename'},
	&ui_textbox('share', $Old_shareName, 44, undef, undef, 'required')
);
print &ui_table_row($text{'edit_sharedvolume'},
	"<input type=radio name=homes value=0 "
	.(($Old_path ne "~" && $Old_path ne "~/") ? "checked" : "").">"
	.$text{'edit_directory'}."<input name=path size=30 value="
	.(($Old_path ne "~" && $Old_path ne "~/") ? $Old_path: "").">"
	.&file_chooser_button("path", 1)
	."<a href=\"/filemin\" target=\"_blank\">".$text{'edit_filemanager_link'}
	."</a><br><input type=radio name=homes value=1 "
	.(($Old_path eq "~" || $Old_path eq "~/") ? "checked" : "").">"
	.$text{'edit_homedirectory'}."<br>"
);
print &ui_table_row($text{'edit_Adouble'},
	'<select name="adouble_options">'
	.'<option value="">'.$text{'edit_default'}.'</option>'
	.'<option value="v1" '
	.($Ea =~ /v1/ ? 'selected' : '')
	.'>'.$text{'edit_Adoublev1'}.'</option>'
	.'<option value="v2" '
	.($Ea =~ /v2/ ? 'selected' : '')
	.'>'.$text{'edit_Adoublev2'}.'</option>'
	.'</select>'
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
	&ui_filebox('dbpath', $Database, 30)
);
print &ui_table_row($text{'edit_Ea'},
	'<select name="ea_options">'
	.'<option value="">'.$text{'edit_default'}.'</option>'
	.'<option value="auto" '
	.($Ea =~ /auto/ ? 'selected' : '')
	.'>'.$text{'edit_Eaauto'}.'</option>'
	.'<option value="sys" '
	.($Ea =~ /sys/ ? 'selected' : '')
	.'>'.$text{'edit_Easys'}.'</option>'
	.'<option value="ad" '
	.($Ea =~ /ad/ ? 'selected' : '')
	.'>'.$text{'edit_Eaad'}.'</option>'
	.'<option value="none" '
	.($Ea =~ /none/ ? 'selected' : '')
	.'>'.$text{'edit_Eanone'}.'</option>'
	.'</select>'
);
print &ui_table_row($text{'edit_MacCharset'},
	'<select name="maccharset">'
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
print &ui_table_row($text{'edit_VolCharset'},
	&ui_textbox('volcharset', $VolCharset, 20)
	." ".$text{'edit_VolCharset_help'}
);
print &ui_table_row($text{'edit_Veto'},
	&ui_textbox('veto', $Veto, 20)
	." ".$text{'edit_Veto_help'}
);
print &ui_table_row($text{'edit_MisceOptions'},
	"<input type=checkbox name=misc_options ".($searchdb eq "1" ? "checked" : "")." value=searchdb>$text{'edit_Optionssearchdb'} <br>\n"
	."<input type=checkbox name=misc_options ".($tm eq "1" ? "checked" : "")." value=tm>$text{'edit_Optionstm'}<br>\n"
	."<input type=checkbox name=misc_options ".($nonetids eq "1" ? "checked" : "")." value=nonetids>$text{'edit_Optionsnonetids'}<br>\n"
	."<input type=checkbox name=misc_options ".($limitsize eq "1" ? "checked" : "")." value=limitsize>$text{'edit_Optionslimitsize'}<br>\n"
	."<input type=checkbox name=misc_options ".($ro eq "1" ? "checked" : "")." value=ro>$text{'edit_Optionsro'}<br>\n"
	."<input type=checkbox name=misc_options ".($upriv eq "1" ? "checked" : "")." value=upriv>$text{'edit_Optionsupriv'}<br>\n"
	."<input type=checkbox name=misc_options ".($usedots eq "1" ? "checked" : "")." value=usedots>$text{'edit_Optionsusedots'}<br>\n"
	."<input type=checkbox name=misc_options ".($invisibledots eq "1" ? "checked" : "")." value=invisibledots>$text{'edit_Optionsinvisibledots'}<br>\n"
	."<input type=checkbox name=misc_options ".($limitsize eq "1" ? "checked" : "")." value=followsymlinks>$text{'edit_Optionsfollowsymlinks'}<br>\n"
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
	'<select name="casefold_options">'
	.'<option value="default">'.$text{'edit_Casefolddefault'}.'</option>'
	.'<option value="tolower" '
	.($Ea =~ /tolower/ ? 'selected' : '')
	.'>'.$text{'edit_Casefoldtolower'}.'</option>'
	.'<option value="toupper" '
	.($Ea =~ /toupper/ ? 'selected' : '')
	.'>'.$text{'edit_Casefoldtoupper'}.'</option>'
	.'<option value="xlatelower" '
	.($Ea =~ /xlatelower/ ? 'selected' : '')
	.'>'.$text{'edit_Casefoldxlatelower'}.'</option>'
	.'<option value="xlateupper" '
	.($Ea =~ /xlateupper/ ? 'selected' : '')
	.'>'.$text{'edit_Casefoldxlateupper'}.'</option>'
	.'</select>'
);
print &ui_table_row($text{'edit_AdvOptions'},
	"<input type=checkbox name=misc_options ".($caseinsensitive eq "1" ? "checked" : "")." value=caseinsensitive>$text{'edit_Optionscaseinsensitive'} <br>\n"
	."<input type=checkbox name=misc_options ".($crlf eq "1" ? "checked" : "")." value=crlf>$text{'edit_Optionscrlf'}<br>\n"
	."<input type=checkbox name=misc_options ".($illegalseq eq "1" ? "checked" : "")." value=illegalseq>$text{'edit_Optionsillegalseq'}<br>\n"
	."<input type=checkbox name=misc_options ".($mswindows eq "1" ? "checked" : "")." value=mswindows>$text{'edit_Optionsmswindows'}<br>\n"
	."<input type=checkbox name=misc_options ".($noadouble eq "1" ? "checked" : "")." value=noadouble>$text{'edit_Optionsnoadouble'}<br>\n"
	."<input type=checkbox name=misc_options ".($nocnidcache eq "1" ? "checked" : "")." value=nocnidcache>$text{'edit_Optionsnocnidcache'}<br>\n"
	."<input type=checkbox name=misc_options ".($nodev eq "1" ? "checked" : "")." value=nodev>$text{'edit_Optionsnodev'}<br>\n"
	."<input type=checkbox name=misc_options ".($nofileid eq "1" ? "checked" : "")." value=nofileid>$text{'edit_Optionsnofileid'}<br>\n"
	."<input type=checkbox name=misc_options ".($nohex eq "1" ? "checked" : "")." value=nohex>$text{'edit_Optionsnohex'}<br>\n"
	."<input type=checkbox name=misc_options ".($prodos eq "1" ? "checked" : "")." value=prodos>$text{'edit_Optionsprodos'}<br>\n"
);

print &ui_table_end();

print &ui_tabs_end_tab('mode', 'advanced');
print &ui_tabs_end();

print &ui_form_end([[undef, $text{'edit_save'}]]);

if ($in{action} =~ /edit/) {
	print &ui_form_start('fshare_delete_action.cgi', 'POST');
	print "<input type=\"hidden\" name=\"delete_volumepath\" value=\"$Old_path\">\n";
	print &ui_form_end([[undef, $text{'edit_delete'}, ]]);
}

&ui_print_footer("index.cgi", $text{'index_module'});
