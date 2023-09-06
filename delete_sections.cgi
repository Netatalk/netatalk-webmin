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

# process deletion request silently and redirect back to the index page
# only in case of error an error message is printed

eval {
	my $afpconfRef = &read_afpconf();
	
	&ReadParse();

	my @indices = split(/\0/, $in{'section_index'});
	delete_sections_in_afpconf_ref_and_write($afpconfRef, @indices);
	
	&redirect("");
};
if($@) {
	# in case the block above has been exited through "die": output error message
	my $msg = $@;
	
	&header($text{'errmsg_title'}, "", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\" target=\"_blank\">$text{help_configs}</a>");
	print $msg;
	&footer("", $text{'edit_return'});
	
	exit;
}

