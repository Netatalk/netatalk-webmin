#!/usr/bin/perl
# Form for editing netatalk configuration files directly
# 
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#	 Some code (C) 2011 by Steffan Cline <steffan@hldns.com>
#	 Some code based on proftpd admin pages
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

ui_print_header(undef, $text{'manual_configs'}, "", "configs", 1);

@files = (
	$config{'afpd_c'},
	$config{'afpdldap_c'},
	$config{'atalk_c'},
	$config{'applevolumedefault_c'},
	$config{'applevolumesystem_c'},
	$config{'netatalk_c'},
	$config{'papd_c'},
	$config{'pam_c'}
);
$in{'file'} = $files[0] if (!$in{'file'});

print qq|<form action="edit_configfiles_form.cgi">\n|;
print qq|<input type="submit" value="$text{'manual_file'}">\n|;
print qq|<select name="file">\n|;
foreach $f (@files) {
	printf "<option value=\"" . $f . "\"%s>%s</option>\n",
		$f eq $in{'file'} ? ' selected' : '', $f;
	$found++ if ($f eq $in{'file'});
	}
print "</select></form>\n";
$found || die $text{'manual_efile'};

print qq|<form action="edit_configfiles_save.cgi" method="post" enctype="multipart/form-data">\n|;
print qq|<input type="hidden" name="file" value="$in{'file'}">\n|;
print qq|<textarea name="data" rows="20" cols="80" style="width:75%">\n|;

open(FILE, $in{'file'});
while(<FILE>) { print &html_escape($_); }
close(FILE);

print "</textarea><br>\n";
print qq|<input type="submit" value="$text{'save'}">\n|;
print qq|</form>|;

print "<hr>\n";
ui_print_footer("index.cgi", $text{'index_module'});
