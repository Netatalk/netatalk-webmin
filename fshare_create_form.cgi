#!/usr/bin/perl
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

require './netatalk2-lib.pl';

$path="NoPath";
$s="homes";

&header($text{'edit_header'},"", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\" target=\"_blank\">$text{help_configs}</a>");
print"<p><p>\n";


print "<hr>\n";
print "<p><p>\n";
print "<form action=fshare_save_action.cgi>\n";

print "<table width=100%>\n";
print "<tr $tb> <td><b>$text{'edit_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td>\n";
print "<table>\n";
	print "<tr><td align=right><b>$text{'edit_sharename'}</b></td>\n";
	print "<td colspan=4>\n";
	print "<input type=radio name=homes value=0 checked>\n";
	print "<input size=10 name=share value=>&nbsp;&nbsp;&nbsp;\n";
	print "<input type=radio name=homes value=1 >$text{'edit_homedirectory'}\n";
	print "</td> </tr>\n";
print "<tr> <td align=right><b>$text{'edit_directory'}</b></td>\n";
print "<td colspan=4><input name=path size=40  value= >\n";
print &file_chooser_button("path", 1);
print "</td> </tr>\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Adouble'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=radio name=adouble_options %s value=default checked>&nbsp;&nbsp;$text{'edit_default'}<br>\n";
print "<input type=radio name=adouble_options %s value=v1>&nbsp;&nbsp;$text{'edit_Adoublev1'}<br>\n";
print "<input type=radio name=adouble_options %s value=v2>&nbsp;&nbsp;$text{'edit_Adoublev2'}<br>\n";
print "<input type=radio name=adouble_options %s value=osx>&nbsp;&nbsp;$text{'edit_Adoubleosx'}<br>\n";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_Volsizelimit'}</b></td>\n";
print "<td colspan=4><input type=\"number\" name=volsizelimit min=\"1\" max=\"99999\" value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_AllowedHosts'}</b></td>\n";
print "<td colspan=4><input name=allowed_hosts size=20 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_DeniedHosts'}</b></td>\n";
print "<td colspan=4><input name=denied_hosts size=20 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_CnidScheme'}</b></td>\n";
print "<td colspan=4><input name=cnidscheme size=5 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_CnidServer'}</b></td>\n";
print "<td colspan=4><input name=cnidserver size=20 value= >\n";
print "</td> </tr>\n";

print "<tr><td align=right> <b>$text{'edit_DataBase'}</b></td>\n";
	print "<td colspan=4><input name=dbpath size=40 value= >\n";
	print &file_chooser_button("dbpath", 1);
print "</td> </tr>\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Ea'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=radio name=ea_options value=default checked>&nbsp;&nbsp;$text{'edit_default'}<br>\n";
print "<input type=radio name=ea_options value=auto>&nbsp;&nbsp;$text{'edit_Eaauto'}<br>\n";
print "<input type=radio name=ea_options value=sys>&nbsp;&nbsp;$text{'edit_Easys'}<br>\n";
print "<input type=radio name=ea_options value=ad>&nbsp;&nbsp;$text{'edit_Eaad'}<br>\n";
print "<input type=radio name=ea_options value=none>&nbsp;&nbsp;$text{'edit_Eanone'}<br>\n";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_MacCharset'}</b></td>\n";
print "<td colspan=4><input name=maccharset size=20 value= >\n";
print "</td> </tr>\n";

print "<tr><td align=right valign=top><b>$text{'edit_MisceOptions'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=checkbox name=misc_options value=searchdb>&nbsp;&nbsp;$text{'edit_Optionssearchdb'} <br>\n";
print "<input type=checkbox name=misc_options value=tm>&nbsp;&nbsp;$text{'edit_Optionstm'}<br>\n";
print "<input type=checkbox name=misc_options value=invisibledots>&nbsp;&nbsp;$text{'edit_Optionsinvisibledots'}<br>\n";
print "<input type=checkbox name=misc_options value=nonetids>&nbsp;&nbsp;$text{'edit_Optionsnonetids'}<br>\n";
print "<input type=checkbox name=misc_options value=limitsize>&nbsp;&nbsp;$text{'edit_Optionslimitsize'}<br>\n";
print "<input type=checkbox name=misc_options value=preexec_close>&nbsp;&nbsp;$text{'edit_Optionspreexec_close'}<br>\n";
print "<input type=checkbox name=misc_options value=ro>&nbsp;&nbsp;$text{'edit_Optionsro'}<br>\n";
print "<input type=checkbox name=misc_options value=root_preexec_close>&nbsp;&nbsp;$text{'edit_Optionsroot_preexec_close'}<br>\n";
print "<input type=checkbox name=misc_options value=upriv>&nbsp;&nbsp;$text{'edit_Optionsupriv'}<br>\n";
print "<input type=checkbox name=misc_options value=usedots>&nbsp;&nbsp;$text{'edit_Optionsusedots'}<br>\n";
print "<input type=checkbox name=misc_options value=followsymlinks>&nbsp;&nbsp;$text{'edit_Optionsfollowsymlinks'}<br>\n";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_Password'}</b></td>\n";
	print "<td colspan=4><input maxlength=8 name=password size=8 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Perm'}</b></td>\n";
print "<td colspan=4><input name=perm size=8 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_FPerm'}</b></td>\n";
print "<td colspan=4><input name=fperm size=8 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_DPerm'}</b></td>\n";
print "<td colspan=4><input name=dperm size=8 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Umask'}</b></td>\n";
print "<td colspan=4><input name=umask size=8 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_PreExec'}</b></td>\n";
print "<td colspan=4><input name=preexec size=20 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_PostExec'}</b></td>\n";
print "<td colspan=4><input name=postexec size=20 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_RootPreExec'}</b></td>\n";
print "<td colspan=4><input name=root_preexec size=20 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_RootPostExec'}</b></td>\n";
print "<td colspan=4><input name=root_postexec size=20 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Veto'}</b></td>\n";
print "<td colspan=4><input name=veto size=20 value= >\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_VolCharset'}</b></td>\n";
print "<td colspan=4><input name=volcharset size=20 value= >\n";
print "</td> </tr>\n";

print "<tr><td  align=right valign=center><b>$text{'edit_Allow'}</b></td>\n";
	print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
	printf "<input name=allow_users size=40 value=> %s</td> </tr>\n", &user_chooser_button("allow_users", 1);
print "<tr>";
	print "<td>&nbsp;&nbsp</td>\n";	
	print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=allow_groups size=40 value=> %s</td> </tr>\n",&group_chooser_button("allow_groups", 1);

print "<tr><td  align=right valign=center><b>$text{'edit_Deny'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=deny_users size=40 value=> %s</td> </tr>\n", &user_chooser_button("deny_users", 1);
print "<tr>";
        print "<td>&nbsp;&nbsp</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=deny_groups size=40 value=> %s</td> </tr>\n",&group_chooser_button("deny_groups", 1);

print"<tr><td  align=right valign=center><b>$text{'edit_Rolist'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=rolist_users size=40 value=> %s</td> </tr>\n", &user_chooser_button("rolist_users", 1);
print "<tr>";
        print "<td>&nbsp;&nbsp</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=rolist_groups size=40 value=> %s</td> </tr>\n",&group_chooser_button("rolist_groups", 1);

print "<tr><td  align=right valign=center><b>$text{'edit_Rwlist'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=rwlist_users size=40 value=> %s</td> </tr>\n", &user_chooser_button("rwlist_users", 1);
print "<tr>";
        print "<td>&nbsp;&nbsp</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=rwlist_groups size=40 value=> %s</td> </tr>\n",&group_chooser_button("rwlist_groups", 1);
print "</table> </td></tr>\n";

print "<tr $tb> <td><b>$text{'edit_adv_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td>\n";
print "<table>\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Casefold'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=radio name=casefold_options checked value=default>&nbsp;&nbsp;$text{'edit_default'}<br>\n";
print "<input type=radio name=casefold_options value=tolower>&nbsp;&nbsp;$text{'edit_Casefoldtolower'}<br>\n";
print "<input type=radio name=casefold_options value=toupper>&nbsp;&nbsp;$text{'edit_Casefoldtoupper'}<br>\n";
print "<input type=radio name=casefold_options value=xlatelower>&nbsp;&nbsp;$text{'edit_Casefoldxlatelower'}<br>\n";
print "<input type=radio name=casefold_options value=xlateupper>&nbsp;&nbsp;$text{'edit_Casefoldxlateupper'}<br>\n";
print "</td></tr>\n";

print "<tr><td align=right valign=top><b>$text{'edit_AdvOptions'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=checkbox name=misc_options value=caseinsensitive>&nbsp;&nbsp;$text{'edit_Optionscaseinsensitive'}<br>\n";
print "<input type=checkbox name=misc_options value=crlf>&nbsp;&nbsp;$text{'edit_Optionscrlf'}<br>\n";
print "<input type=checkbox name=misc_options value=illegalseq>&nbsp;&nbsp;$text{'edit_Optionsillegalseq'}<br>\n";
print "<input type=checkbox name=misc_options value=mswindows>&nbsp;&nbsp;$text{'edit_Optionsmswindows'}<br>\n";
print "<input type=checkbox name=misc_options value=noadouble>&nbsp;&nbsp;$text{'edit_Optionsnoadouble'}<br>\n";
print "<input type=checkbox name=misc_options value=nocnidcache>&nbsp;&nbsp;$text{'edit_Optionsnocnidcache'}<br>\n";
print "<input type=checkbox name=misc_options value=nodev>&nbsp;&nbsp;$text{'edit_Optionsnodev'}<br>\n";
print "<input type=checkbox name=misc_options value=nofileid>&nbsp;&nbsp;$text{'edit_Optionsnofileid'}<br>\n";
print "<input type=checkbox name=misc_options value=nohex>&nbsp;&nbsp;$text{'edit_Optionsnohex'}<br>\n";
print "<input type=checkbox name=misc_options value=nostat>&nbsp;&nbsp;$text{'edit_Optionsnostat'}<br>\n";
print "<input type=checkbox name=misc_options value=prodos>&nbsp;&nbsp;$text{'edit_Optionsprodos'} <br>\n";
print "</td></tr>\n";

print "</table> </td></tr></table><p>\n";
print "<table width=100% >\n";
print "<tr>";
print "<td align=left><input type=submit value=$text{'edit_create'}></td>\n";
print "<td align=right><input type=reset value=Reset></td><br>\n";
print"</tr></table></form>";

print "<hr>\n";
print "<p><p>\n";

&footer("index.cgi",$text{'edit_return'});
