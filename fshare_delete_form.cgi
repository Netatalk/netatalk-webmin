#!/usr/bin/perl
# Display a form for deleting a file share

#
#    Netatalk Webmin Module
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

require 'netatalk2-lib.pl';

&ui_print_header(undef, $text{'delete_file_share_title'}, "", "shares", 1);

print &ui_form_start('fshare_delete_action.cgi', 'POST');

print "<h4>Select File Share</h4>\n";

print "<select name=delete> \n";

# Known bug: If two volumes are using the same path, the first in the list will be deleted
#            regardless of which one is chosen in the dropdown.
foreach $s (open_afile())
{
	$shareName= getShareName($s);
	$Path     = getPath($s);
	$show     = "$shareName ($Path)";

	print "<option value=$Path> $show\n";
}

print "</select>\n";
print &ui_form_end([[undef, $text{'edit_delete'}, ]]);

ui_print_footer("index.cgi", $text{'index_module'});
