# installation guide
To install simply open a terminal, move to the top directory of the bython folder, and type
	
	> git clone https://github.com/mathialo/bython.git
	> cd bython
	> sudo make install


If you allready have an installation of bython, but have downloaded a new version and want to update, type

	> sudo make update


If you want to uninstall bython, type

	> sudo make uninstall


### custom install dir
Bython will automatically install itself to "/usr/local/bython/". If you for some reason want to change this, open the Makefile in the top directory and change the line (no 1):
``` 
INSTALL_DIR = /usr/local/bython/
```
to be whereever you want. The file copying and link creation will now use your new directory.
