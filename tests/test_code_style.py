import unittest
import pep8
import os.path


tests_dir = os.path.dirname(__file__)
module_fn = os.path.abspath(os.path.join(tests_dir, "..", "flask_tiedye.py"))


class TestCodeStyle(unittest.TestCase):

    def test_pep8_conformance(self):
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files([tests_dir, module_fn])
        self.assertEqual(
            result.total_errors,
            0,
            "Found pep8 conformance issues",
        )
