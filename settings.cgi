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
do '../web-lib.pl';
#do './netapple-lib.pl';
use File::Copy;
&init_config("netapple");

$afpd_path = $config{'afpd_d'};
$config = $config_old= $config{'netatalk_c'};
$config_temp = "$atalk_datei.temp";

&ReadParse();

if($in{maxClients}){
	$maxusers = $in{maxClients};
	writeMaxUsersLine($maxusers);
}

&redirect("misc_opt.cgi");

#-------------------------------------------------------------------------------
# mgk: write new max users to file atalk
#
# $var1 = Anzahl users
# mgk: = max users
#------------------------------------------------------------------------------
sub writeMaxUsersLine()
{
	my ($var1) = @_;
	local($lineNumber,$newString,$lineNumbertoModify);
	if( ! defined $var1){
		return 0;
	}

	copy($config , $config_temp) or die "$text{copy_failed}: $!";
	lock_file("$config_temp");
	open(OLD,"<$config") || die "$text{file} $config $text{not_readable}";
	open(NEW,">$config_temp") || die "$text{file} $config_temp $text{not_readable}";

	while (<OLD>){
  		if ($_ =~ /AFPD_MAX_CLIENTS/ ){
  			print NEW "AFPD_MAX_CLIENTS=$var1\n";
 		}
  		print NEW $_;
	}
	close(OLD);
	close(NEW);
	unlock_file("$config_temp");
	rename($config,"$config.orig");
	rename($config_temp, $config);
	unlink("$config.orig") or die "$text{delete_failed}\n";
}
