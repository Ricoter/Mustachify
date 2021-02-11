"""
Click is a simple Python module inspired by the stdlib optparse to make
writing command line scripts fun. Unlike other modules, it's based
around a simple API that does not come with too much magic and is
composable.
"""
from .core import (Argument, BaseCommand, Command, CommandCollection, Context,
                   Group, MultiCommand, Option, Parameter)
from .decorators import (argument, command, confirmation_option, group,
                         help_option, make_pass_decorator, option,
                         pass_context, pass_obj, password_option,
                         version_option)
from .exceptions import (Abort, BadArgumentUsage, BadOptionUsage, BadParameter,
                         ClickException, FileError, MissingParameter,
                         NoSuchOption, UsageError)
from .formatting import HelpFormatter, wrap_text
from .globals import get_current_context
from .parser import OptionParser
from .termui import (clear, confirm, echo_via_pager, edit, get_terminal_size,
                     getchar, launch, pause, progressbar, prompt, secho, style,
                     unstyle)
from .types import (BOOL, FLOAT, INT, STRING, UNPROCESSED, UUID, Choice,
                    DateTime, File, FloatRange, IntRange, ParamType, Path,
                    Tuple)
from .utils import (echo, format_filename, get_app_dir, get_binary_stream,
                    get_os_args, get_text_stream, open_file)

# Controls if click should emit the warning about the use of unicode
# literals.
disable_unicode_literals_warning = False

__version__ = "7.1.2"
