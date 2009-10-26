#!/usr/bin/perl
# restart.cgi
# Kill all smbd and nmdb processes and re-start them

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

require './netapple-lib.pl';

@atalkpids = &find_byname("atalkd");
kill('TERM', @atalkpids );

$rv = system("$config{atalkd_d} </dev/null");
if ($rv) { &error(&text('restart_failed', $config{atalkd_d})); }
&redirect("");

