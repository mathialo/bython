INSTALL_DIR = /usr/local/bython/


install: 
	mkdir -p $(INSTALL_DIR)
	cp -r src/* $(INSTALL_DIR)
	chmod +x $(INSTALL_DIR)bython.py
	ln -s $(INSTALL_DIR)bython.py /usr/local/bin/bython

update: 
	cp src/* $(INSTALL_DIR)

uninstall:
	rm /usr/local/bin/bython
	rm -r $(INSTALL_DIR)*
	rmdir $(INSTALL_DIR)
