#!/usr/bin/perl
# edit_fshare.cgi
# Display a form for editing or creating a new directory share

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

require './netapple-lib.pl';

$path="NoPath";
$s="homes";

&header("Delete Apple File Share", "");

print"<p><p>\n";


print "<hr>\n";
print"<p><p>\n";
print "<form action=delete_FShare.cgi>\n";

print"<h4>Select File Share</h4>\n";

print"<select  name=delete> \n";
foreach $s (open_afile())
{
	$shareName=  getShareName($s);
	$Path     = getPath($s);
	$show     = "$shareName &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp $Path";
	
	print "<option value=$Path> $show\n";
}

print"</select>\n";


print "<input type=submit value=delete> </form>\n";

print "<hr>\n";
print"<p><p>\n";
&footer("","Share List");
