#!/usr/bin/env python3

"""Provide file operation functions."""

import os
import syslog


def cat(file_name):
    """Read a file (line-by-line) into a variable.

    Args:
        file_name (str) : file to read from

    Returns:
          (str) : file contents
    """
    contents = ""
    if os.path.isfile(file_name):
        with open(file_name, "r", encoding="utf-8") as file_stream:
            contents = file_stream.read().strip("\n")
    return contents


def syslog_trace(trace, logerr, out2console=False):
    """Log a (multi-line) message to syslog.
    Initialise with a call to
    syslog.openlog(ident=<string>, facility=<syslog.facility>)

    Args:
        trace (str): Text to send to log
        logerr (int): syslog errornumber
        out2console (bool): If True, will also print the 'trace' to the screen

    Returns:
        None
    """
    log_lines = trace.split("\n")
    for line in log_lines:
        if line and logerr:
            syslog.syslog(logerr, line)
        if line and out2console:
            print(line)
