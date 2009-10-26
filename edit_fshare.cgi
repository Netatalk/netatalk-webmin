#!/usr/bin/perl
# edit_fshare.cgi
# Display a form for creating a new file share

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

$path="NoPath";
$s="homes";

&header($text{'edit_header'},"", "intro", 1, 1, undef());
print"<p><p>\n";


print "<hr>\n";
print"<p><p>\n";
print "<form action=save_fshare.cgi>\n";

print "<table  width=100%>\n";
print "<tr $tb> <td><b>$text{'edit_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td><table>\n";
	print "<tr><td align=right><b>$text{'edit_sharename'}</b></td>\n";
	print "<td colspan=4>";
	print "<input  type=radio name=homes value=0>\n";
	print "<input size=10 name=share value=>&nbsp;&nbsp;&nbsp;\n";
	print "<input type=radio name=homes value=1 >$text{'edit_homedirectory'}\n";
	print "</td> </tr>\n";
print "<tr> <td align=right><b>$text{'edit_directory'}</b></td>\n";
print "<td colspan=4><input name=path size=40  value= >\n";
print &file_chooser_button("path", 1);
print "</td> </tr>\n";
print"<tr><td align=left><br></td></tr>\n";

print"<tr><td align=right valign=top ><b>$text{'edit_Casefold'}</b></td>\n";
print"<td  align=left colspan=3> \n";
print"<input type=radio name=casefold_options checked value=default>&nbsp;&nbsp;$text{'edit_Casefolddefault'}<br>\n";
print"<input type=radio name=casefold_options value=tolower>&nbsp;&nbsp;$text{'edit_Casefoldtolower'}<br>\n";
print"<input type=radio name=casefold_options value=toupper>&nbsp;&nbsp;$text{'edit_Casefoldtoupper'}<br>\n";
print"<input type=radio name=casefold_options value=xlatelower>&nbsp;&nbsp;$text{'edit_Casefoldxlatelower'}<br>\n";
print"<input type=radio name=casefold_options value=xlateupper>&nbsp;&nbsp;$text{'edit_Casefoldxlateupper'}<br> </td></tr>\n";

print"<tr><td align=right><b>$text{'edit_CodePage'}</b></td>\n";
print"<td colspan=2><select align=left  name=codepage> \n";
print"<option value=default selected>$text{'edit_CodePagedefault'}\n";
$counter=1;
foreach $s (getMacCodeFiles())
{
	$show=$s;
        if($s=~/(\w+).(\w+)$/ )
        {
        	$show="$1.$2";	
	
	}
	print "<option value=$s> $show\n";	
}
print"</select>\n";
print"</tr>\n";

print"<tr><td  align=right valign=top><b>$text{'edit_MisceOptions'}</b></td>\n";
print"<td  align=left colspan=3> \n";
print"<input type=checkbox name=misc_options value=prodos>&nbsp;&nbsp;$text{'edit_MisceOptionsprodos'} <br>\n";
print"<input type=checkbox name=misc_options value=crlf>&nbsp;&nbsp;$text{'edit_MisceOptionscrlf'}  <br>\n";
print"<input type=checkbox name=misc_options value=noadouble>&nbsp;&nbsp;$text{'edit_MisceOptionsnoadouble'}<br>\n";
print"<input type=checkbox name=misc_options value=ro>&nbsp;&nbsp;$text{'edit_MisceOptionsro'}<br>\n";
print"<input type=checkbox name=misc_options value=mswindows>&nbsp;&nbsp;$text{'edit_MisceOptionsmswindows'}<br>\n";
print"<input type=checkbox name=misc_options value=nohex>&nbsp;&nbsp;$text{'edit_MisceOptionsnohex'}<br>\n";
print"<input type=checkbox name=misc_options value=usedots>&nbsp;&nbsp;$text{'edit_MisceOptionsusedots'}<br>\n";
print"<input type=checkbox name=misc_options value=limitsize>&nbsp;&nbsp;$text{'edit_MisceOptionslimitsize'}<br>\n";
print "</td></tr>\n";
print"<tr><td align=left></td></tr>\n";


print "<tr><td align=right> <b>$text{'edit_DataBase'}</b></td>\n";
	print "<td colspan=4><input name=dbpath size=40 value= >\n";
	print &file_chooser_button("dbpath", 1);
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Password'}</b></td>\n";
	print "<td colspan=4><input maxlength=8 name=password size=8 value=>\n";
print "</td> </tr>\n";

print"<tr><td  align=right valign=center><b>$text{'edit_Allow'}</b></td>\n";
	print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
	printf "<input name=allow_users size=40 value=> %s</td> </tr>\n", &user_chooser_button("allow_users", 1);
print "<tr>";
	print"<td>&nbsp;&nbsp</td>\n";	
	print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=allow_groups size=40 value=> %s</td> </tr>\n",&group_chooser_button("allow_groups", 1);

print"<tr><td  align=right valign=center><b>$text{'edit_Deny'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=deny_users size=40 value=> %s</td> </tr>\n", &user_chooser_button("deny_users", 1);
print "<tr>";
        print"<td>&nbsp;&nbsp</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=deny_groups size=40 value=> %s</td> </tr>\n",&group_chooser_button("deny_groups", 1);

print"<tr><td  align=right valign=center><b>$text{'edit_Rolist'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=rolist_users size=40 value=> %s</td> </tr>\n", &user_chooser_button("rolist_users", 1);
print "<tr>";
        print"<td>&nbsp;&nbsp</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=rolist_groups size=40 value=> %s</td> </tr>\n",&group_chooser_button("rolist_groups", 1);

print"<tr><td  align=right valign=center><b>$text{'edit_Rwlist'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=rwlist_users size=40 value=> %s</td> </tr>\n", &user_chooser_button("rwlist_users", 1);
print "<tr>";
        print"<td>&nbsp;&nbsp</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=rwlist_groups size=40 value=> %s</td> </tr>\n",&group_chooser_button("rwlist_groups", 1);


print "</table> </td></tr></table><p>\n";
print "<table width=100% >\n";
print"<tr>";
print "<td align=left><input type=submit value=$text{'edit_create'}></td>\n";
print "<td align=right><input type=reset value=Reset></td><br>\n";
print"</tr></table></form>";

print "<hr>\n";
print"<p><p>\n";
&footer("index.cgi",$text{'edit_return'});
