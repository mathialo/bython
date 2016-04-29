INSTALL_DIR = /usr/local/bython/


.PHONY: source


all: source

source:
	$(MAKE) -C $@

install: all
	mkdir $(INSTALL_DIR)
	cp binaries/* $(INSTALL_DIR)
	ln -s $(INSTALL_DIR)bython /usr/local/bin/bython

uninstall:
	rm /usr/local/bin/bython
	rm -r $(INSTALL_DIR)
