# coding=utf-8
from __future__ import absolute_import

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2014 The bioprint Project - Released under terms of the AGPLv3 License"


import io
import unittest
import mock

import bioprint.filemanager
import bioprint.filemanager.util

class FilemanagerMethodTest(unittest.TestCase):

	def setUp(self):
		# mock plugin manager
		self.plugin_manager_patcher = mock.patch("bioprint.plugin.plugin_manager")
		self.plugin_manager_getter = self.plugin_manager_patcher.start()

		self.plugin_manager = mock.MagicMock()

		hook_extensions = dict(
			some_plugin=lambda: dict(dict(machinecode=dict(foo=["foo", "f"]))),
			other_plugin=lambda: dict(dict(model=dict(amf=["amf"]))),
			mime_map=lambda: dict(
				mime_map=dict(
					mime_map_yes=bioprint.filemanager.ContentTypeMapping(["mime_map_yes"], "application/mime_map_yes")
				)
			),
			mime_detect=lambda: dict(
				dict(
					machinecode=dict(
						mime_detect_yes=bioprint.filemanager.ContentTypeDetector(["mime_detect_yes"], lambda x: "application/mime_detect_yes"),
						mime_detect_no=bioprint.filemanager.ContentTypeDetector(["mime_detect_no"], lambda x: None)
					)
				)
			)
		)
		self.plugin_manager.get_hooks.return_value = hook_extensions

		self.plugin_manager_getter.return_value = self.plugin_manager

	def tearDown(self):
		self.plugin_manager_patcher.stop()

	def test_full_extension_tree(self):
		full = bioprint.filemanager.full_extension_tree()
		self.assertTrue("machinecode" in full)
		self.assertTrue("gcode" in full["machinecode"])
		self.assertTrue(isinstance(full["machinecode"]["gcode"], bioprint.filemanager.ContentTypeMapping))
		self.assertItemsEqual(["gcode", "gco", "g"], full["machinecode"]["gcode"].extensions)
		self.assertTrue("foo" in full["machinecode"])
		self.assertTrue(isinstance(full["machinecode"]["foo"], list))
		self.assertItemsEqual(["f", "foo"], full["machinecode"]["foo"])

		self.assertTrue("model" in full)
		self.assertTrue("stl" in full["model"])
		self.assertTrue(isinstance(full["model"]["stl"], bioprint.filemanager.ContentTypeMapping))
		self.assertItemsEqual(["stl"], full["model"]["stl"].extensions)
		self.assertTrue("amf" in full["model"])
		self.assertTrue(isinstance(full["model"]["amf"], list))
		self.assertItemsEqual(["amf"], full["model"]["amf"])

	def test_get_mimetype(self):
		self.assertEquals(bioprint.filemanager.get_mime_type("foo.stl"), "application/sla")
		self.assertEquals(bioprint.filemanager.get_mime_type("foo.gcode"), "text/plain")
		self.assertEquals(bioprint.filemanager.get_mime_type("foo.unknown"), "application/octet-stream")
		self.assertEquals(bioprint.filemanager.get_mime_type("foo.mime_map_yes"), "application/mime_map_yes")
		self.assertEquals(bioprint.filemanager.get_mime_type("foo.mime_map_no"), "application/octet-stream")
		self.assertEquals(bioprint.filemanager.get_mime_type("foo.mime_detect_yes"), "application/mime_detect_yes")
		self.assertEquals(bioprint.filemanager.get_mime_type("foo.mime_detect_no"), "application/octet-stream")

	def test_valid_file_type(self):
		self.assertTrue(bioprint.filemanager.valid_file_type("foo.stl", type="model"))
		self.assertTrue(bioprint.filemanager.valid_file_type("foo.stl", type="stl"))
		self.assertFalse(bioprint.filemanager.valid_file_type("foo.stl", type="machinecode"))
		self.assertTrue(bioprint.filemanager.valid_file_type("foo.foo", type="machinecode"))
		self.assertTrue(bioprint.filemanager.valid_file_type("foo.foo", type="foo"))
		self.assertTrue(bioprint.filemanager.valid_file_type("foo.foo"))
		self.assertTrue(bioprint.filemanager.valid_file_type("foo.mime_map_yes"))
		self.assertTrue(bioprint.filemanager.valid_file_type("foo.mime_detect_yes"))
		self.assertFalse(bioprint.filemanager.valid_file_type("foo.unknown"))

	def test_get_file_type(self):
		self.assertEquals(["machinecode", "gcode"], bioprint.filemanager.get_file_type("foo.gcode"))
		self.assertEquals(["machinecode", "gcode"], bioprint.filemanager.get_file_type("foo.gco"))
		self.assertEquals(["machinecode", "foo"], bioprint.filemanager.get_file_type("foo.f"))
		self.assertEquals(["model", "stl"], bioprint.filemanager.get_file_type("foo.stl"))
		self.assertEquals(["model", "amf"], bioprint.filemanager.get_file_type("foo.amf"))
		self.assertIsNone(bioprint.filemanager.get_file_type("foo.unknown"))

	def test_hook_failure(self):
		def hook():
			raise RuntimeError("Boo!")
		self.plugin_manager.get_hooks.return_value = dict(hook=hook)

		with mock.patch("bioprint.filemanager.logging") as patched_logging:
			logger = mock.MagicMock()
			patched_logging.getLogger.return_value = logger

			bioprint.filemanager.get_all_extensions()

			self.assertEquals(1, len(logger.mock_calls))

class FileManagerTest(unittest.TestCase):

	def setUp(self):
		import bioprint.slicing
		import bioprint.filemanager.storage
		import bioprint.printer.profile

		self.addCleanup(self.cleanUp)

		# mock event manager
		self.event_manager_patcher = mock.patch("bioprint.filemanager.eventManager")
		event_manager = self.event_manager_patcher.start()
		event_manager.return_value.fire = mock.MagicMock()
		self.fire_event = event_manager.return_value.fire

		# mock plugin manager
		self.plugin_manager_patcher = mock.patch("bioprint.plugin.plugin_manager")
		self.plugin_manager = self.plugin_manager_patcher.start()

		self.analysis_queue = mock.MagicMock(spec=bioprint.filemanager.AnalysisQueue)

		self.slicing_manager = mock.MagicMock(spec=bioprint.slicing.SlicingManager)

		self.printer_profile_manager = mock.MagicMock(spec=bioprint.printer.profile.PrinterProfileManager)

		self.local_storage = mock.MagicMock(spec=bioprint.filemanager.storage.LocalFileStorage)
		self.local_storage.analysis_backlog = iter([])

		self.storage_managers = dict()
		self.storage_managers[bioprint.filemanager.FileDestinations.LOCAL] = self.local_storage

		self.file_manager = bioprint.filemanager.FileManager(self.analysis_queue, self.slicing_manager, self.printer_profile_manager, initial_storage_managers=self.storage_managers)

	def cleanUp(self):
		self.event_manager_patcher.stop()
		self.plugin_manager_patcher.stop()

	def test_add_file(self):
		wrapper = object()

		self.local_storage.add_file.return_value = ("", "test.file")
		self.local_storage.path_on_disk.return_value = "prefix/test.file"

		test_profile = dict(id="_default", name="My Default Profile")
		self.printer_profile_manager.get_current_or_default.return_value = test_profile

		file_path = self.file_manager.add_file(bioprint.filemanager.FileDestinations.LOCAL, "test.file", wrapper)

		self.assertEquals(("", "test.file"), file_path)
		self.local_storage.add_file.assert_called_once_with("test.file", wrapper, printer_profile=test_profile, allow_overwrite=False, links=None)
		self.fire_event.assert_called_once_with(bioprint.filemanager.Events.UPDATED_FILES, dict(type="printables"))

	def test_remove_file(self):
		self.file_manager.remove_file(bioprint.filemanager.FileDestinations.LOCAL, "test.file")

		self.local_storage.remove_file.assert_called_once_with("test.file")
		self.fire_event.assert_called_once_with(bioprint.filemanager.Events.UPDATED_FILES, dict(type="printables"))

	def test_add_folder(self):
		self.local_storage.add_folder.return_value = ("", "test_folder")

		folder_path = self.file_manager.add_folder(bioprint.filemanager.FileDestinations.LOCAL, "test_folder")

		self.assertEquals(("", "test_folder"), folder_path)
		self.local_storage.add_folder.assert_called_once_with("test_folder", ignore_existing=True)
		self.fire_event.assert_called_once_with(bioprint.filemanager.Events.UPDATED_FILES, dict(type="printables"))

	def test_add_folder_not_ignoring_existing(self):
		self.local_storage.add_folder.side_effect = RuntimeError("already there")

		try:
			self.file_manager.add_folder(bioprint.filemanager.FileDestinations.LOCAL, "test_folder", ignore_existing=False)
			self.fail("Expected an exception to occur!")
		except RuntimeError as e:
			self.assertEquals("already there", e.message)
		self.local_storage.add_folder.assert_called_once_with("test_folder", ignore_existing=False)

	def test_remove_folder(self):
		self.file_manager.remove_folder(bioprint.filemanager.FileDestinations.LOCAL, "test_folder")

		self.local_storage.remove_folder.assert_called_once_with("test_folder", recursive=True)
		self.fire_event.assert_called_once_with(bioprint.filemanager.Events.UPDATED_FILES, dict(type="printables"))

	def test_remove_folder_nonrecursive(self):
		self.file_manager.remove_folder(bioprint.filemanager.FileDestinations.LOCAL, "test_folder", recursive=False)
		self.local_storage.remove_folder.assert_called_once_with("test_folder", recursive=False)

	def test_get_metadata(self):
		expected = dict(key="value")
		self.local_storage.get_metadata.return_value = expected

		metadata = self.file_manager.get_metadata(bioprint.filemanager.FileDestinations.LOCAL, "test.file")

		self.assertEquals(metadata, expected)
		self.local_storage.get_metadata.assert_called_once_with("test.file")

	@mock.patch("bioprint.filemanager.util.atomic_write")
	@mock.patch("io.FileIO")
	@mock.patch("shutil.copyfileobj")
	@mock.patch("os.remove")
	@mock.patch("tempfile.NamedTemporaryFile")
	@mock.patch("time.time", side_effect=[1411979916.422, 1411979932.116])
	def test_slice(self, mocked_time, mocked_tempfile, mocked_os, mocked_shutil, mocked_fileio, mocked_atomic_write):
		callback = mock.MagicMock()
		callback_args = ("one", "two", "three")

		# mock temporary file
		temp_file = mock.MagicMock()
		temp_file.name = "tmp.file"
		mocked_tempfile.return_value = temp_file

		# mock metadata on local storage
		metadata = dict(hash="aabbccddeeff")
		self.local_storage.get_metadata.return_value = metadata

		# mock printer profile
		expected_printer_profile = dict(id="_default", name="My Default Profile")
		self.printer_profile_manager.get_current_or_default.return_value = expected_printer_profile
		self.printer_profile_manager.get.return_value = None

		# mock get_absolute_path method on local storage
		def path_on_disk(path):
			if isinstance(path, tuple):
				import os
				joined_path = ""
				for part in path:
					joined_path = os.path.join(joined_path, part)
				path = joined_path
			return "prefix/" + path
		self.local_storage.path_on_disk.side_effect = path_on_disk

		# mock split_path method on local storage
		def split_path(path):
			return "", path
		self.local_storage.split_path.side_effect = split_path

		# mock add_file method on local storage
		def add_file(path, file_obj, printer_profile=None, links=None, allow_overwrite=False):
			file_obj.save("prefix/" + path)
			return "", path
		self.local_storage.add_file.side_effect = add_file

		# mock slice method on slicing manager
		def slice(slicer_name, source_path, dest_path, profile, done_cb, printer_profile_id=None, position=None, callback_args=None, overrides=None, on_progress=None, on_progress_args=None, on_progress_kwargs=None):
			self.assertEquals("some_slicer", slicer_name)
			self.assertEquals("prefix/source.file", source_path)
			self.assertEquals("tmp.file", dest_path)
			self.assertIsNone(profile)
			self.assertIsNone(overrides)
			self.assertIsNone(printer_profile_id)
			self.assertIsNone(position)
			self.assertIsNotNone(on_progress)
			self.assertIsNotNone(on_progress_args)
			self.assertTupleEqual(("some_slicer", bioprint.filemanager.FileDestinations.LOCAL, "source.file", bioprint.filemanager.FileDestinations.LOCAL, "dest.file"), on_progress_args)
			self.assertIsNone(on_progress_kwargs)

			if not callback_args:
				callback_args = ()
			done_cb(*callback_args)
		self.slicing_manager.slice.side_effect = slice

		##~~ execute tested method
		self.file_manager.slice("some_slicer", bioprint.filemanager.FileDestinations.LOCAL, "source.file", bioprint.filemanager.FileDestinations.LOCAL, "dest.file", callback=callback, callback_args=callback_args)

		# assert that events where fired
		expected_events = [mock.call(bioprint.filemanager.Events.SLICING_STARTED, {"stl": "source.file", "gcode": "dest.file", "progressAvailable": False}),
		                   mock.call(bioprint.filemanager.Events.SLICING_DONE, {"stl": "source.file", "gcode": "dest.file", "time": 15.694000005722046})]
		self.fire_event.call_args_list = expected_events

		# assert that model links were added
		expected_links = [("model", dict(name="source.file"))]
		self.local_storage.add_file.assert_called_once_with("dest.file", mock.ANY, printer_profile=expected_printer_profile, allow_overwrite=True, links=expected_links)

		# assert that the generated gcode was manipulated as required
		expected_atomic_write_calls = [mock.call("prefix/dest.file", "wb")]
		self.assertEquals(mocked_atomic_write.call_args_list, expected_atomic_write_calls)
		#mocked_open.return_value.write.assert_called_once_with(";Generated from source.file aabbccddeeff\r")

		# assert that shutil was asked to copy the concatenated multistream
		self.assertEquals(1, len(mocked_shutil.call_args_list))
		shutil_call_args = mocked_shutil.call_args_list[0]
		self.assertTrue(isinstance(shutil_call_args[0][0], bioprint.filemanager.util.MultiStream))
		multi_stream = shutil_call_args[0][0]
		self.assertEquals(2, len(multi_stream.streams))
		self.assertTrue(isinstance(multi_stream.streams[0], io.BytesIO))

		# assert that the temporary file was deleted
		mocked_os.assert_called_once_with("tmp.file")

		# assert that our callback was called with the supplied arguments
		callback.assert_called_once_with(*callback_args)

	@mock.patch("os.remove")
	@mock.patch("tempfile.NamedTemporaryFile")
	@mock.patch("time.time", side_effect=[1411979916.422, 1411979932.116])
	def test_slice_error(self, mocked_time, mocked_tempfile, mocked_os):
		callback = mock.MagicMock()
		callback_args = ("one", "two", "three")

		# mock temporary file
		temp_file = mock.MagicMock()
		temp_file.name = "tmp.file"
		mocked_tempfile.return_value = temp_file

		# mock path_on_disk method on local storage
		def path_on_disk(path):
			if isinstance(path, tuple):
				import os
				joined_path = ""
				for part in path:
					joined_path = os.path.join(joined_path, part)
				path = joined_path
			return "prefix/" + path
		self.local_storage.path_on_disk.side_effect = path_on_disk

		# mock slice method on slicing manager
		def slice(slicer_name, source_path, dest_path, profile, done_cb, printer_profile_id=None, position=None, callback_args=None, overrides=None, on_progress=None, on_progress_args=None, on_progress_kwargs=None):
			self.assertEquals("some_slicer", slicer_name)
			self.assertEquals("prefix/source.file", source_path)
			self.assertEquals("tmp.file", dest_path)
			self.assertIsNone(profile)
			self.assertIsNone(overrides)
			self.assertIsNone(printer_profile_id)
			self.assertIsNone(position)
			self.assertIsNotNone(on_progress)
			self.assertIsNotNone(on_progress_args)
			self.assertTupleEqual(("some_slicer", bioprint.filemanager.FileDestinations.LOCAL, "source.file", bioprint.filemanager.FileDestinations.LOCAL, "dest.file"), on_progress_args)
			self.assertIsNone(on_progress_kwargs)

			if not callback_args:
				callback_args = ()
			done_cb(*callback_args, _error="Something went wrong")
		self.slicing_manager.slice.side_effect = slice

		##~~ execute tested method
		self.file_manager.slice("some_slicer", bioprint.filemanager.FileDestinations.LOCAL, "source.file", bioprint.filemanager.FileDestinations.LOCAL, "dest.file", callback=callback, callback_args=callback_args)

		# assert that events where fired
		expected_events = [mock.call(bioprint.filemanager.Events.SLICING_STARTED, {"stl": "source.file", "gcode": "dest.file"}),
		                   mock.call(bioprint.filemanager.Events.SLICING_FAILED, {"stl": "source.file", "gcode": "dest.file", "reason": "Something went wrong"})]
		self.fire_event.call_args_list = expected_events

		# assert that the temporary file was deleted
		mocked_os.assert_called_once_with("tmp.file")

		# assert that time.time was only called once
		mocked_time.assert_called_once()
