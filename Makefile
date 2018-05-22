INSTALL_DIR = /usr/local/bython/


install: 
	mkdir -p $(INSTALL_DIR)
	cp -r src/* $(INSTALL_DIR)
	chmod +x $(INSTALL_DIR)bython.py
	chmod +x $(INSTALL_DIR)py2by.py
	chmod +x $(INSTALL_DIR)by2py.sh
	ln -s $(INSTALL_DIR)bython.py /usr/local/bin/bython
	ln -s $(INSTALL_DIR)py2by.py /usr/local/bin/py2by
	ln -s $(INSTALL_DIR)by2py.sh /usr/local/bin/by2py
	mkdir -p /usr/local/share/man/man1/
	cp etc/bython.1 /usr/local/share/man/man1/bython.1
	cp etc/py2by.1 /usr/local/share/man/man1/py2by.1
	cp etc/by2py.1 /usr/local/share/man/man1/by2py.1
	mandb > /dev/null


uninstall:
	-rm /usr/local/bin/bython
	-rm /usr/local/bin/py2by
	-rm /usr/local/bin/by2py
	-rm -r $(INSTALL_DIR)*
	-rmdir $(INSTALL_DIR)
	-rm /usr/local/share/man/man1/bython.1
	-rm /usr/local/share/man/man1/py2by.1
	-rm /usr/local/share/man/man1/by2py.1
	mandb > /dev/null
