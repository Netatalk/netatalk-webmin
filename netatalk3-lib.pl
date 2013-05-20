#!/usr/bin/perl
#
# Netatalk Webmin Module
# Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list
# of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOTOC LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

BEGIN { push(@INC, ".."); };
use WebminCore;
&init_config();

our %netatalkParameterDefaults = (
	'save password'			=> 'yes',
	'set password'			=> 'no',
	'mac charset'			=> 'MAC_ROMAN',
	'unix charset'			=> 'UTF8',
	'vol charset'			=> "=> 'unix charset'",
	'afp port'				=> '548',
	'disconnect time'		=> '24',
	'dsireadbuf'			=> '12',
	'ea'					=> 'auto',
	'uam list'				=> 'uams_dhx.so uams_dhx2.so',
	'uam path'				=> '/usr/local/lib/netatalk',
	'passwd file'			=> '/etc/afppasswd',
	'advertise ssh'			=> 'no',
	'afp listen'			=> "system's first IP address",
	'afp port'				=> '548',
	'cnid listen'			=> 'localhost:4700',
	'max connections'		=> '200',
	'server quantum'		=> '1048576',
	'sleep time'			=> '10',
	'appledouble'			=> 'ea',
	'acls'					=> 'yes',
	'cnid dev'				=> 'yes',
	'convert appledouble'	=> 'yes',
	'follow symlinks'		=> 'no',
	'invisible dots'		=> 'no',
	'network ids'			=> 'no',
	'preexec close'			=> 'no',
	'read only'				=> 'no',
	'root preexec close'	=> 'no',
	'search db'				=> 'no',
	'stat vol'				=> 'yes',
	'time machine'			=> 'no',
	'unix priv'				=> 'yes',
	'vol dbpath'			=> '/var/netatalk/CNID/',
	'log level'				=> 'default:note',
);

sub write_afpconf {
	file_rotate($config{'afp_conf'});
	
	local (*NEW);
	
    open(NEW,">", "$config{'afp_conf'}.tmp") or die "$config{'afp_conf'}.tmp $!";
    print NEW $_[0];
	close(NEW);
	
	rename($config{'afp_conf'}, "$config{'afp_conf'}.orig") or die "rename failed: $config{'afp_conf'} -> $config{'afp_conf'}.orig $!\n";
	rename("$config{'afp_conf'}.tmp", $config{'afp_conf'}) or die "rename failed: $config{'afp_conf'}.tmp -> $config{'afp_conf'}\n";
	unlink("$config{'afp_conf'}.orig") or die "$text{delete_failed}: $config{'afp_conf'}.orig\n";
}

sub read_afpconf {
	die &text('afpconf_filedoesntexist', $config{'afp_conf'})."\n" unless(-e $config{'afp_conf'});

	local ($/, *FILE);
	open(FILE, "<", $config{'afp_conf'}) or die &text('afpconf_err_file', $config{'afp_conf'}, $!)."\n";
	my $afpconftxt = <FILE>;
	close(FILE);

	return parse_afpconf($afpconftxt);
}

sub parse_afpconf {
	my $afpconftxt = shift;

	my ($linesep) = ($afpconftxt =~ /(\x0d\x0a|\x0a|\x0d)/);
	die "$text{'afpconf_unexpectedeof'}\n" unless($linesep);
	
	my @afpconflines = split(/\x0d\x0a|\x0a|\x0d/, $afpconftxt, -1);
	
	my @sectionsByIndex = ();
	my %sections = ();
	my $section;
	my $i = 0;
	my $sectionIndex = 0;
	while($i <= $#afpconflines) {
		my $j = $i;
		my $line = $afpconflines[$i++];
		while($line =~ /^[^#;]*\\$/) {				# no line continuation after comments
			die "$text{'afpconf_unexpectedeof'}\n" if($i > $#afpconflines);
			$line = substr($line, 0, -1) . $afpconflines[$i++];
		}

		if($line =~ /^\s*\[/) {
			# section name
			if($line =~ /^\s*\[([^#\]]+)\]\s*$/) {	# section name must not contain ']' or '#'
				$section = {
					firstline => $j,
					linecountOfSectionHeader => $i - $j,
					linecount => $i - $j,
					name => $1,
					parameters => {},
					'index' => $sectionIndex++
				};
				if($sections{$$section{name}}) {
					die &text('afpconf_err_duplicatesection', $$section{name}, $j + 1)."\n";
				} else {
					$sections{$$section{name}} = $section;
					push @sectionsByIndex, $section;
				}
			} else {
				die &text('afpconf_syntax_err_sectionheader', $line, $j + 1)."\n";
			}
		} else {
			$$section{linecount} = $i - $$section{firstline} if($section);

			next if($line =~ /^\s*(#|;|$)/);			# skip empty or comment lines
		
			die &text('afpconf_err_no_section', $line, $j + 1)."\n" unless($section);
				
			# key = value
			if($line =~ /^(\s*(.*?)\s*=\s*)(.*?)\s*(?:#|;|$)/) {
				my ($keyAsInFile, $key, $value) = ($1, $2, $3);
				if($$section{parameters}{$key}) {
					die &text('afpconf_err_duplicatekey', $key, $$section{name}, $j + 1)."\n";
				} else {
					$$section{parameters}{$key} = {
						firstline => $j,
						linecount => $i - $j,
						keyAsInFile => $keyAsInFile,
						value => $value
					};
				}
			} else {
				die &text('afpconf_syntax_err', $line, $j + 1)."\n";
			}	
		}
	}
	
	my @volumes = ();
	my @volumepresets = ();
	for my $sectionName (keys(%sections)) {
		# accumulate volumes und volumepresets in separate arrays
		if($sectionName ne 'Homes' && $sectionName ne 'Global') {
			if(exists ${$sections{$sectionName}}{parameters}{'path'}) {
				push @volumes, $sections{$sectionName};
			} else {
				push @volumepresets, $sections{$sectionName};
			}
		}
		
		# accumulate list of names of sections using a volume preset
		if($sectionName ne 'Homes' && ${$sections{$sectionName}}{parameters}{'vol preset'}) {
			my $sectionNameOfVolumePreset = ${$sections{$sectionName}}{parameters}{'vol preset'}{value};
			if(exists $sections{$sectionNameOfVolumePreset}) {
				push @{${$sections{$sectionNameOfVolumePreset}}{presetUsedBySectionNames}}, $sectionName;
			}
		}
	}
	
	return {
		volumeSections => \@volumes,
		volumePresetSections => \@volumepresets,
		sectionsByName => \%sections,
		sectionsByIndex => \@sectionsByIndex,
		lines => \@afpconflines,
		linesep => $linesep,
	}	
}

sub trim {
	return undef unless(defined $_[0]);
	$_[0] =~ /^\s*(.*?)\s*$/;
	
	return $1;
}

sub get_parameter_of_section {
	my $afpconfRef = shift;
	my $sectionRef = shift;
	my $name = shift;
	my $inRef = shift;
	
	my $value = (defined $sectionRef && defined $$sectionRef{parameters}{$name}) ? $$sectionRef{parameters}{$name}{value} : '';
	if($inRef && exists $$inRef{"reload"}) {
		$value = defined $$inRef{"p_$name"} ? $$inRef{"p_$name"} : ''; 
	}
		
	my $default = defined $netatalkParameterDefaults{$name} ? $netatalkParameterDefaults{$name} : '';
	my $defaultSource = defined $netatalkParameterDefaults{$name} ? 'netatalk default' : '';
	
	# if $sectionRef is a volume or user homes, the default may be overridden:
	# by the 'vol preset' defined in this section
	# and if this isn't defined
	# by a 'vol preset' defined by the global section
	if($$sectionRef{name} !~ /Global/) {
		my @searchList = ();
		
		if($inRef && exists $$inRef{"reload"}) {
			# if p_vol preset exists in $inRef this is a reload of a form
			if($$inRef{"p_vol preset"}) {
				push @searchList, $$inRef{"p_vol preset"}, '-> '.$$inRef{"p_vol preset"};
			}
		} else {
			if($$sectionRef{parameters}{'path'} && $$sectionRef{parameters}{'vol preset'} && $$sectionRef{parameters}{'vol preset'}{value}) {
				# volume preset referenced by volume
				my $volumePresetName = $$sectionRef{parameters}{'vol preset'}{value};
				push @searchList, $volumePresetName, '-> '.$volumePresetName;
			}
		}
		
		# if a vol preset has been found, don't use the one in Global section, as they aren't cascading
		unless(@searchList) {
			if(exists $$afpconfRef{sectionsByName}{'Global'}{parameters}{'vol preset'} && $$afpconfRef{sectionsByName}{'Global'}{parameters}{'vol preset'}{value}) {
				# volume preset referenced by Global section
				my $volumePresetName = $$afpconfRef{sectionsByName}{'Global'}{parameters}{'vol preset'}{value};
				push @searchList, $volumePresetName, '-> Global -> '.$volumePresetName;
			}
		}
		# Global section is used as a volume preset (for values that might be defined in all sections)		
		push @searchList, 'Global', '-> Global';
		
		# now use list to find a definition
		while(@searchList) {
			my $sectionName = shift @searchList;
			my $source = shift @searchList;
			if(exists $$afpconfRef{sectionsByName}{$sectionName}{parameters}{$name} && $$afpconfRef{sectionsByName}{$sectionName}{parameters}{$name}{value}) {
				$default = $$afpconfRef{sectionsByName}{$sectionName}{parameters}{$name}{value};
				$defaultSource = $source;
				last;
			}
		}
	}
	
	return ($value, $default, $defaultSource);
}

# modify_afpconf_ref_and_write
# 
# Parameters:
# - a reference to an afpconf structure as constructed by parse_afpconf
# - a reference to a hash with the web parameters
#   - index
#   - name
#   - p_...
# 
# Checks the parameters for consistency, modifies the structure and
# writes out the afp.conf file, if modifications actually took place.
#
sub modify_afpconf_ref_and_write {
	my $afpconfRef = shift;
	my $paramRef = shift;
	
	# list of array refs of the form [firstline, linecount, value] or [firstline, linecount]
	# if value is not given, the lines will be removed
	# if linecount is 0, then value will be inserted before firstline
	my @modlist = ();	
	
	my $index = trim($$paramRef{'index'});
	my $name = trim($$paramRef{'name'});
	
	die "Volume/Volume preset name must not be empty.\n" unless($name);
	
	my $parametersOfSectionRef = {};
	my $insertWhere = scalar(@{$$afpconfRef{lines}});			# default to appending at end
	my @insertedLines = ();
	
	if($index =~ /\d+/) {
		# the index is numerical - we're about to MODIFY a section
		my $sectionToModifyRef;
		if($sectionToModifyRef = ${$$afpconfRef{sectionsByIndex}}[$index]) {
			my $existingName = $$sectionToModifyRef{name};
			if($existingName ne $name) {
				# rename section
				die "Volume/Volume preset name already used.\n" if($$afpconfRef{sectionsByName}{$name});
				push @modlist, [$$sectionToModifyRef{firstline}, $$sectionToModifyRef{linecountOfSectionHeader}, "[$name]"];
			}
			$parametersOfSectionRef = $$sectionToModifyRef{parameters};
		} else {
			die "Section doesn't exist.\n";
		}
		
		# insert new parameters directly after the section header
		$insertWhere = $$sectionToModifyRef{firstline} + $$sectionToModifyRef{linecountOfSectionHeader};
	} else {
		# the index is something else, therefore ignored: we're about to ADD a section
		die "Volume/Volume preset name already used.\n" if($$afpconfRef{sectionsByName}{$name});
		
		# insert section header line
		push @insertedLines, "[$name]";
	}
	
	# now work through the parameters in the parameters
	for my $key (keys(%$paramRef)) {
		if($key =~ /^p_(.*)/) {
			my $param_name = $1;
			my $value = trim($$paramRef{$key});
			if($$parametersOfSectionRef{$param_name}) {
				# replace or delete parameter
				if($value) {
					push @modlist, [$$parametersOfSectionRef{$param_name}{firstline}, $$parametersOfSectionRef{$param_name}{linecount}, $$parametersOfSectionRef{$param_name}{keyAsInFile}.$value];
				} else {
					push @modlist, [$$parametersOfSectionRef{$param_name}{firstline}, $$parametersOfSectionRef{$param_name}{linecount}];
				}
			} else {
				# insert parameter
				if($value) {
					push @insertedLines, "$param_name = $value";
				}
			}
		}
	}
	
	# append eventual inserted lines to @modlist
	if(@insertedLines) {
		push @modlist, [$insertWhere, 0, join($$afpconfRef{linesep}, @insertedLines)];
	}
	
	# and simply return if nothing needs to be changed
	return unless(@modlist);
	
	# now process @modlist
	for my $modActionRef (sort { $$b[0] <=> $$a[0] } @modlist) {
		my ($first, $len, @replacement) = @$modActionRef;
		splice(@{$$afpconfRef{lines}}, $first, $len, @replacement);
	};
	
	# reparse afpconf (and thereby do a final syntax check before writing) and write it
	my $afpconftxt = join($$afpconfRef{linesep}, @{$$afpconfRef{lines}});
	%$afpconfRef = %{parse_afpconf($afpconftxt)};
	write_afpconf($afpconftxt);
	
	return;
}

# delete_section_in_afpconf_ref_and_write
# 
# Parameters:
# - a reference to an afpconf structure as constructed by parse_afpconf
# - indices of sections to delete
#
# Checks the parameters for consistency, modifies the structure and
# writes out the afp.conf file.
#
sub delete_sections_in_afpconf_ref_and_write {
	my $afpconfRef = shift;

	# check indices and sort them backwards
	my @indices = sort { $b <=> $a } map {
		die "Index not numerical." unless(/^\s*(\d+)\s*$/);
		my $index = 1 * $1;
		die "Index doesn't exist." unless(exists ${$$afpconfRef{sectionsByIndex}}[$index]);
		$index;
	} @_;
	
	return unless(@indices);
	
	# delete the sections from the lines array
	map {
		my $sectionToModifyRef = ${$$afpconfRef{sectionsByIndex}}[$_];
		splice(@{$$afpconfRef{lines}}, $$sectionToModifyRef{firstline}, $$sectionToModifyRef{linecount});
	} @indices;
	
	# reparse afpconf (and thereby do a final syntax check before writing) and write it
	my $afpconftxt = join($$afpconfRef{linesep}, @{$$afpconfRef{lines}});
	%$afpconfRef = %{parse_afpconf($afpconftxt)};
	write_afpconf($afpconftxt);
	
	return;
}

sub split_into_users_and_groups {
	my $text = shift;

	my @users = ();
	my @groups = ();
	
	# user and group names are separated by spaces or commas
	# to allow for spaces in names, they may be enclosed in pairs of "
	# group names are prefixed with @ (if enclosing " then INSIDE of them)
	while($text =~ /[, ]*(".*?"|[^ ,]+)/g) {
		my $match = $1;
		if($match =~ s/^("?)@/$1/) {
			push @groups, $match;
		} else {
			push @users, $match;
		}
	}
	
	return (join(' ', @users), join(' ', @groups));
}

sub join_users_and_groups {
	my $users = shift;
	my $groups = shift;
	
	# prefix groups with @
	my @groups = ();
	while($groups =~ /[, ]*(".*?"|[^ ,]+)/g) {
		my $match = $1;
		$match =~ s/(^"?)/$1@/;
		push @groups, $match;
	}
	
	my @users = ();
	while($users =~ /[, ]*(".*?"|[^ ,]+)/g) {
		push @users, $1;
	}
	
	return join(' ', @users, @groups);
}

sub file_rotate {
  	my ($file) = @_;
    unlink($file . ".7");
    rename($file . ".6", $file . ".7");
    rename($file . ".5", $file . ".6");
    rename($file . ".4", $file . ".5");
    rename($file . ".3", $file . ".4");
    rename($file . ".2", $file . ".3");
    rename($file . ".1", $file . ".2");
    copy_source_dest($file, $file . ".1") or die "copy failed: $!";	# use function from web-lib-funcs.pl instead of File::Copy
}

sub read_license
{
    local %license;

    open(FH, "<", $config{'license_conf'}) || die "No license file found at the configured location: $config{'license_conf'}\n";
    while(defined($line = <FH>)) {
        chomp $line;
        if ($line =~ /serial:\s+(.*)/) {
            $license{"serial"} = $1;
        }
        if ($line =~ /expires:\s+(.*)/) {
            $license{"expires"} = $1;
        }
        if ($line =~ /users:\s+(.*)/) {
            $license{"users"} = $1;
        }
        if ($line =~ /key:\s+(.*)/) {
            $license{"key"} = $1;
        }
    }

    close(FH);
    return %license;
}

sub save_license
{
    my ($in) = @_;
    my $file = $config{'license_conf'};

    file_rotate($file);

    open(NEW, ">$file.tmp");

    print NEW "serial:  " . $in{"serial"} . "\n";
    print NEW "expires: " . $in{"expires"} . "\n";

    if ($in{"users"} ne "unlimited") {
        print NEW "users:   " . $in{"users"} . "\n";
    }
    print NEW "key:     " . $in{"key"} . "\n";

	close(NEW);

	rename($file, "$file.orig") or die "rename failed: $file -> $file.orig\n";
	rename("$file.tmp", $file) or die "rename failed: $file.tmp -> $file\n";
	unlink("$file.orig") or die "$text{delete_failed}: $file.orig\n";
}
