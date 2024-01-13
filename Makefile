# Makefile for Netatalk webmin module

WEBMIN_DIR ?= /usr/share/webmin
ifneq ($(wildcard /usr/libexec/webmin),)
	WEBMIN_DIR := /usr/libexec/webmin
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
	netatalk3-lib.pl \
	*.cgi

all: netatalk3-wbm.tgz

dist: netatalk3-wbm.tgz

localdist: netatalk3-local-wbm.tgz

optdist: netatalk3-opt-wbm.tgz

install:
	@${WEBMIN_DIR}/install-module.pl netatalk3-wbm-${VERSION}.tgz

clean:
	-rm -f netatalk*.tgz
	-rm -rf netatalk3

netatalk3-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive for distribution: \"netatalk3-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk3
	@mkdir netatalk3
	@tar cf - $(FILES) | tar xf - -C netatalk3
	@tar cf - netatalk3 | gzip > netatalk3-wbm-${VERSION}.tgz
	@rm -rf netatalk3
	@echo Done.

netatalk3-local-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive for distribution \"netatalk3-local-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk3
	@mkdir netatalk3
	@tar cf - $(FILES) | tar xf - -C netatalk3
	@cp config-usr-local-netatalk netatalk3/config
	@tar cf - netatalk3 | gzip > netatalk3-local-wbm-${VERSION}.tgz
	@rm -rf netatalk3
	@echo Done.

netatalk3-opt-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive for distribution: \"netatalk3-opt-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk3
	@mkdir netatalk3
	@tar cf - $(FILES) | tar xf - -C netatalk3
	@cp config-opt-netatalk netatalk3/config
	@tar cf - netatalk3 | gzip > netatalk3-opt-wbm-${VERSION}.tgz
	@rm -rf netatalk3
	@echo Done.
