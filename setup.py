from setuptools import setup
from bython import VERSION_NUMBER

# Install python package, scripts and manual pages
setup(name="bython",
      version=VERSION_NUMBER,
      author="Mathias Lohne",
      email="mathialo@ifi.uio.no",
      license="MIT",
      scripts=["scripts/by2py", "scripts/bython", "scripts/py2by"],
      data_files=[("man/man1", ["etc/bython.1", "etc/py2by.1", "etc/by2py.1"])],
      packages=["bython"],
      zip_safe=False)