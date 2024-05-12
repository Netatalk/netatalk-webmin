#!/usr/bin/perl
# Action for deleting a file share
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

require './netatalk2-lib.pl';

&ReadParse();

if($in{'delete_volumepath'}){
	local $line = getSpezLine($applevolume_default, $in{'delete_volumepath'});
	local $result = deleteSpezLine($applevolume_default, $line);
	if ($result == 0) {
		showMessage($text{'edit_delete_error'})
	}
}
else {
	die $text{'edit_volume_delete_error'};
}

redirect("index.cgi");
