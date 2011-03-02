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

$afpd_path= $config{'afpd_d'};     #"/usr/sbin/afpd";
$start="startproc";
$currentString ="\t";
$zeichen="/";
$zeichen2='$';

$atalk_datei=$atalk_old= $config{'netatalk_c'};
$atalk_temp = "$atalk_datei.temp";

&ReadParse();

if($in{maxClients}){
	$maxusers = $in{maxClients};
	#getLinetoModify();
	writeAtalkLine($maxusers);
}

&redirect("misc_opt.cgi");

#-------------------------------------------------------------------------------
#schreibt neue Anzahl max users in File atalk
# mgk: write new max users to file atalk
#
#
#$var1 = Anzahl users
# mgk: = max users
#------------------------------------------------------------------------------
sub writeAtalkLine()
{
	my ($var1) = @_;
	local($lineNumber,$newString,$lineNumbertoModify);
	if( ! defined $var1){
		return 0;
	}
	$lineNumbertoModify = 0;
	$lineNumbertoModify = getAtalkLinetoModify();
	#print"Debug Output $lineNumbertoModify \n";
	$newString =newString($lineNumbertoModify,$var1);
	#print"Debug Output $newString \n";
	deleteAtalkLine($atalk_datei,$lineNumbertoModify);
	#da eine linie fehlt eine
	#$lineNumbertoModify--;
	
	#name der temporär Datei
	# mgk: temporary file

    	#Kopie anegen
	# mgk: copy again

	copy( $atalk_datei , $atalk_temp)	or die "$text{copy_failed}: $!";
	#erfassen der Zeile welche geändert werden sol

	lock_file("$atalk_temp");
	open(OLD,"<$atalk_datei") || die "$text{file} $atalk_datei $text{not_readable}";
	open(NEW,">$atalk_temp") || die "$text{file} $atalk_temp $text{not_readable}";

	while(<OLD>){
  		if($.eq $lineNumbertoModify ){
  			print NEW  "\t$newString\n";
#  		if($var2 ne "    "){
#  			print NEW  "$var2\n";
#  		}
 		}
  		print NEW $_;
	}
	close(OLD);
	close(NEW);
	unlock_file("$atalk_temp");

	#umbenans
	rename($atalk_datei,"$atalk_datei.orig");
	rename($atalk_temp,$atalk_datei);
	#löschen der Datei    AppleVolumes.sven.old
	unlink("$atalk_datei.orig") or die "$text{delete_failed}\n";
}


#--------------------------------------------------
#Erfassen der Zeile, welche neuen Eintrag benötigt
#mgk: Enter the line, which the new entry needs
#
#keine Parameter übergabe alle benötigten sind global
#mgk: no parameters are transfered. All necessary are global
#return value Linien-Number
#mgk: Return value is the line number
#--------------------------------------------------
sub getAtalkLinetoModify
{
	local($count,$lines,$connections);
	$connections="-c";
	$count = 0;$lines =0;
	open(OLD,"<$atalk_old") || die "$text{file} $atalk_old $text{not_readable}";
	while(<OLD>)
	{
		#eine Zeile mehr
		$count++;
		if($_ =~ /$afpd_path/ && /$start/){
			$lines = $count;
		}
	}
	close(OLD);
	return $lines;
}

#-----------------------------------------------------------
#Methode kreiert neuen String der die Anzahl users definiert
#mgk: Method creates new string that is the number of users defined
#
#
#$var1 Zeilen Nummer welche editert werden soll
#mgk:  Lines number which should be editted
#$var2 max users
#return neuer String
#mgk: return new string
#-----------------------------------------------------------
sub newString
{
	my ($var1,$var2) = @_;
	local($currentString,$maxUsers,$line);
	if( ! defined $var1){
		return 0;
	}
	if( ! defined $var2){
		return 0;
	}
	$maxUsers = getUsers();
	open(OLD,"<$atalk_old") || die "$text{file} $atalk_old $text{not_readable}";
	
	$. =0;
	do {$line = <OLD>} until $. eq $var1 || eof;
	while($line=~/([A-Za-z0-9$zeichen$zeichen2|=-]*)/g){
			if($afpd_path  eq $1){
				$currentString.="$afpd_path -c $var2";
				$currentString.=" ";	
			}
			elsif($1 ne "" && $1 ne $afpd_path && $1 ne "-c" && $1 ne "$maxUsers"){
				$currentString.=$1;
				$currentString.=" ";
			}
	}
	close(OLD);
	return $currentString;	
}

#------------------------------------------------------------------
#löscht eine bestimmte Zeile in File
#mgk: deletes a certain line in file
#$var1 =>Datei
#mgk:    file
#$var2 =>Zeilen NR, welche gelöscht werden soll
#mgk:    Lines which should be deleted
#------------------------------------------------------------------
sub deleteAtalkLine(){
	my ($var1,$var2) = @_;
	local($counter,$lines);
	if( ! defined $var1){
		return 0;
	}
	if( ! defined $var2){
		return 0;
	}
        #print "Lines :  @lines[1]   @lines[0]<br>\n";
        copy( $var1 , $atalk_temp)
	or die "$text{copy_failed}: $!";

	lock_file("$atalk_temp");	
	open(OLD,"<$atalk_datei") || die "$text{file} $atalk_datei $text{not_readable}";
	open(NEW,">$atalk_temp")  || die "$text{file} $atalk_temp $text{not_readable}";
	$counter =0;
	while(<OLD>){
		$counter++;
 		if($counter != $var2 ){
  			print NEW $_;
  		}
	}
	close(OLD);
	close(NEW);
	unlock_file("$atalk_temp");

	#umbenans
	rename($atalk_datei,"$atalk_datei.orig");
	rename($atalk_temp,$atalk_datei);
	#löschen der Datei    AppleVolumes.sven.old
	# mgk: delete file
	unlink("$atalk_datei.orig") or die "$text{delete_failed}\n";
	return 1;
}

sub getUsers
{
	local($users,$connections,$users);
	$connections="-c";
	$users=0;
	open(OLD,"<$atalk_datei") || die "$text{file} $atalk_datei $text{not_readable}";
	while(<OLD>)
	{
		if($_ =~ /$afpd_path/ && /$start/)
		{
			if($_ =~/$connections\s*([0-9]*)/){
				#shift(@rv);
				$users=$1;
			}
		}
	}
	return $users;
	close(OLD);
}


