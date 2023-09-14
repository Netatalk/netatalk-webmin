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
	$server =~ /$hostname*/ ? $server="-" : "" ;
}

deleteSpezLine($filetoedit ,$server);
createNewLine();

&redirect("servers.cgi");

#-----------------------------------------------------------------------------
# Function creates new line with entry for servers
# in afpd.conf
#
#-----------------------------------------------------------------------------
sub createNewLine(){
	local($newString);
	if($in{server}){
		$newString = "- ";
	}
	else{
		if($in{servername}){
			if($in{servername} =~ /[:@]/){
				showMessage($text{error_illegal_char});
				return 0;
			}
			$newString = "\"$in{servername}\" ";
		}
		else{
			error($text{'save_newServer_errorMessage'});
		}
	}
	if($in{tcpip} eq "-tcp" && $in{ddp} eq "-ddp"){
		$newString .= "-transall ";
	}
	else{
		$newString .= "$in{ddp} $in{tcpip} ";
	}
	if($in{port}){
		$newString .= "-port $in{port} ";
	}
	if($in{address}){
		$newString .= "-ipaddr $in{address} ";
	}
	$newString .= "$in{savepassword} ";
	$newString .= "$in{setpassword} ";
	if($in{logmesg}){
		$newString .= "-loginmesg \"$in{logmesg}\" ";
	}
	if($in{uams}){
		$in{uams} =~ s/\x00/\,/g;
		$newString .= "-uamlist $in{uams} ";
	}
	$newString .= "$in{icon} ";
	if($in{mimicmodel}){
		$newString .= "-mimicmodel \"$in{mimicmodel}\" ";
	}
	addLineToFile($filetoedit,$newString);
}
