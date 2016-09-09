# coding=utf-8
from __future__ import absolute_import

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2014 The bioprint Project - Released under terms of the AGPLv3 License"

import bioprint.plugin


class TestMixedPlugin(bioprint.plugin.StartupPlugin, bioprint.plugin.SettingsPlugin):
	pass


__plugin_name__ = "Mixed Plugin"
__plugin_description__ = "Test mixed plugin"
__plugin_implementation__ = TestMixedPlugin()