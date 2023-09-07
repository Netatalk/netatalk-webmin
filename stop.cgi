#!/usr/bin/perl
# restart.cgi
# Kill all smbd and nmdb processes and re-start them

#    Netatalk Webmin Module
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Some code (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#	 Some code (C) 2011 by Steffan Cline <steffan@hldns.com>
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

require './netapple-lib.pl';

$rv = system("$config{stop_netatalk} </dev/null");
if ($rv) { die &text('init_failed', $config{stop_netatalk}); }

&redirect("");

