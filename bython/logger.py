import sys


class Logger(object):
    """ Logger class. Writes errors and info to the cmd line. """

    def __init__(self, verbose=False):
        """
        Initialize a logger object.

        Args:
            verbose (boolean):      If True, the logger will print all status 
                                    updates and warnings, in addition to errors
        """
        self.verbose = verbose


    def log_info(self, text):
        """
        Log an info line, prefixed with an [i]. If verbose is False, this does
        nothing.

        Args:
            text (str):             Info text to print.
        """
        if self.verbose: print(" [i]  %s" % text)


    def log_warn(self, text):
        """
        Log a warning, prefixed with an [!]. If verbose is False, this does
        nothing.

        Args:
            text (str):             Warning text to print.
        """
        if self.verbose: print(" [!]  %s" % text)


    def program_header(self):
        """
        Print a header ment to separate info from compiler from the output of 
        the resulting program. If verbose is False, this does nothing.
        """
        if self.verbose: print("\n---- OUPUT FROM PROGRAM ----\n")


    def program_footer(self):
        """
        Print a footer ment to separate the output of the resulting program 
        from the info from compiler. If verbose is False, this does nothing.
        """        
        if self.verbose: print("\n----     END  OUPUT     ----\n")


    def log_error(self, text):
        """
        Log an error. This will be printed regardless of the status of the 
        verbose variable
        """
        print("\033[91m\033[1mError:\033[0m %s" % text, file=sys.stderr)
        

