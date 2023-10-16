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
This module initializes the keyboard interface for the current platform.
"""

import sys

from dragonfly._platform_checks import IS_X11

# Import the keyboard classes for the current platform.
if sys.platform == "win32":
    from ._win32 import (
        Win32Keyboard as Keyboard,
        Win32Typeable as Typeable,
        Win32KeySymbols as KeySymbols
    )

elif sys.platform == "darwin":
    from ._pynput import (
        PynputKeyboard as Keyboard,
        PynputTypeable as Typeable,
        DarwinKeySymbols as KeySymbols
    )

elif IS_X11:
    # Import classes for X11.  This is typically used on Unix-like systems.
    # The DISPLAY environment variable is normally set in an X11 session.
    #  If it is not, it may be set manually in ~/.profile or equivalent.
    from ._x11_base import (
        X11Typeable as Typeable,
        XdoKeySymbols as KeySymbols
    )

    # Import the keyboard for typing through xdotool.
    from ._x11_xdotool import XdotoolKeyboard as Keyboard

    # The libxdo implementation doesn't work with Python 3, so it is not
    #  used.
    # from ._x11_libxdo import LibxdoKeyboard as Keyboard

else:
    # No keyboard implementation is available. Dragonfly can function
    #  without a keyboard class, so don't raise an error or log any
    #  messages.  Error messages will occur later if and when keyboard
    #  events are sent.
    from ._base import (
        BaseKeyboard as Keyboard,
        BaseTypeable as Typeable,
        MockKeySymbols as KeySymbols
    )

# Initialize a Keyboard instance.
keyboard = Keyboard()
