# Depricated. Use setup.py instead for installation. Uninstall command is 
# included for backwards compatability for now, but will be removed in the
# future.

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


# The following part is not depricated. It is used to publish new versions to 
# PyPI

release: 
	-rm -r dist
	python3 setup.py sdist bdist_wheel
	twine upload dist/*


test-release: 
	-rm -r dist
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
