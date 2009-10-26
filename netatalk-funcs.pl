
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

sub create_entry {
	my($filename,$line)=@_;
	unless($filename and $line) { die "Not enough infor for create_entry to work!\n"; }
	lock_file("$filename");
	open(CNF,">>$filename") or die "Cannot open $filename for appending: $!\n";
	print CNF "$line\n";
	close CNF;
	unlock_file("$filename");
}

sub startform {

	return "<form METHOD=\"POST\"  ENCTYPE=\"application/x-www-form-urlencoded\">";

}

sub checkbox {
	my $out="<INPUT TYPE=\"checkbox\" NAME=\"$_[0]\"";
	$out .= " VALUE=\"1\"";
	if(defined($_[1])) { $out .= " checked"; }
	$out .= ">";
	return $out;
}

sub textfield { # name,size,value
        my $out="<INPUT TYPE=\"text\" NAME=\"$_[0]\"";
        if($_[1]) {
                $out .= " SIZE=$_[1]";
        }
        if($_[2]) {
                $out .= " value=\"$_[2]\"";
        }
        $out .= ">";
}

sub td {
	return "<td>".join('',@_)."</td>";
}

sub TR {
        return "<tr>".join('',@_)."</tr>";
}

sub center {
	return "<center>".join('',@_)."</center>";
}

sub parse_str
{
	my $line = shift @_;
	local(@lines,@ret);

	@lines = split(/\s/,$line);

	while($#lines >= 0) {
		$_ = $lines[0];
		while((/^\"/ && !/\"$/) || ($_ eq "\"")) {
			$a = shift(@lines);
			$lines[0] = "$a $lines[0]";
			$_ = $lines[0];
		}
		$lines[0] =~ s/\"//g;

		push(@ret,shift(@lines));
	}
	return @ret;
}

1;
