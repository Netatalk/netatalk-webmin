#!/usr/bin/env bash
set -e

MODULE="netatalk"
TARBALL="$MODULE.wbm.gz"
FILES="help/** images/** lang/** CHANGES COPYING README.md config* module.info *.cgi *.pl"

echo "Creating Netatalk Webmin Module distribution tarball..."
echo "$TARBALL"
tar -zcf ./${TARBALL} ./${FILES}
