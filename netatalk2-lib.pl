#!/usr/bin/perl
# Common functions for manipulating the netatalk config files

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
#    Copyright (C) 2000 by Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Copyright (C) 2023-24 Daniel Markstedt <daniel@mindani.net>
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

do '../web-lib.pl';
BEGIN { push(@INC, ".."); };
use WebminCore;
use File::Copy;
use CGI qw/:standard/;
init_config();

$applevolume_default = $config{'applevolumedefault_c'};

$pername = ();

#struct volume_format administers all information of a " line "
use Class::Struct;
	struct  volume_format => {
		path=>'$',
		name=>'$',
		all_options=>'$',
		options=>'options_format',
	};

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
	open(FH,"<$applevolume_default") || die "$applevolume_default $text{not_readable}";

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
		if($line=~/^([\/~:]\S*)\s?("([^"]+)")?\s?(\N+)?/ )
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
				if($path=~/([^\/]+)$/ )
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
			while ($all_options =~ /(\w+):([\w\d\/\$@,\.\-:]+)/g)
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
sub createNewFileShare
{
	local $new_line;
	my ($in) = @_;
	local @volumes = open_afile();
	foreach $v (@volumes) {
		if (($in{path} eq getPath($v)) || ($in{homes} && (getPath($v) =~ "^~"))) {
			showMessage(&text(error_dup_path, getPath($v)));
			exit;
		}
		if ($in{share} eq getShareName($v)) {
			showMessage(&text(error_dup_name, getShareName($v)));
			exit;
		}
	}

	#homes or other Path
	if($in{homes}){
		$new_line = "~ ";
	}
	elsif($in{default_options}){
		$new_line = ":DEFAULT: ";
	}
	else{
		$pathli = $in{path};
		if($pathli){
			$new_line = "$pathli ";
		}
		else{
			showMessage($text{give_correct_path});
			return 0;
		}
	}

	#share name is captured
	if($in{share}){
		$new_line .= "\"$in{share}\"";
	}
	elsif (!$in{default_options}){
		showMessage($text{indicate_sharename});
		return 0;
	}

	#options read in
	$new_line .= " volsizelimit:$in{volsizelimit}" if $in{volsizelimit};
	$new_line .= " allowed_hosts:$in{allowed_hosts}" if $in{allowed_hosts};
	$new_line .= " denied_hosts:$in{denied_hosts}" if $in{denied_hosts};
	$new_line .= " cnidscheme:$in{cnidscheme}" if $in{cnidscheme};
	$new_line .= " cnidserver:$in{cnidserver}" if $in{cnidserver};
	$new_line .= " dbpath:$in{dbpath}" if $in{dbpath};
	$new_line .= " maccharset:$in{maccharset}" if $in{maccharset};
	$new_line .= " password:$in{password}" if $in{password};
	$new_line .= " perm:$in{perm}" if $in{perm};
	$new_line .= " fperm:$in{fperm}" if $in{fperm};
	$new_line .= " dperm:$in{dperm}" if $in{dperm};
	$new_line .= " umask:$in{umask}" if $in{umask};
	$new_line .= " veto:$in{veto}" if $in{veto};
	$new_line .= " volcharset:$in{volcharset}" if $in{volcharset};

	if($in{adouble_options} && $in{adouble_options} ne "default"){
		$new_line .= " adouble:$in{adouble_options}";
	}
	if($in{ea_options} && $in{ea_options} ne "default"){
		$new_line .= " ea:$in{ea_options}";
	}
	if($in{casefold_options} && $in{casefold_options} ne "default"){
		$new_line .= " casefold:$in{casefold_options}";
	}

	if($in{allow_users} || $in{allow_groups} ){
		$new_line .= " allow:";
		if($in{allow_users}){
		    $new_line .= join(',', split(/\s+/, $in{allow_users}));
		}
		if($in{allow_users} && $in{allow_groups} ){
			$new_line .= ",@";
		} elsif($in{allow_groups}) {
			$new_line .= "@";
		}
		if($in{allow_groups}){
			$new_line .= join(',@', split(/\s+/, $in{allow_groups}));
		}
	}
	if($in{deny_users} || $in{deny_groups} ){
		$new_line .= " deny:";
		if($in{deny_users}){
			$new_line .= join(',', split(/\s+/, $in{deny_users}));
		}
		if($in{deny_users} && $in{deny_groups} ){
			$new_line .= ",@";
		} elsif($in{deny_groups}) {
			$new_line .= "@";
		}
		if($in{deny_groups}){
			$new_line .= join(',@', split(/\s+/, $in{deny_groups}));
		}
        }

	if($in{misc_options}){
		$new_line .= " options:";
		foreach $name(param(misc_options)){
			@values = param(misc_options);
			$input_misc = join(',', @values);
		}
		$new_line .= $input_misc;
	}

        if($in{rolist_users} || $in{rolist_groups} ){
                $new_line .= " rolist:";
                if($in{rolist_users}){
                    $new_line .= join(',', split(/\s+/, $in{rolist_users}));
                }
                if($in{rolist_users} && $in{rolist_groups} ){
                        $new_line .= ",@";
                } elsif($in{rolist_groups}) {
                        $new_line .= "@";
                }
                if($in{rolist_groups}){
                        $new_line .= join(',@', split(/\s+/, $in{rolist_groups}));
                }
        }

        if($in{rwlist_users} || $in{rwlist_groups} ){
                $new_line .= " rwlist:";
                if($in{rwlist_users}){
                    $new_line .= join(',', split(/\s+/, $in{rwlist_users}));
                }
                if($in{rwlist_users} && $in{rwlist_groups} ){
                        $new_line .= ",@";
                } elsif($in{rwlist_groups}) {
                        $new_line .= "@";
                }
                if($in{rwlist_groups}){
                        $new_line .= join(',@', split(/\s+/, $in{rwlist_groups}));
                }
        }

        return $new_line;
}


#-----------------------------------------------------------------------------
# Function creates new line with entry for servers
# in afpd.conf
#-----------------------------------------------------------------------------
sub createNewServerLine(){
	local $illegalChars = ":@\$\"<>\/";
	local $newString;
	my ($in) = @_;
	local @servers = getAllAfpd();
	foreach my $s (@servers) {
		if ($in{servername} eq $s->{servername}) {
			showMessage(&text(error_dup_name, $s->{servername}));
			exit;
		}
	}

	unless($in{servername}){
		$newString = "- ";
	}
	else{
		if($in{servername} =~ /[$illegalChars]/){
			showMessage("$text{error_illegal_char} $illegalChars");
			return 0;
		}
		$newString = "\"$in{servername}\" ";
	}
	if( $in{transport_tcp} && $in{transport_ddp} ){
		$newString .= "-transall ";
	}
	elsif( $in{transport_tcp} ){
		$newString .= "-noddp -tcp ";
	}
	elsif( $in{transport_ddp} ){
		$newString .= "-ddp -notcp ";
	}
	else{
		$newString .= "-notransall ";
	}
	if($in{port}){
		$newString .= "-port $in{port} ";
	}
	if($in{address}){
		$newString .= "-ipaddr $in{address} ";
	}
	if($in{savepassword} eq 'yes'){
		$newString .= "-savepassword ";
	}
	elsif($in{savepassword} eq 'no'){
		$newString .= "-nosavepassword ";
	}
	if($in{setpassword} eq 'yes'){
		$newString .= "-setpassword ";
	}
	elsif($in{setpassword} eq 'no'){
		$newString .= "-nosetpassword ";
	}
	if($in{loginmesg}){
		$newString .= "-loginmesg \"$in{loginmesg}\" ";
	}
	if($in{uams}){
		$in{uams} =~ s/\x00/\,/g;
		$newString .= "-uamlist $in{uams} ";
	}
	if($in{icon} eq 'yes'){
		$newString .= "-icon ";
	}
	elsif($in{icon} eq 'no'){
		$newString .= "-noicon ";
	}
	if($in{mimicmodel}){
		$newString .= "-mimicmodel \"$in{mimicmodel}\" ";
	}
	if($in{setuplog}){
		$newString .= "-setuplog \"$in{setuplog}\" ";
	}
	if($in{maccodepage}){
		$newString .= "-maccodepage $in{maccodepage} ";
	}
	if($in{unixcodepage}){
		$newString .= "-unixcodepage $in{unixcodepage} ";
	}
	if($in{defaultvol}){
		$newString .= "-defaultvol $in{defaultvol} ";
	}
	if($in{systemvol}){
		$newString .= "-systemvol $in{systemvol} ";
	}
	if($in{uservol} eq 'yes'){
		$newString .= "-uservol ";
	}
	elsif($in{uservol} eq 'no'){
		$newString .= "-nouservol ";
	}
	if($in{uservolfirst} eq 'yes'){
		$newString .= "-uservolfirst ";
	}
	elsif($in{uservolfirst} eq 'no'){
		$newString .= "-nouservolfirst ";
	}
	if($in{uampath}){
		$newString .= "-uampath $in{uampath} ";
	}
	if($in{k5keytab}){
		$newString .= "-k5keytab $in{k5keytab} ";
	}
	if($in{k5service}){
		$newString .= "-k5service $in{k5service} ";
	}
	if($in{k5realm}){
		$newString .= "-k5realm $in{k5realm} ";
	}
	if($in{ntdomain}){
		$newString .= "-ntdomain $in{ntdomain} ";
	}
	if($in{ntseparator}){
		$newString .= "-ntseparator $in{ntseparator} ";
	}
	if($in{adminauthuser}){
		$newString .= "-adminauthuser $in{adminauthuser} ";
	}
	if($in{passwdfile}){
		$newString .= "-passwdfile $in{passwdfile} ";
	}
	if($in{advertise_ssh}){
		$newString .= "-advertise_ssh ";
	}
	if($in{proxy}){
		$newString .= "-proxy ";
	}
	if($in{nozeroconf}){
		$newString .= "-nozeroconf ";
	}
	if($in{slp}){
		$newString .= "-slp ";
	}
	if($in{ddpaddr}){
		$newString .= "-ddpaddr $in{ddpaddr} ";
	}
	if($in{fqdn}){
		$newString .= "-fqdn $in{fqdn} ";
	}
	if($in{hostname}){
		$newString .= "-hostname $in{hostname} ";
	}
	if($in{server_quantum}){
		$newString .= "-server_quantum $in{server_quantum} ";
	}
	if($in{dsireadbuf}){
		$newString .= "-dsireadbuf $in{dsireadbuf} ";
	}
	if($in{tcprcvbuf}){
		$newString .= "-tcprcvbuf $in{tcprcvbuf} ";
	}
	if($in{tcpsndbuf}){
		$newString .= "-tcpsndbuf $in{tcpsndbuf} ";
	}

	return $newString;
}


#------------------------------------------------------------------
#Function reads afpd.conf and stores data for UI display in an array
#------------------------------------------------------------------
sub readAfpd
{
	local	@afpd_all;
	local $fileToRead = $config{'afpd_c'};
	open(FH, "<$fileToRead") || die "$fileToRead $text{not_readable}";
	while(<FH>)
	{
		#Line with continuation characters read in
		if($_=~/(^[\w\d-\"].*)/ ){
			local %afpd = (
				servername => &get_system_hostname(),
				transport => $text{'create_server_disabled'},
				uams => $text{'create_server_no_auth'},
				port => $text{'create_server_default'},
				address => $text{'create_server_default'}
			);

			if($_ =~ /^(\"[^\"]+\"|[^\s-]+)\s/)  {
				$1 =~ /^\"*([^\"]+)\"*/;
				$afpd{servername} = $1;
			}

			if($_ =~ /-transall/ || $_ =~ /-(ddp|tcp)\s+-(ddp|tcp)/ ){
				$afpd{transport} = "AppleTalk, TCP/IP";
			}
			elsif($_ =~ /-(ddp|notcp)\s+-(notcp|ddp)/ ){
				$afpd{transport} = "AppleTalk";
			}
			elsif($_ =~ /-(noddp|tcp)\s+-(tcp|noddp)/ ){
				$afpd{transport} = "TCP/IP";
			}
			elsif($_ =~ /-notransall/ || $_ =~ /-(noddp|notcp)\s+-(noddp|notcp)/ ){
				$afpd{transport} = "$text{'create_server_disabled'}";
			}

			if($_ =~ /-uamlist\s([\w\d\._,]+)\s/){
				$afpd{uams} = $1;
			}
			if($_ =~ /-port\s([0-9]*)/){
				$afpd{port} = $1;
			}
			if($_ =~ /-ipaddr\s([0-9.]*)/){
				$afpd{address} = $1;
			}
			push @afpd_all, \%afpd;
		}
	}
	close(FH);
	return @afpd_all;
}


#------------------------------------------------------------------
#Function reads afpd.conf and stores data for editing in an array
#------------------------------------------------------------------
sub getAllAfpd
{
	local @afpd_all;
	local $fileToRead = $config{'afpd_c'};

	open(FH, "<$fileToRead") || die "$fileToRead $text{not_readable}";
	while(<FH>)
	{
		local %afpd;
		#Line with continuation characters read in
		if($_=~/(^[\w\d-\"].*)/ ){
			if($_ =~ /^(\"[^\"]+\"|[^\s-]+)\s/) {
				$1 =~ /^\"*([^\"]+)\"*/;
				$afpd{servername} = $1;
			}
			if($_ =~ /-transall/) {
				$afpd{transport} = "-transall";
			} elsif($_ =~ /-notransall/) {
				$afpd{transport} = "-notransall";
			} else {
				if($_ =~ /-tcp/) {
					$afpd{transport} = "-tcp";
				} elsif($_ =~ /-notcp/) {
					$afpd{transport} = "-notcp";
				}
				if($_ =~ /-ddp/) {
					$afpd{transport} .= " -ddp";
				} elsif($_ =~ /-noddp/) {
					$afpd{transport} .= " -noddp";
				}
			}
			if($_ =~ /-port\s([\d]+)/) {
				$afpd{port} = $1;
			}
			if($_ =~ /-ipaddr\s(\d+\.\d+\.\d+\.\d+)/) {
				$afpd{ipaddr} = $1;
			}
			if($_ =~ /-loginmesg\s"(.*?)"/) {
				$afpd{loginmesg} = $1;
			}
			if($_ =~ /-savepassword/) {
				$afpd{savepassword} = "yes";
			} elsif($_ =~ /-nosavepassword/) {
				$afpd{savepassword} = "no";
			}
			if($_ =~ /-setpassword/) {
				$afpd{setpassword} = "yes";
			} elsif($_ =~ /-nosetpassword/) {
				$afpd{setpassword} = "no";
			}
			if($_ =~ /-uamlist\s([\w\d\.,]+)/) {
				$afpd{uamlist} = $1;
			}
			if($_ =~ /-icon/) {
				$afpd{icon} = "yes";
			} elsif($_ =~ /-noicon/) {
				$afpd{icon} = "no";
			}
			if($_ =~ /-mimicmodel\s\"*([\w\d\,]+)\"*/) {
				$afpd{mimicmodel} = $1;
			}
			if($_ =~ /-setuplog\s\"(.+)\"/) {
				$afpd{setuplog} = $1;
			}
			if($_ =~ /-maccodepage\s([\w_]+)/) {
				$afpd{maccodepage} = $1;
			}
			if($_ =~ /-unixcodepage\s([^\s]+)/) {
				$afpd{unixcodepage} = $1;
			}
			if($_ =~ /-defaultvol\s(\/[^\s]*)/) {
				$afpd{defaultvol} = $1;
			}
			if($_ =~ /-systemvol\s(\/[^\s]*)/) {
				$afpd{systemvol} = $1;
			}
			if($_ =~ /-uservol/) {
				$afpd{uservol} = "yes";
			} elsif($_ =~ /-nouservol/) {
				$afpd{uservol} = "no";
			}
			if($_ =~ /-uservolfirst/) {
				$afpd{uservolfirst} = "yes";
			} elsif($_ =~ /-uservolfirst/) {
				$afpd{uservolfirst} = "no";
			}
			if($_ =~ /-uampath\s(\/[^\s]*)/) {
				$afpd{uampath} = $1;
			}
			if($_ =~ /-k5keytab\s(\/[^\s]*)/) {
				$afpd{k5keytab} = $1;
			}
			if($_ =~ /-k5service\s([^\s]+)/) {
				$afpd{k5service} = $1;
			}
			if($_ =~ /-k5realm\s([^\s]+)/) {
				$afpd{k5realm} = $1;
			}
			if($_ =~ /-ntdomain\s([^\s]+)/) {
				$afpd{ntdomain} = $1;
			}
			if($_ =~ /-ntseparator\s([^\s]+)/) {
				$afpd{ntseparator} = $1;
			}
			if($_ =~ /-adminauthuser\s([^\s]+)/) {
				$afpd{adminauthuser} = $1;
			}
			if($_ =~ /-passwdfile\s(\/[^\s]*)/) {
				$afpd{passwdfile} = $1;
			}
			if($_ =~ /-advertise_ssh/) {
				$afpd{advertise_ssh} = 1;
			}
			if($_ =~ /-proxy/) {
				$afpd{proxy} = 1;
			}
			if($_ =~ /-nozeroconf/) {
				$afpd{nozeroconf} = 1;
			}
			if($_ =~ /-slp/) {
				$afpd{slp} = 1;
			}
			if($_ =~ /-ddpaddr\s([^\s]+)/) {
				$afpd{ddpaddr} = $1;
			}
			if($_ =~ /-fqdn\s([^\s]+)/) {
				$afpd{fqdn} = $1;
			}
			if($_ =~ /-hostname\s([^\s]+)/) {
				$afpd{hostname} = $1;
			}
			if($_ =~ /-server_quantum\s([^\s]+)/) {
				$afpd{server_quantum} = $1;
			}
			if($_ =~ /-dsireadbuf\s([^\s]+)/) {
				$afpd{dsireadbuf} = $1;
			}
			if($_ =~ /-tcprcvbuf\s([^\s]+)/) {
				$afpd{tcprcvbuf} = $1;
			}
			if($_ =~ /-tcpsndbuf\s([^\s]+)/) {
				$afpd{tcpsndbuf} = $1;
			}
			push @afpd_all, \%afpd;
		}
	}
	close(FH);
	return @afpd_all;
}


#------------------------------------------------------------------------------
#Function appends a new line to file
#
#$var1 File to which the line should be appended
#$var2 String to be appended
#$var3 Line number to append string to
#$var4 Total number of lines in file
#------------------------------------------------------------------------------
sub addLineToFile()
{
	my ($var1, $var2, $var3, $var4) = @_;
	local($temporary, $lin);
 	$temporary = "$var1.temp";

	copy($var1, $temporary) or die "$text{copy_failed}: $!";

	lock_file("$temporary");
	open(OLD, "<$var1") || die "$var1 $text{not_readable}";
	open(NEW, ">$temporary") || die "$temporary $text{not_readable}";

	if($var4 < 2) {
		print NEW "$var2\n";
	}
	else {
		while(my $line = <OLD>) {
			if($var3 eq 1 && $. eq 1) {
				print NEW "$var2\n";
			}
			print NEW $line;
			if($. eq ($var3 - 1)){
				print NEW "$var2\n";
			}
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
#deletes a certain line in a file
#$var1 =>File
#$var2 =>Line number to delete
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
	$temporary = "$var1.temp";
 	copy($var1, $temporary)
		or die "$text{copy_failed}: $!";

	lock_file("$temporary");
	open(OLD, "<$var1") || die "$var1 $text{not_readable}";
	open(NEW, ">$temporary") || die "$temporary $text{not_readable}";
	while(<OLD>){
		if($. != $var2){
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

#-------------------------------------------------------------------------------
#Returns the the line number where a specific string was found
#
#$var1 is the file
#$var2 is the line to match
#-------------------------------------------------------------------------------
sub getSpezLine
{
	my ($var1, $var2) = @_;
	local $counter = 0;
	local $outputli = 0;
	# Escape special chars such as the dollar sign
	local $escaped_name = quotemeta($var2);
	open(OLD, "<$var1") || die "$var1 $text{not_readable}";
	while(<OLD>){
		$counter++;
		# Server names may or may not be quoted
 		if($_ =~ /^\"?$escaped_name/ ){
 			$outputli = $counter;
 			last
		}
	}
	close(OLD);
	return $outputli;
}


#-------------------------------------------------------------------------------
#Returns the number of lines of a file
#
#$var1 is the file
#-------------------------------------------------------------------------------
sub getLinesSpezFile() {
	my ($var1) = @_;
	local($counting);
	$counting = 1;
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
