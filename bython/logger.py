import sys


class Logger(object):
	""" Logger class. Writes errors and info to the cmd line. """

	def __init__(self, verbose=False):
		self.verbose = verbose

	def log_info(self, text):
		if self.verbose: print(" [i]  %s" % text)

	def log_warn(self, text):
		if self.verbose: print(" [!]  %s" % text)

	def program_header(self):
		if self.verbose: print("\n---- OUPUT FROM PROGRAM ----\n")

	def program_footer(self):
		if self.verbose: print("\n----     END  OUPUT     ----\n")

	def log_error(self, text):
		print("\033[91m\033[1mError:\033[0m %s" % text, file=sys.stderr)
		

