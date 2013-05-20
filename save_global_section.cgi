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

	# properly join multiple values for uam list and canonicalize
	$in{'p_uam list'} =~ s/\x00/ /g;
	$in{'p_uam list'} =~ s/^[ ,]+//; $in{'p_uam list'} =~ s/[ ,]+$//; $in{'p_uam list'} =~ s/[ ,]+/ /g;

	# correct fields which had to be named without spaces catering for sloppy name handling in the webmin API
	$in{'p_k5 keytab'} = $in{'p_k5_keytab'}; delete $in{'p_k5_keytab'};
	$in{'p_vol dbpath'} = $in{'p_vol_dbpath'}; delete $in{'p_vol_dbpath'};
	$in{'p_log file'} = $in{'p_log_file'}; delete $in{'p_log_file'};

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
