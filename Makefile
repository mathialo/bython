INSTALL_DIR = /usr/local/bython/


.PHONY: source


all: source

source:
	$(MAKE) -C $@

install: source
	mkdir -p $(INSTALL_DIR)
	cp binaries/* $(INSTALL_DIR)
	ln -s $(INSTALL_DIR)bython /usr/local/bin/bython

update: source
	cp binaries/* $(INSTALL_DIR)

uninstall:
	rm /usr/local/bin/bython
	rm $(INSTALL_DIR)*
	rmdir $(INSTALL_DIR)
