#!/usr/bin/perl
# Display netatalk help text
#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
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
#

do '../../web-lib.pl';

&header("Configurations Help", "", undef(), 1, 1);

print qq|<a href="https://netatalk.sourceforge.io/2.2/htmldocs/">Click here to go to the Netatalk 2 Manual</a>|;
