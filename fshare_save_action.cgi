#!/usr/bin/perl
# Action for saving a new or edited file share

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

&ReadParse();

local $totalLines = getLinesSpezFile($applevolume_default);
local $lineNumber = 1;

if ($in{oldpath}) {
	$lineNumber = getSpezLine($applevolume_default, $in{'oldpath'});
	local $result = deleteSpezLine($applevolume_default, $lineNumber);
	if ($result == 0) {
		showMessage($text{'edit_delete_error'})
	}
} else {
	$lineNumber = getLinesSpezFile($applevolume_default);
}

if ($in{default_options}) {
	$lineNumber = getSpezLine($applevolume_default, ":DEFAULT:");
	if ($lineNumber) {
		local $result = deleteSpezLine($applevolume_default, $lineNumber);
		if ($result == 0) {
			showMessage($text{'edit_delete_error'})
		}
	}
	else {
		$lineNumber = 1;
	}
}

local $fileShareLine = createNewFileShare($in);

if ($fileShareLine ne 0) {
	addLineToFile($applevolume_default, $fileShareLine, $lineNumber, $totalLines);
}

redirect("index.cgi");
