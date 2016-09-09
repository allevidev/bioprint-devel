from __future__ import absolute_import

import bioprint.plugin


class TestSettingsPlugin(bioprint.plugin.SettingsPlugin):
	pass


__plugin_name__ = "Settings Plugin"
__plugin_description__ = "Test settings plugin"
__plugin_implementation__ = TestSettingsPlugin()