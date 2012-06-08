import sys, unittest
sys.path.append('../')
import css_concatenate

class TestCSSConcat(unittest.TestCase):
	"""Testing concatenation from css-concatenate script."""

	def test_path_from_import_single_quotes(self):
		url = css_concatenate.get_path_from_import('@import url(\'one.css\')', 0)
		self.assertEqual(url, 'one.css')

	def test_path_from_import_double_quotes(self):
		url = css_concatenate.get_path_from_import('@import url("one.css")', 0)
		self.assertEqual(url, 'one.css')

	def test_path_from_import_non_quotes(self):
		url = css_concatenate.get_path_from_import('@import url(one.css)', 0)
		self.assertEqual(url, 'one.css')

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCSSConcat))
unittest.TextTestRunner(verbosity=2).run(suite)