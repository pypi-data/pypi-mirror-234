# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
# PyGTK is pain in the ass.
# There is not a day goes by I don't feel regret
# for my decision to implement OS-level indicators.
import gi

# try which gir is available prioritising Gtk3
gi.require_version("AppIndicator3", "0.1")
try:
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
except ImportError:
    try:
        from gi.repository import AppIndicator3 as AppIndicator
    except ImportError:
        from gi.repository import AppIndicator as AppIndicator  # noqa

gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
try:
    from gi.repository import Gtk as Gtk
    from gi.repository import GLib as GLib
    from gi.repository import Notify as Notify
    from gi.repository.Gtk import Menu as Menu
    from gi.repository.Gtk import MenuItem as MenuItem
    from gi.repository.Gtk import CheckMenuItem as CheckMenuItem
    from gi.repository.Gtk import RadioMenuItem as RadioMenuItem
    from gi.repository.Gtk import SeparatorMenuItem as SeparatorMenuItem
except ImportError as e:
    raise RuntimeError("Gtk dependencies not found") from e

# ------------------------------------------------------------------------------
# here imports should be absolute:
from es7s.gtk._entrypoint import invoke as entrypoint_fn  # noqa

from .indicator import *  # noqa
