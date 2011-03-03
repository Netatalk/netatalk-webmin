# Makefile for Netatalk webmin module

FILES = \
	CHANGES \
	config \
	config.info \
	config-suse-linux \
	config-opt-netatalk \
	config-usr-local-netatalk \
	create_server.cgi \
	CREDITS \
	delete_fshare.cgi \
	delete_FShare.cgi \
	delete_server.cgi \
	edit_configfiles_form.cgi \
	edit_configfiles_save.cgi \
	editexist_server.cgi \
	edit_fshare.cgi \
	edit_server.cgi \
	help/configs.cgi \
	help/volumehelp.cgi \
	images/edit.gif \
	images/icon.gif \
	images/interface.png \
	images/misc.png \
	images/server.png \
	images/users.png \
	images/volumes.gif \
	index.cgi \
	lang/de \
	lang/en \
	misc_opt.cgi \
	modi_fshare.cgi \
	module.info \
	netapple-lib.pl \
	README \
	restart.cgi \
	save_fshare.cgi \
	save_Modi_FShare.cgi \
	save_newServer.cgi \
	servers.cgi \
	settings.cgi \
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
