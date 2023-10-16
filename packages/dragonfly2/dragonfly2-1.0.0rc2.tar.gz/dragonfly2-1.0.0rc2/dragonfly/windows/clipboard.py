#
# This file is part of Dragonfly.
# (c) Copyright 2007, 2008 by Christo Butcher
# Licensed under the LGPL.
#
#   Dragonfly is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dragonfly is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with Dragonfly.  If not, see
#   <http://www.gnu.org/licenses/>.
#

"""
This module initializes the clipboard interface for the current platform.
"""

import os
import sys

from dragonfly._platform_checks                 import IS_X11
from dragonfly.windows.base_clipboard           import BaseClipboard


# Import the clipboard classes and functions for the current platform.
if sys.platform == "win32":
    from dragonfly.windows.win32_clipboard      import \
        Win32Clipboard as Clipboard, win32_clipboard_ctx

elif sys.platform == "darwin":
    from dragonfly.windows.pyperclip_clipboard  import \
        PyperclipClipboard as Clipboard

elif IS_X11:
    from dragonfly.windows.x11_clipboard        import \
        XselClipboard as Clipboard

else:
    from dragonfly.windows.base_clipboard       import \
        BaseClipboard as Clipboard
