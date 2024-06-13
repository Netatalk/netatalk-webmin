#!/usr/bin/perl
# allmanual_save.cgi
# Save an entire config file
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

&ReadParseMime();

my @files = &getConfig();
&indexof($in{'file'}, @files) >= 0 || die $in{'file'};

my $temp = &transname();
system("cp ".quotemeta($in{'file'})." $temp");
$in{'data'} =~ s/\r//g;
&open_lock_tempfile(FILE, ">$in{'file'}");
&print_tempfile(FILE, $in{'data'});
&close_tempfile(FILE);
if ($config{'test_manual'}) {
	my $err = &test_config();
	if ($err) {
		system("mv $temp ".quotemeta($in{'file'}));
		die &text('manual_etest', "<pre>$err</pre>");
		}
	}
unlink($temp);
redirect("index.cgi");
