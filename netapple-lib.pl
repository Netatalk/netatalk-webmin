#!/usr/bin/perl
#Common function for editing the atalk config files

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Some code (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Contributions from:
#       Sven Mosimann <sven.mosimann@ecologic.ch>
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

# This module is almost all Sven's. I'm merging it into "the"
#  Netatalk webmin lib module. I've had to update it to the "new"
#  config file format, as it was using the older format.
# I've held off merging some of this, but it is on my TODO. Before this
#  module comes out of "BETA" I want ONE function module, not 2.

do '../web-lib.pl';
use File::Copy;
use CGI qw/:standard/;
&init_config("netapple");

#mgk: datei means "file"
$datei = $config{'applevolumedefault_c'};
$temp  = "$datei.temp";

$slash="/";
$pername = ();
$hostname= `hostname`;



#strcut volume_format verwaltet alle Informationen einer "Zeile"
#mgk: struct volume_format administers all information of a " line " 
use Class::Struct;
	struct  volume_format => {
		path=>'$',
		name=>'$',
		casefold=>'$',
		codepage=>'$',
		options=>'$',
		dbpath=>'$',
		password=>'$',
		allow=>'$',
		deny=>'$',
		rwlist=>'$',
		rolist=>'$',
	};

$|=1;

#damit users aufgelistet werden können
#mgk: so that users to be listed can
foreign_require("useradmin","user-lib.pl");


#-------------------------------------------------------------------------------------
#liest file AppleVolumes.default aus und durchfortset es nach
#mgk: file AppleVolumes.default picks out and through away set it after
#Infos
#-------------------------------------------------------------------------------------
sub open_afile
{
local(@rv,$line);

#mgk: File $datei not readable
open(FH,"<$datei") || die "$text{file} $datei $text{not_readable}";

while(defined($line = <FH>) )
{
	local($longName);
   	#Zeile mit Fortsetzungszeichen einlesen
	#mgk: Line with continuation characters read in
   	chomp $line;
   	if($line =~ s/\\$//  )
   	{
  		$line .=<FH>;
  		redo unless eof(FH);
    	}
    	#Zeile einlesen welche mit '~' oder '/' beginnen
	#mgk: Which read line in with ' ~ ' or ' / ' begin
    	if($line=~/^[$slash~]+/ )
    	{
      		#neue Klasse volume_format erzeugen
		#mgk: new class volume_format produces
      		my $volume = volume_format->new();
      		#home dir abfangen
		#mgk: home dir intercept
      		if($line =~ /^([~]+)/)
      		{
         		$volume->path($1);
         		$volume->name("Home directory");
         		push(@rv,$volume->name);
      		}
     		$count=0;
      		#alle anderes Dir abfangen
		#mgk: all other dir intercept
		#mgk: added '\$' to maintain compatibility
		#	with new format
      		while($line=~/([A-Za-z$slash"\$=~,-_.0-9]+)/g )
      		{
        		#PATH einlesen
			#mgk: path read in
        		if($count == 0)
        		{
       				##print "PATH: $1\n";
       				$volume->path($1);
       				if($1 eq "~"){
       					$count++;
       				}
        		}
        		#Dir Name einlesen
			#mgk: dir name read in
        		elsif($count == 1)
        		{
       				if($1 =~/^(["])/){
       				    #print"Line $line <br>\n";
       					if($line =~/"(.*?)"/){
       						#$volume->name($1);
       					    #print"INFO $1 <br>\n";
       					    $volume->name($1);
       						push(@rv,$1);
       					}
       				}
       				else{
       				$volume->name($1);
       				push(@rv,$1);
       				}
        		}	
        		#options    einlesen
			#mgk: options read in
			#mgk: Changed to the new ":" delimiter,
			#  added new allow,deny,rwlist,rolist options,
			#  added the '\$' to the allowable characters
      			elsif($1 =~/(\w+):([A-Za-z$slash\$@,.0-9]+)/)
       			{
      				if("casefold" eq $1){
      					$volume->casefold($2);	
      				}
      				elsif("codepage" eq $1){
      					$volume->codepage($2);	
      				}
      				elsif("options" eq $1){
      					$volume->options($2);	
      				}
      				elsif("allow" eq $1){
      					$volume->allow($2);	
      				}
				elsif("deny" eq $1){
                                        $volume->deny($2);
                                }
				elsif("rwlist" eq $1){
                                        $volume->rwlist($2);
                                }
				elsif("rolist" eq $1){
                                        $volume->rolist($2);
                                }
      				elsif("dbpath" eq $1){
      					$volume->dbpath($2);	
      				}
      				elsif("password" eq $1){
      					$volume->password($2);	
      				}
       			}
 			$count++;
     		}
     		#vorhandene Options in $volume schreiben
		#mgk: available options in $volume write
     		$pername{$volume->name} = $volume;
   	}
}
close(FH);
return @rv;
}

#------------------------------------------------------------------------------
#returns shareName
#------------------------------------------------------------------------------
sub getShareName
{
  my ($var1) = @_;
  $shareName = 1;
  if ($rp = $pername{$var1}){
	$shareName = $rp->name;
	
 }	
  return $shareName;
}

#------------------------------------------------------------------------------
#gibt Path zurück
#mgk: give Path back
#------------------------------------------------------------------------------
sub getPath
{
  	my ($var1) = @_;
  	$path =0;
  	if ($rp = $pername{$var1}){
		$path = $rp->path;
 	}	
  	return $path;
}

#------------------------------------------------------------------------------
#gibt casefold zurück
#mgk: give casefold back
#------------------------------------------------------------------------------
sub getCasfold
{
  	my ($var1) = @_;
  	$casefold = "";
  	if ($rp = $pername{$var1}){
		$casefold = $rp->casefold;
 	}	
  	return $casefold;
}

#------------------------------------------------------------------------------
#gibt Options zurück
#give options back
#------------------------------------------------------------------------------
sub getOptions
	{
  	my ($var1) = @_;
  	$Options ="";
  	if ($rp = $pername{$var1}){
		$Options = $rp->options;
 	}	
  	return $Options;
}

#------------------------------------------------------------------------------
#gibt Codepage zurück
#give codepage back
#------------------------------------------------------------------------------
sub getCodepage
	{
  	my ($var1) = @_;
  	$Codepage ="";
  	if ($rp = $pername{$var1}){
		$Codepage = $rp->codepage;
 	}	
  	return $Codepage;
}



#------------------------------------------------------------------------------
#gibt Access zurück
#give access back
#mgk: Updated and added 3 new funcs to allow for the new
#  allow/deny/rolist/rwlist format
#------------------------------------------------------------------------------

#mgk: legacy
sub getAccess { return getAllow(@_); }

sub getAllow
	{
  	my ($var1) = @_;
  	$Access ="";
  	if ($rp = $pername{$var1}){
		$Access = $rp->allow;
 	}	
  	return $Access;
}
sub getDeny
        {
        my ($var1) = @_;
        $Access ="";
        if ($rp = $pername{$var1}){
                $Access = $rp->deny;
        }
        return $Access;
}
sub getRwlist
        {
        my ($var1) = @_;
        $Access ="";
        if ($rp = $pername{$var1}){
                $Access = $rp->rwlist;
        }
        return $Access;
}
sub getRolist
        {
        my ($var1) = @_;
        $Access ="";
        if ($rp = $pername{$var1}){
                $Access = $rp->rolist;
        }
        return $Access;
}

#------------------------------------------------------------------------------
#gibt Access zurück
#mgk: give password back
#------------------------------------------------------------------------------
sub getPassword
	{
  	my ($var1) = @_;
  	$Password ="";
  	if ($rp = $pername{$var1}){
		$Password = $rp->password;
 	}	
  	return $Password;
}

#------------------------------------------------------------------------------
#gibt Database Path zurück
#mgk: give database path back
#------------------------------------------------------------------------------
sub getDatabase
	{
  	my ($var1) = @_;
  	$Database ="";
  	if ($rp = $pername{$var1}){
		$Database = $rp->dbpath;
 	}	
  	return $Database;
}


#------------------------------------------------------------------------------
#erfasst alle dateien im Verzeichnis /atalk/nls/
#mgk: enters all files in the directory /atalk/nls/
#------------------------------------------------------------------------------
sub getMacCodeFiles
{
    #local(@rv,@rs,$direntry,$realDir);
    #$near="/nls";
    #$dir=$config{'atalk_nls'};
    #$realDir=$config{'atalk_nls'};
    #opendir(DIR,$realDir);
    #foreach $direntry (readdir(DIR)){
    #next if $direntry eq ".";  #Sonderverzeichnisse
    #mgk: Special directories
	#next if $direntry eq ".."; #ignorieren
    #mgk: ignore
    #if(-f "$realDir/$direntry"){
    #push(@rv,"$realDir/$direntry");
    #}
    #}
    #closedir(DIR);
    local(@rv);
	return @rv;
}

#------------------------------------------------------------------------------
#überprüft ob angegebener Pfad existiert
#mgk: checked whether indicated path exists
#------------------------------------------------------------------------------
sub getPathOK
{
     	my ($var1) = @_;
     	local($rv);
     	$rv =0;
     	opendir(DIR,$var1);
     	if(readdir(DIR)){
     		$rv = "1";
     	}
     	closedir(DIR);
	return $rv;
}


#------------------------------------------------------------------------------
#listet alle users mit ID >=500 auf
#mgk: list all users with ID >=500
#------------------------------------------------------------------------------
sub getUsers
{
    	local(@rv);
    	@ulist  = foreign_call("useradmin","list_users");
    	for($i=0; $i<@ulist; $i++){
    		if( $ulist[$i]->{'uid'}> 499 || $ulist[$i]->{'uid'} eq 0){
    			$user= $ulist[$i]->{'user'};
    			push(@rv,$user);
    		}
     	}
     	return @rv;
}

#------------------------------------------------------------------------------
#listet alle Gruppen mit ID >=100auf   plus root mot gid = 0
#mgk: list all groups with ID >=100 and root gid == 0
#------------------------------------------------------------------------------
sub getGroups
{
	local(@rv);
	@glist = foreign_call("useradmin","list_groups");
	for($i=0; $i<@glist; $i++){
		if( $glist[$i]->{'gid'}> 99 || $glist[$i]->{'gid'} eq 0){
	   		$group = $glist[$i]->{'group'};
	   		push(@rv,$group);
	   	}	
	}
	return @rv;
}

#------------------------------------------------------------------------------
#schreibt neues File Share
#mgk: writes new file Share
#indem neue Zeile generiert wird oder Zeilen generiert werden
#mgk: as new line is generated or lines to be generated
#
#------------------------------------------------------------------------------
sub writeNewFileShare
{
	$space =" ";
	local($line_1,$line_2,$setSlash,$zeichen);
	#&ReadParse();
	my ($in) = @_;
	$zeichen='"';
	#homes oder anderer Path
	#mgk: homes or other Path
	if($in{homes}){
		$line_1 ="~ ";
	}
	else{
		$pathli = $in{path};
		if($pathli && 1 eq getPathOK($pathli)){
			$path = $in{path};
			$line_1 = $path;
			$line_1 .= " ";
		}
		else{
			showMessage($text{give_correct_path});
			return 0;	
		}
		#Share Name erfassen
		#mgk: Enter share name
		if($in{share}){
			 $sharename=$in{share};
			 $line_1.=$zeichen;
			 $line_1.=$sharename;
			 $line_1.=$zeichen;
			 $line_1.=" ";
			 #mgk: zeichen == characters
		}
		else{
			showMessage($text{indicate_sharename});
			return 0;
		}
	}
	#options einlesen---------------------
	#mgk: options read in
	if($in{casefold_options}  && $in{casefold_options} ne "default"){
		$caseFoldOption =$in{casefold_options};
		$line_1.="casefold:";
		$line_1.=$caseFoldOption;
	}
	if($in{codepage} && $in{codepage} ne "default"){
		$codePage =$in{codepage};
		$line_1.=" codepage:";
		$line_1.=$codePage;
	}
	if($in{misc_options}){
		$line_1.=" options:";
		foreach $name(param(misc_options)){
			@values = param(misc_options);
			$input_misc = join(',',@values);
		}
		$line_1.=$input_misc;
	}
	

	if($in{password}){
		$PassWord=$in{password};
		$line_1.=" password:";
		$line_1.=$PassWord;
	}
	if($in{dbpath}){
		$dataPath=$in{dbpath};
		$line_1.=" dbpath:";
		$line_1.=$dataPath;
	}
	#mgk: revamped the rest of this function to properly handle the
	#   newer format (allow/deny/rwlist/rolist)
	#Allow
	if($in{allow_users} || $in{allow_groups} ){
		$line_1.=" allow:";
		if($in{allow_users}){
		    $line_1.=join(',',split(/\s+/, $in{allow_users}));
		}
		#Komma zwischen Gruppen Users setzen
		#mgk: Comma between groups of users set
		if($in{allow_users} && $in{allow_groups} ){
			$line_1.=",@";
		} elsif($in{allow_groups}) {
			#mgk: added to handle other case
			$line_1.="@";
		}
		if($in{allow_groups}){
			$line_1.=join(',@',split(/\s+/,$in{allow_groups}));
		}
	}
        #Deny
        if($in{deny_users} || $in{deny_groups} ){
                $line_1.=" deny:";
                if($in{deny_users}){
                    $line_1.=join(',',split(/\s+/, $in{deny_users}));
                }
                #Komma zwischen Gruppen Users setzen
                #mgk: Comma between groups of users set
                if($in{deny_users} && $in{deny_groups} ){
                        $line_1.=",@";
                } elsif($in{deny_groups}) {
                        #mgk: added to handle other case
                        $line_1.="@";
                }
                if($in{deny_groups}){
                        $line_1.=join(',@',split(/\s+/,$in{deny_groups}));
                }
        }
        #rolist
        if($in{rolist_users} || $in{rolist_groups} ){
                $line_1.=" rolist:";
                if($in{rolist_users}){
                    $line_1.=join(',',split(/\s+/, $in{rolist_users}));
                }
                #Komma zwischen Gruppen Users setzen
                #mgk: Comma between groups of users set
                if($in{rolist_users} && $in{rolist_groups} ){
                        $line_1.=",@";
                } elsif($in{rolist_groups}) {
                        #mgk: added to handle other case
                        $line_1.="@";
                }
                if($in{rolist_groups}){
                        $line_1.=join(',@',split(/\s+/,$in{rolist_groups}));
                }
        }
        #rwlist
        if($in{rwlist_users} || $in{rwlist_groups} ){
                $line_1.=" rwlist:";
                if($in{rwlist_users}){
                    $line_1.=join(',',split(/\s+/, $in{rwlist_users}));
                }
                #Komma zwischen Gruppen Users setzen
                #mgk: Comma between groups of users set
                if($in{rwlist_users} && $in{rwlist_groups} ){
                        $line_1.=",@";
                } elsif($in{rwlist_groups}) {
                        #mgk: added to handle other case
                        $line_1.="@";
                }
                if($in{rwlist_groups}){
                        $line_1.=join(',@',split(/\s+/,$in{rwlist_groups}));
                }
        }
	writeLine( $line_1 ,$line_2);	
}

#------------------------------------------------------------------------------
#schreibt neue Zeile in AppleVolumes.default
#mgk: new line writes in AppleVolumes.default
#
#var1 erste Linie welche zu schreiben ist
#mgk: var1 first line to write
#var2 zweite Linie welche zu schreiben ist
#mgk: var2 second line to write
#solle keine zweite geschrieben werden Linie ,var2="    " übergeben
#mgk: no second line, var2 = " " is to be written transferred
#-----------------------------------------------------------------------------
sub writeLine()
{
	my ($var1,$var2) = @_;
        @line = getLines($datei);
	copy($datei,$temp)
	or die "$text{copy_failed}: $!";

	&lock_file("$temp");
	open(OLD,"<$datei") || die "$text{file} $datei $text{not_readable}";
	open(NEW,">$temp") || die "$text{file} $temp $text{not_readable}";

	while(<OLD>){
  		if($.== @line[0]){
  		#if($.== 17){
  		print NEW  "$var1\n";
  		}
  		print NEW $_;
	}
	close(OLD);
	close(NEW);
	&unlock_file("$temp");

	#umbenans
	rename($datei,"$datei.orig");
	rename($temp,$datei);
	#löschen der Datei    AppleVolumes.sven.old
	#mgk: delete the file AppleVolumes.sven.old
	unlink("$datei.orig") or die "$text{delete_failed}: $datei.orig\n";
}


#------------------------------------------------------------------
#löscht eine bestimmte Zeile in File
#mgk: deletes a certain line in file
#mgk:
#$var1 =>Datei
#mgk: $var1 => File
#$var2 =>Anfang der Zeile, welche gefunden werden soll (sprich Verzeichnis)
#mgk: var2 => Start of the line, which is to be found (speak directory) 
#------------------------------------------------------------------
sub deleteLine(){
	my ($var1,$var2) = @_;
	local($counter,$lines);
	if( ! defined $var1){
		return 0;
	}
	if( ! defined $var2){
		return 0;
	}

        @lines = getLines($datei,$var2);
        copy( $datei , $temp)
	or die "$text{copy_failed}: $!";

        &lock_file("$temp");
	open(OLD,"<$datei") || die "$text{file} $datei $text{not_readable}";
	open(NEW,">$temp")  || die "$text{file} $datei $text{not_readable}";

	$counter =0;
	while(<OLD>){
 		if($counter != @lines[0] && $counter != @lines[1] ){
  			print NEW $_;
  		}
  		$counter++;
  		
	}
	close(OLD);
	close(NEW);
        &unlock_file("$temp");

	#umbenans
	rename($datei,"$datei.orig");
	rename($temp,$datei);
	#löschen der Datei  AppleVolumes.sven.old
	#mgk: Delete the file AppleVolumes.sven.old
	unlink("$datei.orig") or die "$text{delete_failed}: $datei.orig\n";
	return 1;
	
}


#------------------------------------------------------------------
#Seite, welche einen Eingabefehler anzeigen soll
#mgk: Page, which displays input error
#
#$var1 Info-Text
#------------------------------------------------------------------

sub showMessage
{
	my ($var1) = @_;
	&header("Warning", "");
	print "<h2>****  $var1  ***</h2>\n";
	&footer("","Share List");
}

#------------------------------------------------------------------
#Funktion zum erfassen der maximalen zulässigen user
# in file atalk
#mgk: Function to enter the max. admissible user
#
#------------------------------------------------------------------

sub getMaxUser
{
	local(@rv,$config, @rv);

	$config = $config{'netatalk_c'};
	push(@rv,"0");

	open(OLD,"<$config") || die "$text{file} $config $text{not_readable}";
	while (<OLD>) {
        if ($_ =~ /AFPD_MAX_CLIENTS=\([0-9]*\)/ ) {
            shift(@rv);
            push(@rv,$1);
        }
    }
	close(OLD);
	return @rv;
}


#------------------------------------------------------------------
#Funktion liest File afpd.conf ein und speichert Infos in struct
#afpd in array @afpd[server,tcp(tcp,notcp),ddp(ddp,noddp),port,address]
# in file atalk
#mgk:Function reads file in afpd.conf and stores
#
#------------------------------------------------------------------
sub readAfpd
{
	local($fileToRead,$zeichen1,@afpd,@afpd_all);
	local($notcp,$nodpp,$port,$address,$logimMessage,$savepass,$setpass);
	push(@afpd_all,1);
	$hostname= `hostname`;
	$zeichen1='-';
	$notcp="-notcp";$nodpp="-noddp",$port="-port";$address="-address";
	$logimMessage="-loginmesg";$savepass="savepassword";$setpass="setpassword";
	$fileToRead = $config{'afpd_c'};
	open(FH,"<$fileToRead") || die "$text{file} $fileToRead $text{not_readable}";
	while(<FH>)
	{
   	#Zeile mit Fortsetzungszeichen einlesen
	#mgk: Line with continuation characters read in
    	if($_=~/(^[0-9A-Za-z$zeichen1"].*)/  ){
    		#print "$1 <br>\n";
    		@afpds = ($hostname,"-tcp","-ddp","-","-");
    			#server auslesen
			#mgk: servers select
    		
    		if($1 =~ /^(\w+)/)  {
    			@afpds[0]=$1;
    			#print"Servername $1 <br> \n";
    		}
    		if($_ =~ /$notcp/){
    		 	@afpds[1]=$notcp;
    		}
    		
    		if($_ =~ /$nodpp/){
    		 	@afpds[2]=$nodpp;
    		}
    		if($_ =~ /$port\s*([0-9]*)/){
    		 	@afpds[3]=$1;
    		}
    		if($_ =~ /$address\s*([0-9.]*)/){
    		 	@afpds[4]=$1;
    		}
    		push(@afpd_all,@afpds);
    	}
    }	
	close(FH);
	return @afpd_all;
}





#------------------------------------------------------------------
#Funktion liest File afpd.conf ein und speichert Infos in struct
#afpd in array @afpd[server,tcp(tcp,notcp),ddp(ddp,noddp),port,address]
# in file atalk
#mgk: Function reads file in afpd.conf and stores
#
#------------------------------------------------------------------
sub getAllAfpd
{
	local($fileToRead,$zeichen1,@afpd,@afpd_all);
	local($notcp,$nodpp,$port,$address,$logimMessage,$savepass,$setpass);
	push(@afpd_all);
	$hostname= `hostname`;
	$zeichen1='-';
	$notcp="-notcp";$nodpp="-noddp",$port="-port";$address="-address";
	$logimMessage="-loginmesg";$savepass="savepassword";$setpass="setpassword";
	$fileToRead = $config{'afpd_c'};
	open(FH,"<$fileToRead") || die "Datei $fileToRead nicht einlesbar";
	while(<FH>)
	{
   	#Zeile mit Fortsetzungszeichen einlesen
	#mgk: Line with continuation characters read in
    	if($_=~/(^[0-9A-Za-z$zeichen1"].*)/  ){
    		#print "$1 <br>\n";
    		@afpd = ($hostname,"-tcp","-ddp","-","-","","-","-");
    			#server auslesen
			#mgk: servers select
    		
    		if($1 =~ /^(\w+)/)  {
    			@afpd[0]=$1;
    		}
    		if($_ =~ /$notcp/){
    		 	@afpd[1]=$notcp;
    		}   		
    		if($_ =~ /$nodpp/){
    		 	@afpd[2]=$nodpp;
    		}
    		if($_ =~ /$port\s*([0-9]*)/){
    		 	@afpd[3]=$1;
    		}
    		if($_ =~ /$address\s*([0-9.]*)/){
    		 	@afpd[4]=$1;
    		}
    		if($_ =~ /$logimMessage\s*"(.*?)"/){
    		 	@afpd[5]=$1;
    		}
    		if($_ =~ /$savepass/){
    		 	@afpd[6]=$savepass;
    		}
    		if($_ =~ /$setpass/){
    		 	@afpd[7]=$setpass;
    		}
    		push(@afpd_all,@afpd);
    	}
    }	
	close(FH);
	return @afpd_all;
}


#------------------------------------------------------------------------------
#Funktion hängt eine neue Linie an file
#mgk: Function hangs a new line on file
#
#
#$var1 Linie die hinzugefügt wird
#mgk: var1 Line is added
#$var2 File an das Linie angehängt werden soll
#mgk: var2 File at line should be attached
#------------------------------------------------------------------------------
sub addLineToFile()
{
	my ($var1,$var2) = @_;
	local($temporary,$lin);
    	$lin = getLinesSpezFile($var1);
 	$temporary = "$var1.temp";

	copy($var1,$temporary) or die "$text{copy_failed}: $!";

	lock_file("$temporary");
	open(OLD,"<$var1") || die "$text{file} $var1 $text{not_readable}";
	open(NEW,">$temporary") || die "$text{file} $temporary $text{not_readable}";

	while(<OLD>){
	
		print NEW $_;
  		if($.== $lin){
  			print NEW  "$var2\n";
  		}
  		
	}
	close(OLD);
	close(NEW);
	unlock_file("$temporary");
	#umbenans
	rename($var1,"$var1.orig");
	rename($temporary,$var1);
	#löschen der Datei    AppleVolumes.sven.old
	#mgk: Delete file AppleVolumes.sven.old
	unlink("$var1.orig") or die "$text{delete_failed}: $var1.orig\n";
}

#------------------------------------------------------------------
#gibt die Anzahl Zeilen des angeben Files zurück oder einer bestimmten Zeile
#mgk: gives the number of lines, indicates files back or to a certain line
#
#$var1 File das zu öffenen ist
#$var2 Linie, von welcher die ZeilenNummer zu ermitteln ist
#mgk:  Line, from which the line number is to determine
#------------------------------------------------------------------
sub getLines(){
	my ($var1,$var2,$var3) = @_;
	local($counter,$output,@rv);
	$counter = 0;$output = 1;
	#Testen ob die Varibel übergeben worden ist
	#mgk: Tests whether the variable transferred(?)
	if( ! defined $var1){
		return 0;
	}
	#Testen ob die zweite
	#mgk: Tests the second
	elsif( ! defined $var2){
	      open(FH,"<$var1") || die return 0;
			while(defined($line = <FH>) ){
 				if($line=~/^[$slash~]+/ ){
 					push(@rv,$output);
 				}
 				$output++;
	      }
	}
	else{
		open(FH,"<$var1") || die return 0;
	      	while(defined($line = <FH>) )
	      	{
 				if($line=~/^[$slash~]+/ ){
					if($line =~ /([A-Za-z$slash=~,-_\\]+)/){
 						if($1 =~ /$var2/){
 							$output = $counter;
 							push(@rv,$output);
 							$output++;
							if($line =~ /[\\]/){
								push(@rv,$output);
 							}
 							else{
 								push(@rv,-1);
							}
 						}		
 					}
     			}	
 				$counter++;	
	      	}
	}
	return @rv;	
}

#------------------------------------------------------------------
#löscht eine bestimmte Zeile in File
#mgk: deletes a certain line in file
#$var1 =>Datei
#mgk:    File
#$var2 =>Anfang der Zeile, welche gefunden werden soll (sprich Verzeichnis)
#mgk:    Start of the line, which is to be found (speak directory)
#------------------------------------------------------------------
sub deleteSpezLine(){
	my ($var1,$var2) = @_;
	local($temporary);
	if( ! defined $var1){
		return 0;
	}
	if( ! defined $var2){
		return 0;
	}
	$line = getSpezLine($var1,$var2);
	$temporary="$var1.temp";
        #print "Lines :  @lines[1]   @lines[0]<br>\n";
 	copy($var1, $temp)
		or die "$text{copy_failed}: $!";

	lock_file("$temporary");
	open(OLD,"<$var1") || die "$text{file} $datei $text{not_readable}";
	open(NEW,">$temporary")  || die "$text{file} $temp $text{not_readable}";
	while(<OLD>){
	
 		if($. != $line ){
  			print NEW $_;
  		}
	}
	close(OLD);
	close(NEW);
	unlock_file("$temporary");
	#umbenans
	rename($var1,"$var1.orig");
	rename($temporary,$var1);
	#löschen der Datei    AppleVolumes.sven.old
	#mgk: delete the file
	unlink("$var1.orig") or die "$text{delete_failed}: $var1.orig\n";
	return 1;
	
}

sub getSpezLine
{
	my ($var1,$var2) = @_;
	local($counter,$outputli);
	$counter = 0;
	open(OLD,"<$var1") || die "$text{file} $datei $text{not_readable}";
	while(<OLD>){
		$counter++;
 		if($_ =~ /^$var2/ ){
 			$outputli=$counter;
  		}
	}
	close(OLD);
	return $outputli;
}


#-------------------------------------------------------------------------------
#Funktion ermittelt Anzahl Linien eines Files
#mgk: Function determines number of lines of the files
#
#$var1 File das auszulesen ist
#mgk: $var1 is the file
#-------------------------------------------------------------------------------
sub getLinesSpezFile() {
	my ($var1) = @_;
	local($counting);
	$counting = 0;
	#Testen ob die Varibel übergeben worden ist
	#mgk: Test the file
	open(FileHandle,"<$var1") || die return 0;
	while(<FileHandle>){
		$counting++;
	}
	close(FileHandle);
	return $counting;
}

sub getHostName(){
	return $hostname;
}


