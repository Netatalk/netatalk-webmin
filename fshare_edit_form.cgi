#!/usr/bin/perl
# Display a form for editing a file share

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
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
ui_print_header(undef, $text{'edit_file_share_title'}, "", "shares", 1);

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
	#print "users : $1 <br>\n";
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

print "<form action=fshare_save_action.cgi>\n";
print "<input type=\"hidden\" name=\"oldpath\" value=\"$Old_path\">\n";

print "<table width=100%>\n";
print "<tr $tb> <td><b>$text{'edit_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td>\n";
print "<table >\n";

	print "<tr><td align=right><b>$text{'edit_sharename'}</b></td>\n";
	print "<td colspan=4>\n";
	printf "<input size=44 name=share value=\"%s\" required>\n",
		($Old_path ne "~" && $Old_path ne "~/") ? $Old_shareName: "";
	print "</td> </tr>\n";
print "<tr>\n";
print "<td align=right><b>$text{'edit_sharedvolume'}</b></td>\n";
print "<td colspan=4>";
	printf "<input type=radio name=homes value=0 %s>\n",
		($Old_path ne "~" && $Old_path ne "~/") ? "checked" : "";
	printf "$text{'edit_directory'}<input name=path size=26 value=\"%s\" >\n",
		($Old_path ne "~" && $Old_path ne "~/") ? $Old_path: "";
	print &file_chooser_button("path", 1);
	print "<br>\n";
	printf "<input type=radio name=homes value=1 %s >$text{'edit_homedirectory'}<br>\n",
		($Old_path eq "~" || $Old_path eq "~/") ? "checked" : "";
print "<a href=\"/filemin\" target=\"_blank\">$text{'edit_filemanager_link'}</a>\n";
print "</td> </tr>\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Adouble'}</b></td>\n";
print "<td align=left colspan=3>\n";
printf "<input type=radio name=adouble_options %s value=default>$text{'edit_default'}<br>\n",
		 $Adouble eq "" ? "checked" : "";
printf "<input type=radio name=adouble_options %s value=v1>$text{'edit_Adoublev1'}<br>\n",
		 $Adouble eq "v1" ? "checked" : "";
printf "<input type=radio name=adouble_options %s value=v2>$text{'edit_Adoublev2'}<br>\n",
		 $Adouble eq "v2" ? "checked" : "";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_Volsizelimit'}</b></td>\n";
printf "<td colspan=4><input type=\"number\" name=volsizelimit min=\"1\" max=\"99999\" value=%s>\n",
	$Volsizelimit ne "" ? $Volsizelimit : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_AllowedHosts'}</b></td>\n";
printf "<td colspan=4><input name=allowed_hosts size=20 value=%s>\n",
	$AllowedHosts ne "" ? $AllowedHosts : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_DeniedHosts'}</b></td>\n";
printf "<td colspan=4><input name=denied_hosts size=20 value=%s>\n",
	$DeniedHosts ne "" ? $DeniedHosts : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_CnidScheme'}</b></td>\n";
printf "<td colspan=4><input name=cnidscheme size=5 value=%s>\n",
	$CnidScheme ne "" ? $CnidScheme : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_CnidServer'}</b></td>\n";
printf "<td colspan=4><input name=cnidserver size=20 value=%s>\n",
	$CnidServer ne "" ? $CnidServer : "";
print "</td> </tr>\n";

print "<tr><td align=right> <b>$text{'edit_DataBase'}</b></td>\n";
printf "<td colspan=4><input name=dbpath size=40 value=%s >\n",
	$Database ne "" ? $Database :  "";
print &file_chooser_button("dbpath", 1);
print "</td> </tr>\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Ea'}</b></td>\n";
print "<td align=left colspan=3>\n";
printf "<input type=radio name=ea_options %s value=default>$text{'edit_default'}<br>\n",
		 $Ea eq "" ? "checked" : "";
printf "<input type=radio name=ea_options %s value=auto>$text{'edit_Eaauto'}<br>\n",
		 $Ea eq "auto" ? "checked" : "";
printf "<input type=radio name=ea_options %s value=sys>$text{'edit_Easys'}<br>\n",
		 $Ea eq "sys" ? "checked" : "";
printf "<input type=radio name=ea_options %s value=ad>$text{'edit_Eaad'}<br>\n",
		 $Ea eq "ad" ? "checked" : "";
printf "<input type=radio name=ea_options %s value=none>$text{'edit_Eanone'}<br>\n",
		 $Ea eq "none" ? "checked" : "";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_MacCharset'}</b></td>\n";
printf "<td colspan=4><input name=maccharset size=20 value=%s>\n",
	$MacCharset ne "" ? $MacCharset : "";
print "</td> </tr>\n";

print "<tr><td  align=right valign=top><b>$text{'edit_MisceOptions'}</b></td>\n";
print "<td align=left colspan=3> \n";
printf "<input type=checkbox name=misc_options %s value=searchdb>$text{'edit_Optionssearchdb'} <br>\n",
		 $searchdb eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=tm>$text{'edit_Optionstm'}<br>\n",
		 $tm eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=nonetids>$text{'edit_Optionsnonetids'}<br>\n",
                 $nonetids eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=limitsize>$text{'edit_Optionslimitsize'}<br>\n",
                 $limitsize eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=ro>$text{'edit_Optionsro'}<br>\n",
                 $ro eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=upriv>$text{'edit_Optionsupriv'}<br>\n",
                 $upriv eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=usedots>$text{'edit_Optionsusedots'}<br>\n",
                 $usedots eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=invisibledots>$text{'edit_Optionsinvisibledots'}<br>\n",
		 $invisibledots eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=followsymlinks>$text{'edit_Optionsfollowsymlinks'}<br></td>\n",
                 $limitsize eq "1" ? "checked" : "";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_Password'}</b></td>\n";
printf "<td colspan=4><input maxlength=8 name=password size=8 value=%s>\n",
	$Password ne "" ? $Password : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Perm'}</b></td>\n";
printf "<td colspan=4><input name=perm size=8 value=%s>\n",
	$Perm ne "" ? $Perm : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_FPerm'}</b></td>\n";
printf "<td colspan=4><input name=fperm size=8 value=%s>\n",
	$FPerm ne "" ? $FPerm : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_DPerm'}</b></td>\n";
printf "<td colspan=4><input name=dperm size=8 value=%s>\n",
	$DPerm ne "" ? $DPerm : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Umask'}</b></td>\n";
printf "<td colspan=4><input name=umask size=8 value=%s>\n",
	$Umask ne "" ? $Umask : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Veto'}</b></td>\n";
printf "<td colspan=4><input name=veto size=20 value=%s>\n",
	$Veto ne "" ? $Veto : "";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_VolCharset'}</b></td>\n";
printf "<td colspan=4><input name=volcharset size=20 value=%s>\n",
	$VolCharset ne "" ? $VolCharset : "";
print "</td> </tr>\n";

print "<tr><td align=right valign=center><b>$text{'edit_Allow'}</b></td>\n";
	print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
printf "<input name=allow_users size=40 value=\"%s\"> %s</td> </tr>\n",
	join(' ',  @allow_users),
	&user_chooser_button("allow_users", 1);
print "<tr>\n";
	print"<td>&nbsp;&nbsp</td>\n";
	print" <td align=right>$text{'edit_groups'}</td> <td colspan=3>\n";
	printf "<input name=allow_groups size=40 value=\"%s\"> %s</td> </tr>\n",
	join(' ', grep { !/^@/ } @allow_groups),
	&group_chooser_button("allow_groups", 1);

print "<tr><td align=right valign=center><b>$text{'edit_Deny'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
printf "<input name=deny_users size=40 value=\"%s\"> %s</td> </tr>\n",
        join(' ',  @deny_users),
        &user_chooser_button("deny_users", 1);
print "<tr>\n";
        print"<td>&nbsp;&nbsp</td>\n";
        print" <td align=right>$text{'edit_groups'}</td> <td colspan=3>\n";
        printf "<input name=deny_groups size=40 value=\"%s\"> %s</td> </tr>\n",
        join(' ', grep { !/^@/ } @deny_groups),
        &group_chooser_button("deny_groups", 1);

print "<tr><td align=right valign=center><b>$text{'edit_Rolist'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
printf "<input name=rolist_users size=40 value=\"%s\"> %s</td> </tr>\n",
        join(' ',  @rolist_users),
        &user_chooser_button("rolist_users", 1);
print "<tr>\n";
        print"<td>&nbsp;&nbsp</td>\n";
        print" <td align=right>$text{'edit_groups'}</td> <td colspan=3>\n";
        printf "<input name=rolist_groups size=40 value=\"%s\"> %s</td> </tr>\n",
        join(' ', grep { !/^@/ } @rolist_groups),
        &group_chooser_button("rolist_groups", 1);

print "<tr><td  align=right valign=center><b>$text{'edit_Rwlist'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
printf "<input name=rwlist_users size=40 value=\"%s\"> %s</td> </tr>\n",
        join(' ',  @rwlist_users),
        &user_chooser_button("rwlist_users", 1);
print "<tr>\n";
        print"<td>&nbsp;&nbsp</td>\n";
        print" <td align=right>$text{'edit_groups'}</td> <td colspan=3>\n";
        printf "<input name=rwlist_groups size=40 value=\"%s\"> %s</td> </tr>\n",
        join(' ', grep { !/^@/ } @rwlist_groups),
        &group_chooser_button("rwlist_groups", 1);
print "</table> </td></tr>\n";
print "<tr $tb> <td><b>$text{'edit_adv_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td><table >\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Casefold'}</b></td>\n";
print "<td align=left colspan=3> \n";
printf "<input type=radio name=casefold_options %s value=default>$text{'edit_Casefolddefault'}<br>\n",
		 $Casefold eq "" ? "checked" : "";
printf "<input type=radio name=casefold_options %s value=tolower>$text{'edit_Casefoldtolower'}<br>\n",
		 $Casefold eq "tolower" ? "checked" : "";
printf "<input type=radio name=casefold_options %s value=toupper>$text{'edit_Casefoldtoupper'}<br>\n",
		 $Casefold eq "toupper" ? "checked" : "";
printf "<input type=radio name=casefold_options %s value=xlatelower>$text{'edit_Casefoldxlatelower'}<br>\n",
		 $Casefold eq "xlatelower" ? "checked" : "";
printf "<input type=radio name=casefold_options %s value=xlateupper>$text{'edit_Casefoldxlateupper'}<br>\n",
		 $Casefold eq "xlateupper" ? "checked" : "";
print "</td></tr>\n";

print "<tr><td  align=right valign=top><b>$text{'edit_AdvOptions'}</b></td>\n";
print "<td align=left colspan=3> \n";
printf "<input type=checkbox name=misc_options %s value=caseinsensitive>$text{'edit_Optionscaseinsensitive'}<br>\n",
		 $caseinsensitive eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=crlf>$text{'edit_Optionscrlf'}<br>\n",
		 $crlf eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=illegalseq>$text{'edit_Optionsillegalseq'}<br>\n",
                 $illegalseq eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=mswindows>$text{'edit_Optionsmswindows'}<br>\n",
                 $mswindows eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=noadouble>$text{'edit_Optionsnoadouble'}<br>\n",
		 $noadouble eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=nocnidcache>$text{'edit_Optionsnocnidcache'}<br>\n",
                 $nocnidcache eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=nodev>$text{'edit_Optionsnodev'}<br>\n",
                 $nodev eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=nofileid>$text{'edit_Optionsnofileid'}<br>\n",
                 $nofileid eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=nohex>$text{'edit_Optionsnohex'}<br>\n",
                 $nohex eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=prodos>$text{'edit_Optionsprodos'} <br>\n",
		 $prodos eq "1" ? "checked" : "";
print "</td></tr>\n";
print "</table> </td></tr>\n";
print "</table>\n";

print "<input type=submit value=$text{'edit_Save'}></form>\n";

print "<form action=fshare_delete_action.cgi>\n";
print "<input type=hidden name=delete value=$Old_path>\n";
print "<input type=submit value=$text{'global_Delete'}></form>\n";

ui_print_footer("index.cgi", $text{'index_module'});
