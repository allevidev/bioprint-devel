# coding=utf-8
from __future__ import absolute_import

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2015 The bioprint Project - Released under terms of the AGPLv3 License"

import bioprint.plugin

class VirtualPrinterPlugin(bioprint.plugin.SettingsPlugin):

    def virtual_printer_factory(self, comm_instance, port, baudrate, read_timeout):
        if not port == "VIRTUAL":
            return None

        if not self._settings.global_get_boolean(["devel", "virtualPrinter", "enabled"]):
            return None

        from . import virtual
        serial_obj = virtual.VirtualPrinter(read_timeout=float(read_timeout))
        return serial_obj

__plugin_name__ = "Virtual Printer"
__plugin_author__ = "Gina Häußge, based on work by Daid Braam"
__plugin_homepage__ = "https://github.com/foosel/bioprint/wiki/Plugin:-Virtual-Printer"
__plugin_license__ = "AGPLv3"
__plugin_description__ = "Provides a virtual printer via a virtual serial port for development and testing purposes"

def __plugin_load__():
    plugin = VirtualPrinterPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_hooks__
    __plugin_hooks__ = {
        "bioprint.comm.transport.serial.factory": plugin.virtual_printer_factory
    }
