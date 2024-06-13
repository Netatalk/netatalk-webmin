#!/usr/bin/perl
# allmanual_form.cgi
# Display a text box for manually editing directives from one of the files
#
# Copyright (c) Jamie Cameron
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Modifications for Netatalk:
# Copyright (C) 2024 Daniel Markstedt <daniel@mindani.net>

require 'netatalk2-lib.pl';

&ReadParse();

&ui_print_header(undef, $text{'manual_configs'}, "", "configs", 1);

my @files = &getConfig();
$in{'file'} = $files[0] if (!$in{'file'});
&indexof($in{'file'}, @files) >= 0 || &error($text{'manual_efile'});

# File selector
print &ui_form_start("allmanual_form.cgi");
print &ui_submit($text{'manual_file'}),"\n";
print &ui_select("file", $in{'file'}, \@files);
print &ui_form_end();

# File editor
print &ui_form_start("allmanual_save.cgi", "form-data");
print &ui_hidden("file", $in{'file'});
print &ui_table_start(undef, undef, 2);
print &ui_table_row(undef,
	&ui_textarea("data", &read_file_contents($in{'file'}), 20, 80), 2);
print &ui_table_end();
print &ui_form_end([ [ undef, $text{'save'} ] ]);

&ui_print_footer("index.cgi", $text{'index_module'});
