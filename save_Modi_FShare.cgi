#!/usr/bin/perl
# save_fshare.cgi
# Save a new or edited file share

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

use CGI qw/:standard/;
require './netapple-lib.pl';
&ReadParse();

#test ob pfad existiert
#mgk: test whether the path exists
$all=$in;$ok =0;
if($in{path}){
	$pathli = $in{path};
	$ok =  getPathOK($pathli);
	if($ok ne 1){
		showMessage ("$text{not_valid_path}");
	}
}
else{
	showMessage ("$text{no_path}");
}

if($in{oldpath} && $ok eq 1){
		$info =  $in{oldpath};
		deleteLine($datei,$info);
		writeNewFileShare($in);
		
}
&redirect("");



