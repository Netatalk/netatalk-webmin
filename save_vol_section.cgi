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

require './netatalk3-lib.pl';

eval {
	&ReadParse();

	# rejoin parameters that have been split for the user interface
	$in{'p_valid users'} = join_users_and_groups(defined $in{'pu_valid_users'} ? $in{'pu_valid_users'} : '', defined $in{'pg_valid_users'} ? $in{'pg_valid_users'} : '');
	$in{'p_invalid users'} = join_users_and_groups(defined $in{'pu_invalid_users'} ? $in{'pu_invalid_users'} : '', defined $in{'pg_invalid_users'} ? $in{'pg_invalid_users'} : '');
	$in{'p_rolist'} = join_users_and_groups(defined $in{'pu_rolist'} ? $in{'pu_rolist'} : '', defined $in{'pg_rolist'} ? $in{'pg_rolist'} : '');
	$in{'p_rwlist'} = join_users_and_groups(defined $in{'pu_rwlist'} ? $in{'pu_rwlist'} : '', defined $in{'pg_rwlist'} ? $in{'pg_rwlist'} : '');

	my $afpconfRef = &read_afpconf();
	modify_afpconf_ref_and_write($afpconfRef, \%in);
	
	&redirect("");
};
if($@) {
	my $msg = $@;
	
	&header($text{'errmsg_title'}, "", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\">$text{help_configs}</a>");

	print "<p>$msg<p>";
	
	&footer("", $text{'edit_vol_section_return'});
	exit;
}

