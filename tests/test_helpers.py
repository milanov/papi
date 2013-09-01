import sys
sys.path.append('/home/milan/Desktop/papi/')

import unittest
from os import mkdir, remove, rmdir
from os.path import abspath, join
from papi import helpers
import shutil

class TestHelpers(unittest.TestCase):


    def setUp(self):
        self.file_current_folder_name = "testfile.py"
        self.file_current_folder = open(self.file_current_folder_name, "w+")
        self.file_current_folder.close()

        self.not_package_folder_name = "notpackage"
        mkdir(self.not_package_folder_name)

        self.package_folder = "package_folder"
        mkdir(self.package_folder)
        self.init_name = "__init__.py"
        self.init_file = open(join(self.package_folder, self.init_name), "w+")
        self.init_file.close()
        self.file_package_name = "file_package.py"
        self.file_package = open(join(self.package_folder, self.file_package_name), "w+")
        self.file_package.close()

        self.inner_folder = "inner_folder"
        mkdir(join(self.package_folder, self.inner_folder))
        self.inner_file_name = "inner_file.py"
        self.inner_file = open(join(join(self.package_folder, self.inner_folder), self.inner_file_name), "w+")
        self.inner_init = open(join(join(self.package_folder, self.inner_folder), self.init_name), "w+")
        self.inner_file.close()
        self.inner_init.close()

    def tearDown(self):
        remove(abspath(self.file_current_folder_name))
        rmdir(abspath(self.not_package_folder_name))
        shutil.rmtree(abspath(self.package_folder))

    def test_ispackage_path_not_path(self):
        self.assertFalse(helpers.ispackage_path(self.file_current_folder_name))


    def test_ispackage_path_not_package(self):
        self.assertFalse(helpers.ispackage_path(abspath(self.not_package_folder_name)))


    def test_ispackage_path_is_package_path(self):
        self.assertTrue(helpers.ispackage_path(abspath(self.package_folder)))


    def test_safe_import_import(self):
        self.assertIsNotNone(helpers.safe_import("package_folder.file_package"))


    def test_safe_import_not_import(self):
        self.assertIsNone(helpers.safe_import("import_package.nonexisting"))

    def test_isattribute_is_attribute(self):
        attribute = 4
        self.assertTrue(helpers.isattribute(attribute))

    def test_isattribute_not_attribute(self):
        def not_attrubute():
            pass
        self.assertFalse(helpers.isattribute(not_attrubute))
    
    def test_visible_name_is_visible(self):
        def visible():
           pass
        self.assertTrue(helpers.visiblename(visible.__name__))

    def test_visible_name_not_visible(self):
        def __visible__():
           pass
        self.assertFalse(helpers.visiblename(__visible__.__name__))

    def test_extract_attributes_successfully(self):
        import testfile
        self.assertEqual([], helpers.extract_attributes(testfile))

    def test_extract_attributes_not_right(self):
        self.file_current_folder = open("testfile.py", "w")
        self.file_current_folder.write("variable = 5")

        import testfile
        self.assertNotEqual([], helpers.extract_attributes(self.file_current_folder))

        self.file_current_folder.truncate()
        self.file_current_folder.close()

    def test_extract_submodules_successfully(self):
      import package_folder
      import package_folder.file_package
      import package_folder.inner_folder
      import package_folder.inner_folder.inner_file

      expected = [package_folder.file_package, package_folder.inner_folder]
      module_tree = [package_folder, package_folder.file_package, package_folder.inner_folder, package_folder.inner_folder.inner_file]
      actual = helpers.extract_submodules(package_folder, module_tree)
      self.assertEqual(set(expected), set(actual))

if __name__ == '__main__' :
    unittest.main()
 