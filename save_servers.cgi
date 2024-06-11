#!/usr/bin/perl
# Save a new or edited server configuration

#    Netatalk Webmin Module
#    Copyright (C) 2000 Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Copyright (C) 2000 Matthew Keller <kellermg@potsdam.edu>
#    Copyright (C) 2023-4 Daniel Markstedt <daniel@mindani.net>
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

local $filetoedit = $config{'afpd_c'};
local $totalLines = getLinesSpezFile($filetoedit);
local $lineNumber = 1;

if($in{'old_servername'}) {
	$lineNumber = getSpezLine($filetoedit, $in{'old_servername'});
	local $result = deleteSpezLine($filetoedit, $lineNumber);
	if ($result == 0) {
		showMessage($text{'edit_delete_error'})
	}
} else {
	$lineNumber = getLinesSpezFile($filetoedit);
}

local $serverLine = createNewServerLine($in);

if ($serverLine ne 0) {
	addLineToFile($filetoedit, $serverLine, $lineNumber, $totalLines);
}

redirect("index.cgi");
