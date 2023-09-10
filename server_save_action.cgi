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

use CGI qw/:standard/;
require './netapple-lib.pl';

&ReadParse();
	
$hostname = getHostName();
$filetoedit = $config{'afpd_c'};
if($in{old_servername}){
	$server = $in{old_servername};
	$server =~  /$hostname*/  ? $server="-" : "" ;
}

deleteSpezLine($filetoedit ,$server);
createNewLine();
addLineToFile($filetoedit);

&redirect("servers.cgi");

#-----------------------------------------------------------------------------
# Function creates new line with entry for servers
# in afpd.conf
#
#-----------------------------------------------------------------------------
sub createNewLine(){
	local($newString);
	if($in{server}){
		$newString="- ";
	}
	else{
		if($in{servername}){
			 $newString=$in{servername};
			 $newString.="  ";
		}
		else{
			error($text{'save_newServer_errorMessage'});
		}
	}
	if($in{tcpip}){
		$newString.=$in{tcpip};
		$newString.=" ";
	}
	if($in{ddp}){
		$newString.=$in{ddp};
		$newString.=" ";
	}
	if($in{port}){
		$newString.="-port ";
		$newString.=$in{port};
		$newString.=" ";
	}
	if($in{address}){
		$newString.="-ipaddr ";
		$newString.=$in{address};
		$newString.=" ";
	}
	if($in{savepassword}){
		$newString.="$in{savepassword}";
		$newString.=" ";
	}
	if($in{setpassword}){
		$newString.=$in{setpassword};
		$newString.=" ";
	}
	if($in{logmesg}){
	    $newString.="-loginmesg \"";
		$newString.=$in{logmesg};
		$newString.="\" ";
	}
	addLineToFile($filetoedit,$newString);
}
