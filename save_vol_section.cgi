#!/usr/bin/perl
#
# Netatalk Webmin Module
# Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
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
	
	&header($text{'errmsg_title'}, "", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\" target=\"_blank\">$text{help_configs}</a>");

	print "<p>$msg<p>";
	
	&footer("", $text{'edit_vol_section_return'});
	exit;
}

