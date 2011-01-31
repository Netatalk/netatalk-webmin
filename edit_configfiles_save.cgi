#!/usr/bin/perl
# edit_configfiles_save.cgi
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

require './netapple-lib.pl';

&ReadParseMime();

@files = ($config{'netatalk2_c'},$config{'netatalk_c'},$config{'afpd_c'},$config{'afpdldap_c'},$config{'atalk_c'},$config{'papd_c'},$config{'applevolumedefault_c'},$config{'applevolumesystem_c'});
&indexof($in{'file'}, @files) >= 0 || &error( $in{'file'} );

$temp = &transname();
system("cp ".quotemeta($in{'file'})." $temp");
$in{'data'} =~ s/\r//g;
&open_lock_tempfile(FILE, ">$in{'file'}");
&print_tempfile(FILE, $in{'data'});
&close_tempfile(FILE);
if ($config{'test_manual'}) {
	$err = &test_config();
	if ($err) {
		system("mv $temp ".quotemeta($in{'file'}));
		&error(&text('manual_etest', "<pre>$err</pre>"));
		}
	}
unlink($temp);
&redirect("");
