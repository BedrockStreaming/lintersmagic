"""
magic function that checks a cell for pep8 compliance, using pycodestyle
%pycodestyle_on
a=1
should give an error about missing spaces
"""

__version__ = "0.5"

import sys
import tempfile
import io
import os
import logging
import pycodestyle as pycodestyle_module

from IPython.core.magic import register_cell_magic
from IPython.core.magic import register_line_magic
from IPython.core import magic_arguments

vw = None
init_pycodestyle = False
ignore_codes = []
max_line_length = 79


class VarWatcher(object):
    # https://ipython.readthedocs.io/en/stable/config/callbacks.html
    def __init__(self, ip):
        self.shell = ip

    def auto_run_pycodestyle(self, result):
        pycodestyle(1, result.info.raw_cell)
        if result.error_before_exec:
            print("Error before execution: %s" % result.error_before_exec)


def load_ipython_extension(ipython, pck=""):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    if pck == "":
        global vw
        vw = VarWatcher(ipython)
    if pck == "pycodestyle":
        ipython.events.register("post_run_cell", vw.auto_run_pycodestyle)
    pass


def unload_ipython_extension(ipython, pck=""):
    # If you want your extension to be unloadable, put that logic here.
    if pck == "pycodestyle":
        ipython.events.unregister("post_run_cell", vw.auto_run_pycodestyle)
        global init_pycodestyle
        init_pycodestyle = False
    pass


@magic_arguments.magic_arguments()
@magic_arguments.argument(
    "--ignore", "-i", help="ignore option, comma separated errors"
)
@magic_arguments.argument("--max_line_length", "-m", help="set the max length")
@register_line_magic
def pycodestyle_on(line):
    # validate for any options
    args = magic_arguments.parse_argstring(pycodestyle_on, line)
    # check ignore codes
    global ignore_codes
    if args.ignore:
        ignore_codes = list(set(ignore_codes + args.ignore.split(",")))

    # check max-line-length
    global max_line_length
    if args.max_line_length:
        max_line_length = int(args.max_line_length)
    load_ipython_extension(vw.shell, pck="pycodestyle")


@register_line_magic
def pycodestyle_off(line):
    unload_ipython_extension(vw.shell, pck="pycodestyle")


@register_cell_magic
def pycodestyle(line, cell):
    """pycodestyle cell magic for pep8"""
    global init_pycodestyle
    if not init_pycodestyle:
        init_pycodestyle = True

    # output is written to stdout
    sys.stdout = io.StringIO()
    # store code in a file
    if cell.startswith(("!", "%%", "%")):
        return
    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as file:
        # save to file
        file.write("# The %%pycodestyle cell magic was here\n" + cell + "\n")
        # make sure it's written
        file.flush()
        file.close()
    # now we can check the file by name.
    # we might be able to use 'stdin', have to check implementation
    format = "%(row)d:%(col)d: %(code)s %(text)s"
    pycodestyle = pycodestyle_module.StyleGuide(
        format=format, ignore=ignore_codes, max_line_length=max_line_length
    )
    # check the filename
    pycodestyle.check_files(paths=[file.name])
    # split lines
    stdout = sys.stdout.getvalue().splitlines()

    for line in stdout:
        # on windows drive path also contains :
        line, col, error = line.split(":")[-4:]

        logging.warning("{}:{}:{}".format(int(line) + 0, col, error))
        # restore
    try:
        os.remove(file.name)
    except OSError as e:
        logging.error("Error: %s - %s." % (e.filename, e.strerror))
    return
