INSTALL_DIR = /usr/local/bython/


install: 
	mkdir -p $(INSTALL_DIR)
	cp -r src/* $(INSTALL_DIR)
	chmod +x $(INSTALL_DIR)bython.py
	chmod +x $(INSTALL_DIR)py2by.py
	ln -s $(INSTALL_DIR)bython.py /usr/local/bin/bython
	ln -s $(INSTALL_DIR)py2by.py /usr/local/bin/py2by
	cp etc/bython.1 /usr/local/share/man/man1/bython.1
	cp etc/py2by.1 /usr/local/share/man/man1/py2by.1
	mandb > /dev/null


uninstall:
	rm /usr/local/bin/bython
	rm /usr/local/bin/py2by
	rm -r $(INSTALL_DIR)*
	rmdir $(INSTALL_DIR)
	rm /usr/local/share/man/man1/bython.1
	rm /usr/local/share/man/man1/py2by.1
	mandb > /dev/null
