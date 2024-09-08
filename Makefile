# Makefile for Netatalk webmin module

WEBMIN_DIR ?= /usr/share/webmin
ifneq ($(wildcard /usr/libexec/webmin),)
	WEBMIN_DIR := /usr/libexec/webmin
else ifneq ($(wildcard /opt/webmin),)
	WEBMIN_DIR := /opt/webmin
endif

VERSION=`cat module.info |grep version |sed 's/version=//'`

FILES = \
	help/** \
	images/** \
	lang/** \
	CHANGES \
	COPYING \
	README.md \
	config* \
	module.info \
	netatalk-lib.pl \
	*.cgi

all: $(FILES)
	@echo "Creating Netatalk Webmin Module archive for distribution: \"netatalk-${VERSION}.wbm.gz\" ..."
	@-rm -rf netatalk
	@mkdir netatalk
	@tar cf - $(FILES) | tar xf - -C netatalk
	@tar cf - netatalk | gzip > netatalk-${VERSION}.wbm.gz
	@rm -rf netatalk
	@echo Done.

install:
	@${WEBMIN_DIR}/install-module.pl netatalk-${VERSION}.wbm.gz

clean:
	-rm -f netatalk-*.wbm.gz
	-rm -rf netatalk
