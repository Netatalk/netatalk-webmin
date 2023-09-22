# Makefile for Netatalk webmin module

WEBMIN_DIR ?= /usr/share/webmin

FILES = \
	CHANGES \
	config \
	config.info \
	config-opt-netatalk \
	config-suse-linux \
	config-usr-local-netatalk \
	delete_sections.cgi \
	edit_global_section.cgi \
	edit_vol_section.cgi \
	help/configs.html \
	images/icon.gif \
	images/interface.png \
	images/misc.png \
	images/server.png \
	images/users.png \
	images/volumes.gif \
	index.cgi \
	lang/de \
	lang/en \
	module.info \
	netatalk3-lib.pl \
	README.md \
	restart.cgi \
	save_global_section.cgi \
	save_vol_section.cgi \
	show_users.cgi \
	start.cgi \
	stop.cgi \
	VERSION

all:

dist: netatalk3-wbm.tgz

localdist: netatalk3-local-wbm.tgz

optdist: netatalk3-opt-wbm.tgz

install:
	@${WEBMIN_DIR}/install-module.pl netatalk3*-wbm.tgz

clean:
	-rm -f netatalk3-wbm.tgz netatalk3-local-wbm.tgz netatalk3-opt-wbm.tgz
	-rm -rf netatalk3

netatalk3-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "netatalk3-wbm.tgz" ...'
	@-rm -rf netatalk3 netatalk3-wbm.tgz
	@mkdir netatalk3
	@tar cf - $(FILES) | tar xf - -C netatalk3
	@tar cf - netatalk3 | gzip > netatalk3-wbm.tgz
	@rm -rf netatalk3
	@echo Done.

netatalk3-local-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "netatalk3-local-wbm.tgz" ...'
	@-rm -rf netatalk3 netatalk3-local-wbm.tgz
	@mkdir netatalk3
	@tar cf - $(FILES) | tar xf - -C netatalk3
	@cp config-usr-local-netatalk netatalk3/config
	@tar cf - netatalk3 | gzip > netatalk3-local-wbm.tgz
	@rm -rf netatalk3
	@echo Done.

netatalk3-opt-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "netatalk3-opt-wbm.tgz" ...'
	@-rm -rf netatalk3 netatalk3-opt-wbm.tgz
	@mkdir netatalk3
	@tar cf - $(FILES) | tar xf - -C netatalk3
	@cp config-opt-netatalk netatalk3/config
	@tar cf - netatalk3 | gzip > netatalk3-opt-wbm.tgz
	@rm -rf netatalk3
	@echo Done.
