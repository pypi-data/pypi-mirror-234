"""
Created on 27 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A stdio abstraction, implementing ProcessComms

WARNING: macOS (darwin) users must install the gnureadline package

https://sites.google.com/site/xiangyangsite/home/technical-tips/software-development/python/python-readline-completions
https://stackoverflow.com/questions/675370/tab-completion-in-python-interpreter-in-os-x-terminal
https://stackoverflow.com/questions/70735564/python-readline-module-giving-permissionerror-errno-1-only-when-run-at-startu
"""

import os
import sys
import termios

from getpass import getpass

from scs_core.sys.logging import Logging
from scs_core.sys.process_comms import ProcessComms

try:
    import gnureadline as readline
except ImportError:
    import readline


# --------------------------------------------------------------------------------------------------------------------

class StdIO(ProcessComms):
    """
    classdocs
    """

    __HISTORY_LENGTH =  100
    __VOCABULARY = []

    __READLINE_COMPLETION_DEFAULT = 'tab: complete'
    # __READLINE_COMPLETION_DARWIN = 'bind ^I rl_complete'

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def prompt(request, default=None):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        try:
            prompt_str = request + ' (%s): ' % default if default else request + ': '
        except TypeError:
            prompt_str = request + ': '                             # no % format in request string

        line = input(prompt_str).strip()

        return line if line else default


    @staticmethod
    def password(request):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        return getpass(request).strip()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def set(cls, vocabulary=(), history_filename=None):
        # completion...
        cls.__VOCABULARY = vocabulary

        binding = cls.__READLINE_COMPLETION_DEFAULT
        # binding = cls.__READLINE_COMPLETION_DARWIN if sys.platform == 'darwin' else cls.__READLINE_COMPLETION_DEFAULT

        readline.parse_and_bind(binding)
        readline.set_completer(cls.completer)

        # history...
        if history_filename:
            cls.load_history(history_filename)


    @classmethod
    def clear(cls):
        cls.__VOCABULARY = ()
        readline.set_completer()
        readline.clear_history()


    @classmethod
    def completer(cls, text, state):
        results = [token for token in cls.__VOCABULARY if token.startswith(text)]

        return results[state]


    @classmethod
    def load_history(cls, filename):
        if os.path.exists(filename):
            try:
                readline.read_history_file(filename)
            except PermissionError as ex:
                logger = Logging.getLogger()
                logger.error("PermissionError: %s: %s" % (filename, ex))


    @classmethod
    def save_history(cls, filename):
        readline.set_history_length(cls.__HISTORY_LENGTH)
        readline.write_history_file(filename)


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, wait_for_availability=True):
        pass


    def close(self):
        sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------

    def read(self):
        for line in sys.stdin:
            yield line.strip()


    def write(self, message, wait_for_availability=True):           # message should be flushed on close
        print(message.strip())
