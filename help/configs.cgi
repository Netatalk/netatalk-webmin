#!/usr/bin/perl
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

print qq|<iframe id="helppane" width="100%" height="75%" src="http://netatalk.sourceforge.net/2.1/htmldocs/"></iframe>|;

&footer("../index.cgi",$text{'index'});

