#!/usr/bin/perl
# edit_fshare.cgi
# Display a form for editing  directory share

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Some code (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Contributions from:
#       Sven Mosimann <sven.mosimann@ecologic.ch>
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

require './netapple-lib.pl';
require 'netatalk-funcs.pl';

&ReadParse();
open_afile();


$path="NoPath";
$s="homes";
@usres =(); @groups =();

&header($text{'edit_file_title'}, "", "intro", 1, 1, undef());

if($in{shareName}){
	$Old_shareName= $in{shareName};
}
if($in{path}){
	$Old_path=$in{path};
}

$Casefold = getCasfold($Old_shareName);

$Codepage = getCodepage($Old_shareName);

$Options = getOptions($Old_shareName);

#mgk: added new options
while( $Options =~ /\b([A-Za-z]+)\b/g) {
	if($1 eq "prodos"){
		$prodos=1;	
	}
	elsif($1 eq "crlf"){
		$crlf=1;
	}
	elsif($1 eq "noadouble"){
		$noadouble=1;
	}
	elsif($1 eq "ro"){
                $ro=1;
        }
	elsif($1 eq "mswindows"){
                $mswindows=1;
        }
	elsif($1 eq "nohex"){
                $nohex=1;
        }
	elsif($1 eq "usedots"){
                $usedots=1;
        }
	elsif($1 eq "limitsize"){
                $limitsize=1;
        }
}
$Database = getDatabase($Old_shareName);

$Password = getPassword($Old_shareName);

#mgk: reconstruction for new system (new loops, 0-9 characters and '$')
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


$Oldpath= "oldpath";

print "<hr>\n";
print"<p><p>\n";
print "<form action=save_Modi_FShare.cgi>\n";
print "<input type=hidden name=","oldpath"," value=$Old_path>\n";

print "<table  width=100%>\n";
print "<tr $tb> <td><b>$text{'modi_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td><table >\n";
	print "<tr><td align=right><b>$text{'edit_sharename'}</b></td>\n";
	print "<td colspan=4>";
	printf "<input type=radio  name=homes value=0 %s>\n",
		$Old_path ne "~" ? "checked" : "";
	printf "<input size=10 name=share value=\"%s\">\n",
		$Old_path ne "~" ? $Old_shareName: "";
	printf "<input type=radio name=homes value=1 %s >$text{'edit_homedirectory'}\n",
		$Old_path eq "~" ? "checked" : "";
	print "</td> </tr>\n";
print "<tr> <td align=right><b>$text{'edit_directory'}</b></td>\n";
print "<td colspan=4>\n";
printf "<input name=path size=40  value=%s>\n",
		$Old_path ne "~" ? $Old_path : "" ;
print  &file_chooser_button("path", 1);
print "</td> </tr>\n";
print"<tr><td align=left><br></td></tr>\n";

print"<tr><td align=right valign=top ><b>$text{'edit_Casefold'}</b></td>\n";
print"<td  align=left colspan=3> \n";
printf "<input type=radio name=casefold_options %s value=default>&nbsp;&nbsp;$text{'edit_Casefolddefault'}<br>\n",
		 $Casefold eq "" ? "checked" : "";
printf "<input type=radio name=casefold_options %s value=tolower>&nbsp;&nbsp;$text{'edit_Casefoldtolower'}<br>\n",
		 $Casefold eq "tolower" ? "checked" : "";
printf "<input type=radio name=casefold_options %s value=toupper>&nbsp;&nbsp;$text{'edit_Casefoldtoupper'}<br>\n",
		 $Casefold eq "toupper" ? "checked" : "";
printf "<input type=radio name=casefold_options %s value=xlatelower>&nbsp;&nbsp;$text{'edit_Casefoldxlatelower'}<br>\n",
		 $Casefold eq "xlatelower" ? "checked" : "";
printf "<input type=radio name=casefold_options %s value=xlateupper>&nbsp;&nbsp;$text{'edit_Casefoldxlateupper'}<br>\n",
		 $Casefold eq "xlateupper" ? "checked" : "";
print"</td></tr>\n";

print"<tr><td align=right><b>$text{'edit_CodePage'}</b></td>\n";
print"<td colspan=2><select align=left  name=codepage> \n";
print"<option value=default > default \n";
$counter=1;
foreach $input (getMacCodeFiles())
{
	$show=$input;
        if($input=~/(\w+).(\w+)$/ )
        {
        	$show="$1.$2";	
	
	}
	printf "<option   value=$input %s> $show\n",
		$Codepage eq $input ? "selected" : "";	
}
print"</select>\n";
print"</tr>\n";

print"<tr><td  align=right valign=top><b>$text{'edit_MisceOptions'}</b></td>\n";
print"<td  align=left colspan=3> \n";
printf "<input type=checkbox name=misc_options %s value=prodos>&nbsp;&nbsp;$text{'edit_MisceOptionsprodos'} <br>\n",
		 $prodos eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=crlf>&nbsp;&nbsp;$text{'edit_MisceOptionscrlf'}<br>\n",
		 $crlf eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=noadouble>&nbsp;&nbsp;$text{'edit_MisceOptionsnoadouble'}<br>\n",
		 $noadouble eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=ro>&nbsp;&nbsp;$text{'edit_MisceOptionsro'}<br>\n",
                 $ro eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=mswindows>&nbsp;&nbsp;$text{'edit_MisceOptionsmswindows'}<br>\n",
                 $mswindows eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=nohex>&nbsp;&nbsp;$text{'edit_MisceOptionsnohex'}<br>\n",
                 $crlf eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=usedots>&nbsp;&nbsp;$text{'edit_MisceOptionsusedots'}<br>\n",
                 $usedots eq "1" ? "checked" : "";
printf "<input type=checkbox name=misc_options %s value=limitsize>&nbsp;&nbsp;$text{'edit_MisceOptionslimitsize'}<br></td>\n",
                 $limitsize eq "1" ? "checked" : "";
print "<tr><td align=right> <b>$text{'edit_DataBase'}</b></td>\n";
printf "<td colspan=4><input name=dbpath size=40 value=%s >\n",
	$Database ne "" ? $Database :  "";
print &file_chooser_button("dbpath", 1);
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Password'}</b></td>\n";
printf "<td colspan=4><input maxlength=8 name=password size=8 value=%s>\n",
	$Password ne "" ? $Password : "";
print "</td> </tr>\n";

print"<tr><td  align=right valign=center><b>$text{'edit_Allow'}</b></td>\n";
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

print"<tr><td  align=right valign=center><b>$text{'edit_Deny'}</b></td>\n";
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

print"<tr><td  align=right valign=center><b>$text{'edit_Rolist'}</b></td>\n";
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

print"<tr><td  align=right valign=center><b>$text{'edit_Rwlist'}</b></td>\n";
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
print "</table> </td></tr></table><p>\n";

print"<table   width=100%>\n";
print "<tr><td align=left><input type=submit value=$text{'modi_save'}></td></form>\n";
print"<form action=delete_FShare.cgi>\n";
print "<td align=right>\n";
	print"<input type=hidden  name=delete value=$Old_path>\n";
	print"<input type=submit value=$text{'global_Delete'}></td></tr></form>\n";
print"</table>\n";
print "<hr>\n";
print"<p><p>\n";
&footer("",$text{'edit_return'});
