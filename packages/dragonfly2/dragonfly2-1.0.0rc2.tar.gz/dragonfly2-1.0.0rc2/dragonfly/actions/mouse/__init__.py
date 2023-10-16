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
This module initializes the mouse interface for the current platform.
"""

import sys

from dragonfly._platform_checks import IS_X11

# Import mouse events common to each platform.
from ._base import (EventBase, PauseEvent, MoveEvent, MoveRelativeEvent,
                    MoveScreenEvent, MoveWindowEvent)


# Import the mouse functions and classes for the current platform.
if sys.platform == "win32":
    from ._win32 import (
        ButtonEvent, get_cursor_position, set_cursor_position,
        PLATFORM_BUTTON_FLAGS, PLATFORM_WHEEL_FLAGS
    )

elif sys.platform == "darwin":
    from ._pynput import (
        ButtonEvent, get_cursor_position, set_cursor_position,
        PLATFORM_BUTTON_FLAGS, PLATFORM_WHEEL_FLAGS
    )

elif IS_X11:
    try:
        # Prefer pynput over xdotool since it supports horizontal scrolling
        #  and the extra mouse buttons.
        from ._pynput import (
            ButtonEvent, get_cursor_position, set_cursor_position,
            PLATFORM_BUTTON_FLAGS, PLATFORM_WHEEL_FLAGS
        )
    except ImportError:
        from ._xdotool import (
            ButtonEvent, get_cursor_position, set_cursor_position,
            PLATFORM_BUTTON_FLAGS, PLATFORM_WHEEL_FLAGS
        )

else:
    # No mouse interface is available. Dragonfly can function
    # without this functionality, so don't raise an error or log any
    # messages. Errors/messages will occur later if the mouse is used.
    from ._base import (
        BaseButtonEvent as ButtonEvent, get_cursor_position,
        set_cursor_position, PLATFORM_BUTTON_FLAGS, PLATFORM_WHEEL_FLAGS
    )


# Ensure all button and wheel flag names are accounted for.
# Used for debugging. Uncomment if adding new buttons or aliases.
# _BUTTON_NAMES = ["left", "right", "middle", "four", "five"]
# _WHEEL_NAMES = ["wheelup", "stepup", "wheeldown", "stepdown",
#                 "wheelright", "stepright", "wheelleft", "stepleft"]
# assert sorted(PLATFORM_BUTTON_FLAGS.keys()) == sorted(_BUTTON_NAMES),\
#     "Mouse implementation is missing button flags"
# assert sorted(PLATFORM_WHEEL_FLAGS.keys()) == sorted(_WHEEL_NAMES),\
#     "Mouse implementation is missing wheel flags"
