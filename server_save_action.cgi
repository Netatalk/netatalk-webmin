#!/usr/bin/perl
# Save a new or edited server configuration

#    Netatalk Webmin Module
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Some code (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
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

$filetoedit = $config{'afpd_c'};

if($in{old_servername}) {
	$lineNumber = (getSpezLine($filetoedit, $in{old_servername}) - 1);
	deleteSpezLine($filetoedit, $in{old_servername});
} else {
	$lineNumber = (getLinesSpezFile($filetoedit));
}

local $serverLine = createNewServerLine($in);
addLineToFile($filetoedit, $serverLine, $lineNumber);

redirect("index.cgi");
