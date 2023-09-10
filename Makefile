# Makefile for Netatalk webmin module

FILES = \
	CHANGES \
	config \
	config.info \
	config-opt-netatalk \
	config-usr-local \
	server_create_form.cgi \
	CREDITS \
	fshare_delete_form.cgi \
	fshare_delete_action.cgi \
	server_delete_action.cgi \
	edit_configfiles_form.cgi \
	edit_configfiles_save.cgi \
	server_edit_form.cgi \
	fshare_create_form.cgi \
	help/configs.cgi \
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
	fshare_edit_form.cgi \
	module.info \
	netapple-lib.pl \
	README \
	restart.cgi \
	fshare_save_action.cgi \
	server_save_action.cgi \
	servers.cgi \
	show_users.cgi \
	start.cgi \
	stop.cgi \
	VERSION

all:

dist: netatalk2-wbm.tgz

localdist: netatalk2-local-wbm.tgz

optdist: netatalk2-opt-wbm.tgz

clean:
	-rm -f netatalk2-wbm.tgz netatalk2-local-wbm.tgz netatalk2-opt-wbm.tgz
	-rm -rf netapple

netatalk2-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "netatalk2-wbm.tgz" ...'
	@-rm -rf netatalk2 netatalk2-wbm.tgz
	@mkdir netapple
	@tar cf - $(FILES) | tar xf - -C netapple
	@tar cf - netapple | gzip > netatalk2-wbm.tgz
	@rm -rf netapple
	@echo Done.

netatalk2-local-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "netatalk2-local-wbm.tgz" ...'
	@-rm -rf netapple netatalk2-local-wbm.tgz
	@mkdir netapple
	@tar cf - $(FILES) | tar xf - -C netapple
	@cp config-usr-local netapple/config
	@tar cf - netapple | gzip > netatalk2-local-wbm.tgz
	@rm -rf netapple
	@echo Done.

netatalk2-opt-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "netatalk2-opt-wbm.tgz" ...'
	@-rm -rf netapple netatalk2-opt-wbm.tgz
	@mkdir netapple
	@tar cf - $(FILES) | tar xf - -C netapple
	@cp config-opt-netatalk netapple/config
	@tar cf - netapple | gzip > netatalk2-opt-wbm.tgz
	@rm -rf netapple
	@echo Done.
