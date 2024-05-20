#!/usr/bin/perl
# Action for deleting a file share
#
#    Netatalk Webmin Module
#    Copyright (C) 2000 Sven Mosimann/EcoLogic <sven.mosimann@ecologic.ch>
#    Copyright (C) 2013 Ralph Boehme <sloowfranklin@gmail.com>
#    Copyright (C) 2024 Daniel Markstedt <daniel@mindani>
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

require 'netatalk2-lib.pl';

eval {
	&ReadParse();

	my $applevolume_default = $config{'applevolumedefault_c'};
	my @paths = split(/\0/, $in{'section_index'});
	my @lines;

	foreach my $p (@paths) {
			unshift (@lines, getSpezLine($applevolume_default, $p));
	}

	foreach my $l (@lines){
		my $result = deleteSpezLine($applevolume_default, $l);
		if ($result == 0) {
			die($text{'edit_delete_error'})
		}
	}

	redirect("index.cgi");
};
if($@) {
	# in case the block above has been exited through "die": output error message
	my $msg = $@;

	ui_print_header(undef, $text{'error_title'}, "", "configs", 1, 1);
	print $msg;
	ui_print_footer("index.cgi", $text{'index_module'});

	exit;
}
