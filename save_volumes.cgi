#!/usr/bin/perl
# Action for saving a new or edited file share

#    Netatalk Webmin Module
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

require 'netatalk2-lib.pl';

&ReadParse();

my $applevolume_default = $config{'applevolumedefault_c'};
my $totalLines = getLinesSpezFile($applevolume_default);
my $lineNumber = 1;

if ($in{oldpath}) {
	$lineNumber = getSpezLine($applevolume_default, $in{'oldpath'});
	my $result = deleteSpezLine($applevolume_default, $lineNumber);
	if ($result == 0) {
		showMessage($text{'edit_delete_error'})
	}
} else {
	$lineNumber = getLinesSpezFile($applevolume_default);
}

if ($in{default_options}) {
	$lineNumber = getSpezLine($applevolume_default, ":DEFAULT:");
	if ($lineNumber) {
		my $result = deleteSpezLine($applevolume_default, $lineNumber);
		if ($result == 0) {
			showMessage($text{'edit_delete_error'})
		}
	}
	else {
		$lineNumber = 1;
	}
}

my $fileShareLine = createNewFileShare($in);

if ($fileShareLine ne 0) {
	addLineToFile($applevolume_default, $fileShareLine, $lineNumber, $totalLines);
}

redirect("index.cgi");
