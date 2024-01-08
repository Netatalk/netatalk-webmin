# Makefile for Netatalk webmin module

WEBMIN_DIR ?= /usr/share/webmin
VERSION=`cat module.info |grep version |sed 's/version=//'`

FILES = \
	CHANGES \
	COPYING \
	CREDITS \
	README.md \
	config* \
	module.info \
	netatalk2-lib.pl \
	*.cgi \
	help/** \
	images/** \
	lang/**

all: netatalk2-wbm.tgz

dist: netatalk2-wbm.tgz

localdist: netatalk2-local-wbm.tgz

optdist: netatalk2-opt-wbm.tgz

install:
	@${WEBMIN_DIR}/install-module.pl netatalk2-wbm-${VERSION}.tgz

clean:
	-rm -f netatalk*.tgz
	-rm -rf netatalk2

netatalk2-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive in \"netatalk2-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk2
	@mkdir netatalk2
	@tar cf - $(FILES) | tar xf - -C netatalk2
	@tar cf - netatalk2 | gzip > netatalk2-wbm-${VERSION}.tgz
	@rm -rf netatalk2
	@echo Done.

netatalk2-local-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive in \"netatalk2-local-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk2
	@mkdir netatalk2
	@tar cf - $(FILES) | tar xf - -C netatalk2
	@cp config-usr-local netatalk2/config
	@tar cf - netatalk2 | gzip > netatalk2-local-wbm-${VERSION}.tgz
	@rm -rf netatalk2
	@echo Done.

netatalk2-opt-wbm.tgz: $(FILES)
	@echo "Creating Netatalk Webmin Module archive in \"netatalk2-opt-wbm-${VERSION}.tgz\" ..."
	@-rm -rf netatalk2
	@mkdir netatalk2
	@tar cf - $(FILES) | tar xf - -C netatalk2
	@cp config-opt-netatalk netatalk2/config
	@tar cf - netatalk2 | gzip > netatalk2-opt-wbm-${VERSION}.tgz
	@rm -rf netatalk2
	@echo Done.
