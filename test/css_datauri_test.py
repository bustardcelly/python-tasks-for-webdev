import sys, os, unittest
sys.path.append('../')
import css_url2uri

class TestURLToURI(unittest.TestCase):

	def test_temp_file_ext(self):
		path = 'walter.jpg'
		modified = css_url2uri.set_base64_filename_from_orig_path(path)
		stripped = css_url2uri.get_orig_filename_from_base64_file(modified)
		self.assertEqual(path, stripped)

	def test_relative_directory_path(self):
		rel = css_url2uri.relative_directory_path(os.path.join(os.getcwd(), 'style'), os.path.join(os.getcwd(), 'style/assets'))
		self.assertEqual(rel[1:], 'assets')
	
	def test_encode_to_base64(self):
		out = css_url2uri.encode_to_base64(os.path.join(os.getcwd(), 'assets/style/assets', 'walter.jpg'))
		self.assertTrue(out is not None)
		self.assertEqual(os.path.basename(out), 'walter.jpg.base64')
		os.remove(out)

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestURLToURI))
unittest.TextTestRunner(verbosity=2).run(suite)