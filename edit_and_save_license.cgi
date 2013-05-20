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

&header("License", "", undef(), 1, 1, undef(),"<a href=\"help/configs.cgi\">$text{help_configs}</a>");
&ReadParse();

%license = read_license();

if ($in{"action"} eq "save") {
    save_license($in);
}

print"<p><p>\n";

print &ui_hr();

if ($in{"action"} eq "save") {
    print "<p>Successfully saved license file<p><hr>";
} else {
	print"<p><p>\n";

	print &ui_form_start('edit_and_save_license.cgi', 'POST', undef, 'name="configform"');

	print &ui_hidden("action", "save");

	print &ui_table_start("License", 'width="100%"', 2);
	print &ui_table_row("Serial", "<input size=30 name=serial value=$license{'serial'}>");
	print &ui_table_row("Expires", "<input size=30 name=expires value=$license{'expires'}>");
	print &ui_table_row("Users", "<input size=30 name=users value=".($license{'users'} || "unlimited").">");
	print &ui_table_row("Key", "<input size=30 name=key value=$license{'key'}>");
	print &ui_table_end();

	print &ui_form_end([[undef, $text{'save_button_title'}, 0, undef]]);

	print &ui_hr();
}
print "<p><p>\n";

&footer("", $text{'edit_return'});
