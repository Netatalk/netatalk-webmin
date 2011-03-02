# Makefile for Netatalk webmin module

FILES = \
	CHANGES \
	config \
	config.info \
	config-suse-linux \
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
	netatalk-funcs.pl \
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

clean:
	-rm netatalk-wbm.tgz
	-rm -rf netatalk-wbm

netatalk-wbm.tgz: $(FILES)
	@echo 'Creating Netatalk Webmin Module archive in "netatalk-wbm.tgz" ...'
	@-rm -rf netatalk-wbm
	@mkdir netatalk-wbm
	@tar cf - $(FILES) | tar xf - -C netatalk-wbm
	@tar cf - netatalk-wbm | gzip > netatalk-wbm.tgz
	@rm -rf netatalk-wbm
	@echo Done.
