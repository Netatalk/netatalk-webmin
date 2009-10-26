#!/usr/bin/perl

#
#    Netatalk Webmin Module
#    Copyright (C) 2000 by Matthew Keller <kellermg@potsdam.edu>
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
#

do '../../web-lib.pl';
require '../netatalk-funcs.pl';


&header("Volume Config Help", "", undef, 1, 1);

my $CX="PRE";
print <<EOF;

<h3>the variables:</h3>
<$CX>
\$c   -> client's ip or appletalk address
\$f   -> full name (whatever's in the gecos field)
\$g   -> group
\$h   -> hostname
\$s   -> server name (can be the hostname)
\$u   -> username (if guest, it's whatever user guest is running as)
\$v   -> volume name (either ADEID_NAME or basename of path)
\$z   -> zone (may not exist)
\$\$   -> \$
</$CX>

<h3>casefold options [syntax: casefold:option]:</h3>
<$CX>
tolower    -> lowercases names in both directions
toupper    -> uppercases names in both directions
xlatelower -> client sees lowercase, server sees uppercase
xlateupper -> client sees uppercase, server sees lowercase
</$CX>

<h3>allow/deny/rwlist/rolist format [syntax: allow:user1,\@group]:</h3>
<$CX>
user1,\@group,user2  -> allows/denies access from listed users/groups
                       rwlist/rolist control whether or not the
                       volume is ro for those users.
</$CX>

<h3>miscellaneous options [syntax: options:option1,option2]:</h3>
<$CX>
prodos              -> make compatible with appleII clients.
crlf                -> enable crlf translation for TEXT files.
noadouble           -> don't create .AppleDouble unless a resource
                        fork needs to be created.
ro                  -> mount the volume as read-only.
mswindows           -> enforce filename restrictions imposed by MS
                        Windows. this will also invoke a default
                        codepage (iso8859-1) if one isn't already
                        specified.
nohex               -> don't do :hex translations for anything
                        except dot files. specify usedots as well if
                        you want that turned off. note: this option
                        makes the / character illegal.
usedots             -> don't do :hex translation for dot files. note: when
                        this option gets set, certain file names
                        become illegal. these are .Parent and
                        anything that starts with .Apple. also, dot
                        files created on the unix side are marked
                        invisible.
limitsize           -> limit disk size reporting to 2GB. this is
                        here for older macintoshes using newer
                        appleshare clients. yucko.

codepage:filename   -> load filename from nls directory.
dbpath:path         -> store the database stuff in the following path.
password:password   -> set a volume password (8 characters max) 

</$CX>
EOF
