from setuptools import setup
from bython import VERSION_NUMBER

with open("README.md", "r") as fh:
    long_description = fh.read()

# Install python package, scripts and manual pages
setup(name="bython",
      version=VERSION_NUMBER,
      author="Mathias Lohne",
      author_email="mathialo@ifi.uio.no",
      license="MIT",
      description="Python with braces",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/mathialo/bython",
      scripts=["scripts/by2py", "scripts/bython", "scripts/py2by"],
      data_files=[("man/man1", ["etc/bython.1", "etc/py2by.1", "etc/by2py.1"])],
      packages=["bython"],
      zip_safe=False)