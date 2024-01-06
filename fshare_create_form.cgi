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

require 'netatalk2-lib.pl';

ui_print_header(undef, $text{'edit_header'}, "", "shares", 1);

print "<form action=fshare_save_action.cgi>\n";
print "<table width=100%>\n";
print "<tr $tb> <td><b>$text{'edit_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td>\n";
print "<table>\n";
	print "<tr><td align=right><b>$text{'edit_sharename'}</b></td>\n";
	print "<td colspan=4>\n";
	print "<input type=radio name=homes value=0 checked>\n";
	print "<input size=10 name=share value=\"\">\n";
	print "<input type=radio name=homes value=1 >$text{'edit_homedirectory'}\n";
	print "</td> </tr>\n";
print "<tr> <td align=right><b>$text{'edit_directory'}</b></td>\n";
print "<td colspan=4><input name=path size=40 value=\"\" >\n";
print &file_chooser_button("path", 1);
print "<br><a href=\"/filemin\" target=\"_blank\">$text{'edit_filemanager_link'}</a>";
print "</td> </tr>\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Adouble'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=radio name=adouble_options %s value=default checked>$text{'edit_default'}<br>\n";
print "<input type=radio name=adouble_options %s value=v1>$text{'edit_Adoublev1'}<br>\n";
print "<input type=radio name=adouble_options %s value=v2>$text{'edit_Adoublev2'}<br>\n";
print "<input type=radio name=adouble_options %s value=osx>$text{'edit_Adoubleosx'}<br>\n";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_Volsizelimit'}</b></td>\n";
print "<td colspan=4><input type=\"number\" name=volsizelimit min=\"1\" max=\"99999\" value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_AllowedHosts'}</b></td>\n";
print "<td colspan=4><input name=allowed_hosts size=20 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_DeniedHosts'}</b></td>\n";
print "<td colspan=4><input name=denied_hosts size=20 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_CnidScheme'}</b></td>\n";
print "<td colspan=4><input name=cnidscheme size=5 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_CnidServer'}</b></td>\n";
print "<td colspan=4><input name=cnidserver size=20 value=\"\">\n";
print "</td> </tr>\n";

print "<tr><td align=right> <b>$text{'edit_DataBase'}</b></td>\n";
	print "<td colspan=4><input name=dbpath size=40 value=\"\">\n";
	print &file_chooser_button("dbpath", 1);
print "</td> </tr>\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Ea'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=radio name=ea_options value=default checked>$text{'edit_default'}<br>\n";
print "<input type=radio name=ea_options value=auto>$text{'edit_Eaauto'}<br>\n";
print "<input type=radio name=ea_options value=sys>$text{'edit_Easys'}<br>\n";
print "<input type=radio name=ea_options value=ad>$text{'edit_Eaad'}<br>\n";
print "<input type=radio name=ea_options value=none>$text{'edit_Eanone'}<br>\n";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_MacCharset'}</b></td>\n";
print "<td colspan=4><input name=maccharset size=20 value=\"\">\n";
print "</td> </tr>\n";

print "<tr><td align=right valign=top><b>$text{'edit_MisceOptions'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=checkbox name=misc_options value=searchdb>$text{'edit_Optionssearchdb'} <br>\n";
print "<input type=checkbox name=misc_options value=tm>$text{'edit_Optionstm'}<br>\n";
print "<input type=checkbox name=misc_options value=nonetids>$text{'edit_Optionsnonetids'}<br>\n";
print "<input type=checkbox name=misc_options value=limitsize>$text{'edit_Optionslimitsize'}<br>\n";
print "<input type=checkbox name=misc_options value=ro>$text{'edit_Optionsro'}<br>\n";
print "<input type=checkbox name=misc_options value=upriv>$text{'edit_Optionsupriv'}<br>\n";
print "<input type=checkbox name=misc_options value=usedots>$text{'edit_Optionsusedots'}<br>\n";
print "<input type=checkbox name=misc_options value=invisibledots>$text{'edit_Optionsinvisibledots'}<br>\n";
print "<input type=checkbox name=misc_options value=followsymlinks>$text{'edit_Optionsfollowsymlinks'}<br>\n";
print "</td></tr>\n";

print "<tr> <td align=right><b>$text{'edit_Password'}</b></td>\n";
	print "<td colspan=4><input maxlength=8 name=password size=8 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Perm'}</b></td>\n";
print "<td colspan=4><input name=perm size=8 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_FPerm'}</b></td>\n";
print "<td colspan=4><input name=fperm size=8 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_DPerm'}</b></td>\n";
print "<td colspan=4><input name=dperm size=8 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Umask'}</b></td>\n";
print "<td colspan=4><input name=umask size=8 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_Veto'}</b></td>\n";
print "<td colspan=4><input name=veto size=20 value=\"\">\n";
print "</td> </tr>\n";

print "<tr> <td align=right><b>$text{'edit_VolCharset'}</b></td>\n";
print "<td colspan=4><input name=volcharset size=20 value=\"\">\n";
print "</td> </tr>\n";

print "<tr><td  align=right valign=center><b>$text{'edit_Allow'}</b></td>\n";
	print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
	printf "<input name=allow_users size=40 value=\"\"> %s</td> </tr>\n", &user_chooser_button("allow_users", 1);
print "<tr>";
	print "<td>&nbsp;&nbsp;</td>\n";
	print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=allow_groups size=40 value=\"\"> %s</td> </tr>\n",&group_chooser_button("allow_groups", 1);

print "<tr><td  align=right valign=center><b>$text{'edit_Deny'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=deny_users size=40 value=\"\"> %s</td> </tr>\n", &user_chooser_button("deny_users", 1);
print "<tr>";
        print "<td>&nbsp;&nbsp;</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=deny_groups size=40 value=\"\"> %s</td> </tr>\n",&group_chooser_button("deny_groups", 1);

print"<tr><td  align=right valign=center><b>$text{'edit_Rolist'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=rolist_users size=40 value=\"\"> %s</td> </tr>\n", &user_chooser_button("rolist_users", 1);
print "<tr>";
        print "<td>&nbsp;&nbsp;</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=rolist_groups size=40 value=\"\"> %s</td> </tr>\n",&group_chooser_button("rolist_groups", 1);

print "<tr><td  align=right valign=center><b>$text{'edit_Rwlist'}</b></td>\n";
        print "<td align=left>$text{'edit_users'}</td> <td align=left>\n";
        printf "<input name=rwlist_users size=40 value=\"\"> %s</td> </tr>\n", &user_chooser_button("rwlist_users", 1);
print "<tr>";
        print "<td>&nbsp;&nbsp;</td>\n";
        print "<td align=left>$text{'edit_groups'}</td> <td align=left>\n";
printf "<input name=rwlist_groups size=40 value=\"\"> %s</td> </tr>\n",&group_chooser_button("rwlist_groups", 1);
print "</table> </td></tr>\n";

print "<tr $tb> <td><b>$text{'edit_adv_tableheader'}</b></td></tr>\n";
print "<tr $cb> <td>\n";
print "<table>\n";

print "<tr><td align=right valign=top ><b>$text{'edit_Casefold'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=radio name=casefold_options checked value=default>$text{'edit_Casefolddefault'}<br>\n";
print "<input type=radio name=casefold_options value=tolower>$text{'edit_Casefoldtolower'}<br>\n";
print "<input type=radio name=casefold_options value=toupper>$text{'edit_Casefoldtoupper'}<br>\n";
print "<input type=radio name=casefold_options value=xlatelower>$text{'edit_Casefoldxlatelower'}<br>\n";
print "<input type=radio name=casefold_options value=xlateupper>$text{'edit_Casefoldxlateupper'}<br>\n";
print "</td></tr>\n";

print "<tr><td align=right valign=top><b>$text{'edit_AdvOptions'}</b></td>\n";
print "<td align=left colspan=3>\n";
print "<input type=checkbox name=misc_options value=caseinsensitive>$text{'edit_Optionscaseinsensitive'}<br>\n";
print "<input type=checkbox name=misc_options value=crlf>$text{'edit_Optionscrlf'}<br>\n";
print "<input type=checkbox name=misc_options value=illegalseq>$text{'edit_Optionsillegalseq'}<br>\n";
print "<input type=checkbox name=misc_options value=mswindows>$text{'edit_Optionsmswindows'}<br>\n";
print "<input type=checkbox name=misc_options value=noadouble>$text{'edit_Optionsnoadouble'}<br>\n";
print "<input type=checkbox name=misc_options value=nocnidcache>$text{'edit_Optionsnocnidcache'}<br>\n";
print "<input type=checkbox name=misc_options value=nodev>$text{'edit_Optionsnodev'}<br>\n";
print "<input type=checkbox name=misc_options value=nofileid>$text{'edit_Optionsnofileid'}<br>\n";
print "<input type=checkbox name=misc_options value=nohex>$text{'edit_Optionsnohex'}<br>\n";
print "<input type=checkbox name=misc_options value=prodos>$text{'edit_Optionsprodos'} <br>\n";
print "</td></tr>\n";

print "</table> </td></tr></table>\n";

print "<input type=submit value=$text{'edit_create'}>\n";
print "<input type=reset value=$text{'edit_reset'}>\n";
print "</form>";

ui_print_footer("index.cgi", $text{'index_module'});
