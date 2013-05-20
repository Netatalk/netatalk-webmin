# Makefile for Netatalk webmin module

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
	help/configs.cgi \
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
	restart.cgi \
	save_global_section.cgi \
	save_vol_section.cgi \
	show_users.cgi \
	start.cgi \
	stop.cgi \
	VERSION

all:

dist: netatalk-wbm.tgz

localdist: local-wbm.tgz

optdist: opt-wbm.tgz

clean:
	-rm -f netatalk-wbm.tgz local-wbm.tgz opt-wbm.tgz
	-rm -rf netatalk-wbm

netatalk-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "netatalk-wbm.tgz" ...'
	@-rm -rf netatalk-wbm netatalk-wbm.tgz
	@mkdir netatalk-wbm
	@tar cf - $(FILES) | tar xf - -C netatalk-wbm
	@tar cf - netatalk-wbm | gzip > netatalk-wbm.tgz
	@rm -rf netatalk-wbm
	@echo Done.

local-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "local-wbm.tgz" ...'
	@-rm -rf netatalk-wbm local-wbm.tgz
	@mkdir netatalk-wbm
	@tar cf - $(FILES) | tar xf - -C netatalk-wbm
	@cp config-usr-local-netatalk netatalk-wbm/config
	@tar cf - netatalk-wbm | gzip > local-wbm.tgz
	@rm -rf netatalk-wbm
	@echo Done.

opt-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "opt-wbm.tgz" ...'
	@-rm -rf netatalk-wbm opt-wbm.tgz
	@mkdir netatalk-wbm
	@tar cf - $(FILES) | tar xf - -C netatalk-wbm
	@cp config-opt-netatalk netatalk-wbm/config
	@tar cf - netatalk-wbm | gzip > opt-wbm.tgz
	@rm -rf netatalk-wbm
	@echo Done.
