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

all: netatalk-wbm.tgz

dist: netatalk-wbm.tgz

localdist: netatalk-local-wbm.tgz

optdist: netatalk-opt-wbm.tgz

install:
	@${WEBMIN_DIR}/install-module.pl netatalk-wbm-${VERSION}.tgz

clean:
	-rm -f netatalk*.tgz
	-rm -rf netatalk

netatalk-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive for distribution: \"netatalk-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk
	@mkdir netatalk
	@tar cf - $(FILES) | tar xf - -C netatalk
	@tar cf - netatalk | gzip > netatalk-wbm-${VERSION}.tgz
	@rm -rf netatalk
	@echo Done.

netatalk-local-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive for distribution \"netatalk-local-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk
	@mkdir netatalk
	@tar cf - $(FILES) | tar xf - -C netatalk
	@cp config-usr-local-netatalk netatalk/config
	@tar cf - netatalk | gzip > netatalk-local-wbm-${VERSION}.tgz
	@rm -rf netatalk
	@echo Done.

netatalk-opt-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive for distribution: \"netatalk-opt-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk
	@mkdir netatalk
	@tar cf - $(FILES) | tar xf - -C netatalk
	@cp config-opt-netatalk netatalk/config
	@tar cf - netatalk | gzip > netatalk-opt-wbm-${VERSION}.tgz
	@rm -rf netatalk
	@echo Done.
