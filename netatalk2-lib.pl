#!/usr/bin/perl
# Common functions for manipulating the netatalk config files

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Some code (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Contributions from:
#       Sven Mosimann <sven.mosimann@ecologic.ch>
#       Daniel Markstedt <daniel@mindani.net>
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

# TODO: Figure out how to avoid importing web-lib.pl explicitly here...
#       It should be part of WebminCore imports
do '../web-lib.pl';
BEGIN { push(@INC, ".."); };
use WebminCore;
use File::Copy;
use CGI qw/:standard/;
init_config();

$applevolume_default = $config{'applevolumedefault_c'};
$temp = "$applevolume_default.temp";

$slash = "/";
$pername = ();
$hostname = `hostname`;

#struct volume_format administers all information of a " line " 
use Class::Struct;
	struct  volume_format => {
		path=>'$',
		name=>'$',
		all_options=>'$',
		options=>'options_format',
	};

	#note: deliberately skipped preexec/postexec/root_preexec/root_postexec
	#these are dangerous options that should not be used
	struct  options_format => {
		adouble=>'$',
		volsizelimit=>'$',
		allow=>'$',
		deny=>'$',
		allowed_hosts=>'$',
		denied_hosts=>'$',
		cnidscheme=>'$',
		dbpath=>'$',
		cnidserver=>'$',
		ea=>'$',
		maccharset=>'$',
		options=>'$',
		password=>'$',
		perm=>'$',
		fperm=>'$',
		dperm=>'$',
		umask=>'$',
		rolist=>'$',
		rwlist=>'$',
		veto=>'$',
		volcharset=>'$',
		casefold=>'$',
	};

$|=1;

# required in order to list users
foreign_require("useradmin", "user-lib.pl");


#-------------------------------------------------------------------------------------
#reads the file AppleVolumes.default and continues with it
#-------------------------------------------------------------------------------------
sub open_afile
{
	local(@rv,$line);

	#File $applevolume_default not readable
	open(FH,"<$applevolume_default") || die "$text{file} $applevolume_default $text{not_readable}";

	while(defined($line = <FH>) )
	{
		local($longName);
		#Line with continuation characters read in
		chomp $line;
		if($line =~ s/\\$//  )
		{
			$line .=<FH>;
			redo unless eof(FH);
		}
		#read lines which begins with ' ~ ' or ' / '
		if($line=~/^([$slash~]\S*)\s?("([^"]+)")?\s?(\N+)?/ )
		{
			#create new objects using volume_format and options_format
			my $options = options_format->new();
			my $volume = volume_format->new(options => $options);
			$path = $1;
			$name = $3;
			$all_options = $4;
			$volume->path($path);
			$volume->all_options($all_options);

			if($name eq "")
			{
				if($path=~/([^$slash]+)$/ )
				{
					$name = $1;
				}
				else
				{
					$name = $path;
				}
			}
			$volume->name($name);
			#options read in
			while ($all_options =~ /(\w+):([\w\d$slash\$@,.-:]+)/g)
			{
				if ("adouble" eq $1) {
					$options->adouble($2);
				}
				elsif ("volsizelimit" eq $1) {
					$options->volsizelimit($2);
				}
				elsif("allow" eq $1){
					$options->allow($2);
				}
				elsif("allowed_hosts" eq $1){
					$options->allowed_hosts($2);
				}
				elsif("deny" eq $1){
					$options->deny($2);
				}
				elsif("denied_hosts" eq $1){
					$options->denied_hosts($2);
				}
				elsif("cnidscheme" eq $1){
					$options->cnidscheme($2);
				}
				elsif("cnidserver" eq $1){
					$options->cnidserver($2);
				}
				elsif("dbpath" eq $1){
					$options->dbpath($2);
				}
				elsif("ea" eq $1){
					$options->ea($2);
				}
				elsif("maccharset" eq $1){
					$options->maccharset($2);
				}
				elsif("options" eq $1){
					$options->options($2);
				}
				elsif("password" eq $1){
					$options->password($2);
				}
				elsif("perm" eq $1){
					$options->perm($2);
				}
				elsif("fperm" eq $1){
					$options->fperm($2);
				}
				elsif("dperm" eq $1){
					$options->dperm($2);
				}
				elsif("umask" eq $1){
					$options->umask($2);
				}
				elsif("rolist" eq $1){
					$options->rolist($2);
				}
				elsif("rwlist" eq $1){
					$options->rwlist($2);
				}
				elsif("veto" eq $1){
					$options->veto($2);
				}
				elsif("volcharset" eq $1){
					$options->volcharset($2);
				}
				elsif("casefold" eq $1){
					$options->casefold($2);
				}
			}
			#write available options in $volume
			push(@rv,$name);
			$pername{$volume->name} = $volume;
		}
	}
	close(FH);
	return @rv;
}

#------------------------------------------------------------------------------
#Getter subroutines for volume_format object members
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

sub getPath
{
	my ($var1) = @_;
	$path = 0;
	if ($rp = $pername{$var1}){
		$path = $rp->path;
	}
	return $path;
}

sub getAdouble
{
  	my ($var1) = @_;
  	$adouble = "";
  	if ($rp = $pername{$var1}){
		$adouble = $rp->options->adouble;
 	}
  	return $adouble;
}

sub getVolsizelimit
{
  	my ($var1) = @_;
  	$volsizelimit = "";
  	if ($rp = $pername{$var1}){
		$volsizelimit = $rp->options->volsizelimit;
 	}
  	return $volsizelimit;
}

sub getAllow
{
  	my ($var1) = @_;
  	$Access = "";
  	if ($rp = $pername{$var1}){
		$Access = $rp->options->allow;
 	}
  	return $Access;
}

sub getDeny
{
        my ($var1) = @_;
        $Access = "";
        if ($rp = $pername{$var1}){
                $Access = $rp->options->deny;
        }
        return $Access;
}

sub getAllowedHosts
{
  	my ($var1) = @_;
  	$AllowedHosts = "";
  	if ($rp = $pername{$var1}){
		$AllowedHosts = $rp->options->allowed_hosts;
 	}
  	return $AllowedHosts;
}

sub getDeniedHosts
{
        my ($var1) = @_;
        $DeniedHosts = "";
        if ($rp = $pername{$var1}){
                $DeniedHosts = $rp->options->denied_hosts;
        }
        return $DeniedHosts;
}

sub getCnidScheme
{
        my ($var1) = @_;
        $CnidScheme = "";
        if ($rp = $pername{$var1}){
                $CnidScheme = $rp->options->cnidscheme;
        }
        return $CnidScheme;
}

sub getCnidServer
{
        my ($var1) = @_;
        $CnidServer = "";
        if ($rp = $pername{$var1}){
                $CnidServer = $rp->options->cnidserver;
        }
        return $CnidServer;
}

sub getDatabase
{
  	my ($var1) = @_;
  	$Database = "";
  	if ($rp = $pername{$var1}){
		$Database = $rp->options->dbpath;
 	}	
  	return $Database;
}

sub getEa
{
        my ($var1) = @_;
        $Ea = "";
        if ($rp = $pername{$var1}){
                $Ea = $rp->options->ea;
        }
        return $Ea;
}

sub getMacCharset
{
        my ($var1) = @_;
        $MacCharset = "";
        if ($rp = $pername{$var1}){
                $MacCharset = $rp->options->maccharset;
        }
        return $MacCharset;
}

sub getOptions
{
  	my ($var1) = @_;
  	$Options = "";
  	if ($rp = $pername{$var1}){
		$Options = $rp->options->options;
 	}
  	return $Options;
}

sub getPassword
{
  	my ($var1) = @_;
  	$Password = "";
  	if ($rp = $pername{$var1}){
		$Password = $rp->options->password;
 	}	
  	return $Password;
}

sub getPerm
{
  	my ($var1) = @_;
  	$Perm = "";
  	if ($rp = $pername{$var1}){
		$Perm = $rp->options->perm;
 	}	
  	return $Perm;
}

sub getFPerm
{
  	my ($var1) = @_;
  	$FPerm = "";
  	if ($rp = $pername{$var1}){
		$FPerm = $rp->options->fperm;
 	}	
  	return $FPerm;
}

sub getDPerm
{
  	my ($var1) = @_;
  	$DPerm = "";
  	if ($rp = $pername{$var1}){
		$DPerm = $rp->options->dperm;
 	}	
  	return $DPerm;
}

sub getUmask
{
  	my ($var1) = @_;
  	$Umask = "";
  	if ($rp = $pername{$var1}){
		$Umask = $rp->options->umask;
 	}	
  	return $Umask;
}

sub getRolist
{
        my ($var1) = @_;
        $Access = "";
        if ($rp = $pername{$var1}){
                $Access = $rp->options->rolist;
        }
        return $Access;
}

sub getRwlist
{
        my ($var1) = @_;
        $Access = "";
        if ($rp = $pername{$var1}){
                $Access = $rp->options->rwlist;
        }
        return $Access;
}

sub getVeto
{
        my ($var1) = @_;
        $Veto = "";
        if ($rp = $pername{$var1}){
                $Veto = $rp->options->veto;
        }
        return $Veto;
}

sub getVolCharset
{
        my ($var1) = @_;
        $VolCharset = "";
        if ($rp = $pername{$var1}){
                $VolCharset = $rp->options->volcharset;
        }
        return $VolCharset;
}

sub getCasefold
{
  	my ($var1) = @_;
  	$casefold = "";
  	if ($rp = $pername{$var1}){
		$casefold = $rp->options->casefold;
 	}
  	return $casefold;
}

#------------------------------------------------------------------------------
#Special getter for a string of all options, to be printed in the UI
#------------------------------------------------------------------------------
sub getAllOptions
{
  	my ($var1) = @_;
  	$AllOptions ="";
  	if ($rp = $pername{$var1}){
		$AllOptions = $rp->all_options;
 	}
  	return $AllOptions;
}

#------------------------------------------------------------------------------
#checked whether indicated path exists
#------------------------------------------------------------------------------
sub getPathOK
{
	my ($var1) = @_;
	local($rv);
	$rv = 0;
	opendir(DIR,$var1);
	# Bypass the dir exists check if the path starts at the home dir
	if(readdir(DIR) || $var1 =~ /^~/){
		$rv = "1";
	}
	closedir(DIR);
	return $rv;
}


#------------------------------------------------------------------------------
#list all users with ID >=500
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
#list all groups with ID >=100 and root gid == 0
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
#writes new file share by generating new lines
#------------------------------------------------------------------------------
sub writeNewFileShare
{
	local($line_1, $line_2);
	my ($in) = @_;
	#homes or other Path
	if($in{homes}){
		$line_1 ="~ ";
	}
	else{
		$pathli = $in{path};
		if($pathli && 1 eq getPathOK($pathli)){
			$line_1 = "$pathli ";
		}
		else{
			showMessage($text{give_correct_path});
			return 0;	
		}
		#share name is captured
		if($in{share}){
			$line_1 .= "\"$in{share}\"";
		}
		else{
			showMessage($text{indicate_sharename});
			return 0;
		}
	}

	#options read in
	$line_1 .= " volsizelimit:$in{volsizelimit}" if $in{volsizelimit};
	$line_1 .= " allowed_hosts:$in{allowed_hosts}" if $in{allowed_hosts};
	$line_1 .= " denied_hosts:$in{denied_hosts}" if $in{denied_hosts};
	$line_1 .= " cnidscheme:$in{cnidscheme}" if $in{cnidscheme};
	$line_1 .= " cnidserver:$in{cnidserver}" if $in{cnidserver};
	$line_1 .= " dbpath:$in{dbpath}" if $in{dbpath};
	$line_1 .= " maccharset:$in{maccharset}" if $in{maccharset};
	$line_1 .= " password:$in{password}" if $in{password};
	$line_1 .= " perm:$in{perm}" if $in{perm};
	$line_1 .= " fperm:$in{fperm}" if $in{fperm};
	$line_1 .= " dperm:$in{dperm}" if $in{dperm};
	$line_1 .= " umask:$in{umask}" if $in{umask};
	$line_1 .= " veto:$in{veto}" if $in{veto};
	$line_1 .= " volcharset:$in{volcharset}" if $in{volcharset};

	if($in{adouble_options} && $in{adouble_options} ne "default"){
		$line_1 .= " adouble:$in{adouble_options}";
	}
	if($in{ea_options} && $in{ea_options} ne "default"){
		$line_1 .= " ea:$in{ea_options}";
	}
	if($in{casefold_options} && $in{casefold_options} ne "default"){
		$line_1 .= " casefold:$in{casefold_options}";
	}

	if($in{allow_users} || $in{allow_groups} ){
		$line_1 .= " allow:";
		if($in{allow_users}){
		    $line_1 .= join(',', split(/\s+/, $in{allow_users}));
		}
		if($in{allow_users} && $in{allow_groups} ){
			$line_1 .= ",@";
		} elsif($in{allow_groups}) {
			$line_1 .= "@";
		}
		if($in{allow_groups}){
			$line_1 .= join(',@', split(/\s+/, $in{allow_groups}));
		}
	}
	if($in{deny_users} || $in{deny_groups} ){
		$line_1 .= " deny:";
		if($in{deny_users}){
			$line_1 .= join(',', split(/\s+/, $in{deny_users}));
		}
		if($in{deny_users} && $in{deny_groups} ){
			$line_1 .= ",@";
		} elsif($in{deny_groups}) {
			$line_1 .= "@";
		}
		if($in{deny_groups}){
			$line_1 .= join(',@', split(/\s+/, $in{deny_groups}));
		}
        }

	if($in{misc_options}){
		$line_1 .= " options:";
		foreach $name(param(misc_options)){
			@values = param(misc_options);
			$input_misc = join(',', @values);
		}
		$line_1 .= $input_misc;
	}

        if($in{rolist_users} || $in{rolist_groups} ){
                $line_1 .= " rolist:";
                if($in{rolist_users}){
                    $line_1 .= join(',', split(/\s+/, $in{rolist_users}));
                }
                if($in{rolist_users} && $in{rolist_groups} ){
                        $line_1 .= ",@";
                } elsif($in{rolist_groups}) {
                        $line_1 .= "@";
                }
                if($in{rolist_groups}){
                        $line_1 .= join(',@', split(/\s+/, $in{rolist_groups}));
                }
        }

        if($in{rwlist_users} || $in{rwlist_groups} ){
                $line_1 .= " rwlist:";
                if($in{rwlist_users}){
                    $line_1 .= join(',', split(/\s+/, $in{rwlist_users}));
                }
                if($in{rwlist_users} && $in{rwlist_groups} ){
                        $line_1 .= ",@";
                } elsif($in{rwlist_groups}) {
                        $line_1 .= "@";
                }
                if($in{rwlist_groups}){
                        $line_1 .= join(',@', split(/\s+/, $in{rwlist_groups}));
                }
        }

	writeLine($line_1, $line_2);
}

#------------------------------------------------------------------------------
#new line writes in AppleVolumes.default
#
#var1 first line to write
#var2 second line to write
#no second line, var2 = " " is to be written instead
#-----------------------------------------------------------------------------
sub writeLine()
{
	my ($var1,$var2) = @_;
	@line = getLines($applevolume_default);
	copy($applevolume_default, $temp)
	or die "$text{copy_failed}: $!";

	&lock_file("$temp");
	open(OLD, "<$applevolume_default") || die "$text{file} $applevolume_default $text{not_readable}";
	open(NEW, ">$temp") || die "$text{file} $temp $text{not_readable}";

	while(<OLD>){
  		if($. == @line[0]){
			print NEW  "$var1\n";
  		}
  		print NEW $_;
	}
	close(OLD);
	close(NEW);
	&unlock_file("$temp");

	rename($applevolume_default, "$applevolume_default.orig");
	rename($temp, $applevolume_default);
	unlink("$applevolume_default.orig") or die "$text{delete_failed}: $applevolume_default.orig\n";
}


#------------------------------------------------------------------
#deletes a certain line in file
#
#$var1 => File
#$var2 => Start of the line, which is to be found (i.e. directory) 
#------------------------------------------------------------------
sub deleteLine(){
	my ($var1, $var2) = @_;
	local($counter, $lines);
	if( ! defined $var1){
		return 0;
	}
	if( ! defined $var2){
		return 0;
	}

	@lines = getLines($applevolume_default, $var2);
	copy($applevolume_default, $temp)
	or die "$text{copy_failed}: $!";

	&lock_file("$temp");
	open(OLD,"<$applevolume_default") || die "$text{file} $applevolume_default $text{not_readable}";
	open(NEW,">$temp")  || die "$text{file} $applevolume_default $text{not_readable}";

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

	rename($applevolume_default, "$applevolume_default.orig");
	rename($temp, $applevolume_default);
	unlink("$applevolume_default.orig") or die "$text{delete_failed}: $applevolume_default.orig\n";
	return 1;
}


#------------------------------------------------------------------
#Page, which displays input error
#
#$var1 Info-Text
#------------------------------------------------------------------
sub showMessage
{
	my ($var1) = @_;
	ui_print_header(undef, Warning, "", "configs", 1);
	print "<h2>**** $var1 ****</h2>\n";
	ui_print_footer("index.cgi", $text{'index_module'});
}


#------------------------------------------------------------------
#Function reads afpd.conf and stores data for UI display in an array
#
#------------------------------------------------------------------
sub readAfpd
{
	local(
		$fileToRead,
		@afpd,
		@afpd_all,
	);
	push(@afpd_all, 1);
	$fileToRead = $config{'afpd_c'};
	open(FH, "<$fileToRead") || die "$text{file} $fileToRead $text{not_readable}";
	while(<FH>)
	{
		#Line with continuation characters read in
		if($_=~/(^[\w\d-\"].*)/ ){
			@afpd = (
				$hostname,
				"Disabled",
				"No Authentication",
				"Default",
				"Default"
			);
			
			if($_ =~ /^(\"[^\"]+\"|[^\s-]+)\s/)  {
				$1 =~ /^\"*([^\"]+)\"*/;
				@afpd[0] = $1;
			}

			if($_ =~ /-transall/ || $_ =~ /-(ddp|tcp)\s+-(ddp|tcp)/ ){
				@afpd[1] = "AppleTalk, TCP/IP"
			}
			elsif($_ =~ /-(ddp|notcp)\s+-(notcp|ddp)/ ){
				@afpd[1] = "AppleTalk"
			}
			elsif($_ =~ /-(noddp|tcp)\s+-(tcp|noddp)/ ){
				@afpd[1] = "TCP/IP"
			}

			if($_ =~ /-uamlist\s([\w\d\._,]+)\s/){
				@afpd[2] = $1;
			}
			if($_ =~ /-port\s([0-9]*)/){
				@afpd[3] = $1;
			}
			if($_ =~ /-ipaddr\s([0-9.]*)/){
				@afpd[4] = $1;
			}
			push(@afpd_all, @afpd);
		}
	}	
	close(FH);
	return @afpd_all;
}


#------------------------------------------------------------------
#Function reads afpd.conf and stores data for editing in an array
#
#------------------------------------------------------------------
sub getAllAfpd
{
	local(
		$fileToRead,
		@afpd,
		@afpd_all,
		$notcp,
		$nodpp,
		$port,
		$address,
		$loginMessage,
		$nosavepass,
		$nosetpass,
		$uamlist,
		$mimicmodel,
		$noicon
	);
	push(@afpd_all);
	$notcp="-notcp";
	$nodpp="-noddp";
	$port="-port";
	$address="-ipaddr";
	$loginMessage="-loginmesg";
	$nosavepass="-nosavepassword";
	$nosetpass="-nosetpassword";
	$uamlist="-uamlist";
	$mimicmodel="-mimicmodel";
	$noicon="-noicon";
	$fileToRead = $config{'afpd_c'};
	open(FH, "<$fileToRead") || die "$text{file} $fileToRead $text{not_readable}";
	while(<FH>)
	{
		#Line with continuation characters read in
		if($_=~/(^[\w\d-\"].*)/ ){
			@afpd = (
				$hostname,
				"-tcp",
				"-ddp",
				"-",
				"-",
				"",
				"-savepassword",
				"-setpassword",
				"-uamlist uams_dhx2.so",
				"-icon",
				""
			);
			if($_ =~ /^(\"[^\"]+\"|[^\s-]+)\s/)  {
				$1 =~ /^\"*([^\"]+)\"*/;
				@afpd[0] = $1;
			}
			if($_ =~ /$notcp/){
				@afpd[1] = $notcp;
			}   		
			if($_ =~ /$nodpp/){
				@afpd[2] = $nodpp;
			}
			if($_ =~ /$port\s([\d]+)/){
				@afpd[3] = $1;
			}
			if($_ =~ /$address\s(\d+\.\d+\.\d+\.\d+)/){
				@afpd[4] = $1;
			}
			if($_ =~ /$loginMessage\s"(.*?)"/){
				@afpd[5] = $1;
			}
			if($_ =~ /$nosavepass/){
				@afpd[6] = $nosavepass;
			}
			if($_ =~ /$nosetpass/){
				@afpd[7] = $nosetpass;
			}
			if($_ =~ /$uamlist\s([\w\d\.,]+)/){
				@afpd[8] = $1;
			}
			if($_ =~ /$noicon/){
				@afpd[9] = $noicon;
			}
			if($_ =~ /$mimicmodel\s\"*([\w\d\,]+)\"*/){
				@afpd[10] = $1;
			}
			push(@afpd_all, @afpd);
		}
	}	
	close(FH);
	return @afpd_all;
}


#------------------------------------------------------------------------------
#Function appends a new line to file
#
#$var1 Line is added
#$var2 File to which the line should be appended
#------------------------------------------------------------------------------
sub addLineToFile()
{
	my ($var1, $var2) = @_;
	local($temporary, $lin);
    	$lin = getLinesSpezFile($var1);
 	$temporary = "$var1.temp";

	copy($var1, $temporary) or die "$text{copy_failed}: $!";

	lock_file("$temporary");
	open(OLD, "<$var1") || die "$text{file} $var1 $text{not_readable}";
	open(NEW, ">$temporary") || die "$text{file} $temporary $text{not_readable}";

	while(<OLD>){
		print NEW $_;
  		if($. == $lin){
  			print NEW  "$var2\n";
  		}
	}
	close(OLD);
	close(NEW);
	unlock_file("$temporary");
	rename($var1, "$var1.orig");
	rename($temporary, $var1);
	unlink("$var1.orig") or die "$text{delete_failed}: $var1.orig\n";
}

#------------------------------------------------------------------
#gives the number of lines, of the specified file or to a certain line
#
#$var1 File that needs to be opened
#$var2 Line, from which the line number is to ne determined
#------------------------------------------------------------------
sub getLines(){
	my ($var1, $var2, $var3) = @_;
	local($counter, $output,@rv);
	$counter = 0;
	$output = 1;
	#Tests whether the variable has been passed
	if( ! defined $var1){
		return 0;
	}
	#Tests the second
	elsif( ! defined $var2){
		open(FH, "<$var1") || die return 0;
		while(defined($line = <FH>) ){
			if($line =~ /^[$slash~]+/ ){
				push(@rv, $output);
			}
			$output++;
		}
	}
	else{
		open(FH, "<$var1") || die return 0;
		while(defined($line = <FH>) )
		{
			if($line =~ /^[$slash~]+/ ){
				if($line =~ /([A-Za-z$slash=~,-_\\]+)/){
					if($1 =~ /$var2/){
						$output = $counter;
						push(@rv, $output);
						$output++;
						if($line =~ /[\\]/){
							push(@rv, $output);
						}
						else{
							push(@rv, -1);
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
#deletes a certain line in a file
#$var1 =>File
#$var2 =>Start of the line, which is to be found (e.g. directory)
#------------------------------------------------------------------
sub deleteSpezLine(){
	my ($var1, $var2) = @_;
	local($temporary);
	if( ! defined $var1){
		return 0;
	}
	if( ! defined $var2){
		return 0;
	}
	$line = getSpezLine($var1, $var2);
	$temporary = "$var1.temp";
 	copy($var1, $temp)
		or die "$text{copy_failed}: $!";

	lock_file("$temporary");
	open(OLD, "<$var1") || die "$text{file} $applevolume_default $text{not_readable}";
	open(NEW, ">$temporary") || die "$text{file} $temp $text{not_readable}";
	while(<OLD>){
		if($. != $line ){
			print NEW $_;
		}
	}
	close(OLD);
	close(NEW);
	unlock_file("$temporary");
	rename($var1, "$var1.orig");
	rename($temporary, $var1);
	unlink("$var1.orig") or die "$text{delete_failed}: $var1.orig\n";
	return 1;
	
}

sub getSpezLine
{
	my ($var1, $var2) = @_;
	local($counter, $outputli, $escaped_name);
	$counter = 0;
	# Escape special chars such as the dollar sign
	$escaped_name = quotemeta($var2);
	open(OLD, "<$var1") || die "$text{file} $applevolume_default $text{not_readable}";
	while(<OLD>){
		$counter++;
		# Server names may or may not be quoted
 		if($_ =~ /^\"?$escaped_name/ ){
 			$outputli = $counter;
  		}
	}
	close(OLD);
	return $outputli;
}


#-------------------------------------------------------------------------------
#Function determines number of lines of a file
#
#$var1 is the file
#-------------------------------------------------------------------------------
sub getLinesSpezFile() {
	my ($var1) = @_;
	local($counting);
	$counting = 0;
	#Test whether the variable has been passed
	open(FileHandle, "<$var1") || die return 0;
	while(<FileHandle>){
		$counting++;
	}
	close(FileHandle);
	return $counting;
}

sub version() {
	my $version = `$config{'afpd_d'} -v 0>&1`;
	$version =~ m/(afpd \S+) /;

	return $1;
}
