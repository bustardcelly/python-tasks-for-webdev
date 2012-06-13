"""Encodes image assets to base64 and replaces references to relative URL within CSS.
	(c) Todd Anderson 2012 - http://www.custardbelly.com/blog, @_toddanderson_
"""
import sys, os, fileinput, re

valid_img = re.compile('([^\s]+(\.(?i)(jpg|jpeg|png|gif|bmp))$)')

def relative_directory_path(rootDirectory, subDirectory):
	"""Returns the relative path to subDirectory from rootDirectory.
	   relative_directory_path('style', 'style/assets')
	   prints 'assets'
	"""
	common = os.path.commonprefix([rootDirectory, subDirectory])
	if len(common) > 0:
		return subDirectory.split(common)[1][1:]
	return ''

def set_base64_filename_from_orig_path(filepath):
	"""Will save down base64 encoded data from a file with the following naming convention: filename.(png|jpg).base64"""
	return os.path.join(os.path.dirname(filepath), os.path.basename(filepath) + '.base64')

def get_orig_filename_from_base64_file(filepath):
	"""Files encoded with base64 take on the following naming convention: filename.(png|jpg).base64.
	   When saving down a file, use set_base64_filename_from_orig_path() to return expected results from this method.
	"""
	return os.path.splitext(os.path.basename(filepath))[0]

def encode_to_base64(filepath):
	"""Reads in filepath, encodes to base64 and writes out to ${filepath}.base64"""
	with open(filepath, 'rb') as f:
		data = f.read().encode('base64').replace('\n', '')
	if data is not None:
		outpath = set_base64_filename_from_orig_path(filepath)
		with open(outpath, 'w') as f:
			f.write(data)
		return outpath
	return None

def encode_files_from_directory(assetDirectory):
	"""Traverses directory looking for image asset files to encode to base64."""
	for root, dirs, files in os.walk(assetDirectory):
		for file in files:
			# ensure that the extension is image file.
			if re.match(valid_img, os.path.basename(file)) is None:
				continue

			output = encode_to_base64(os.path.join(root,file))
			if output is not None:
				print('Encoded and saved {0}.'.format(output))
			else:
				print('Could not encode {0} to base64.'.format(os.path.basename(file)))

def replace_url_with_base64(directory):
	"""Reads each *.base64 file in directory and replaces url directives in CSS."""
	print('Replacing url directives with data:URI base64 from {0}...'.format(directory))
	for root, dirs, files in os.walk(directory):
		for file in files:
			if os.path.splitext(file)[1][1:] != 'base64':
					continue

			with open(os.path.join(root,file), 'r') as f:
				filename = get_orig_filename_from_base64_file(file)
				ext = os.path.splitext(filename)[1][1:]
				filepath = os.path.join(relative_directory_path(directory, os.path.dirname(os.path.join(root,file))), filename)
				replace_in_file(filepath, 'data:img/{0};base64,{1}'.format(ext,f.read()), directory)

			os.remove(os.path.join(root,file))

def replace_in_file(strToFind, strToReplace, cssDirectory):
	"""Finds and replaces strings within CSS files from specified directory."""
	print('Locating {0} in files from {1}....'.format(strToFind, str(cssDirectory)));
	for root, dirs, files in os.walk(cssDirectory):
		for file in files:
			filepath = os.path.join(root,file)
			# if not a css file, continue
			if os.path.splitext(filepath)[1][1:] != 'css':
				continue

			f = open(filepath);
			if strToFind in f.read():
				print('Found {0} in {1}.'.format(strToFind, filepath))
				for line in fileinput.input([filepath], inplace=1):
					if strToFind in line:
						line = line.replace(strToFind, strToReplace)
					sys.stdout.write(line)
			f.close()

if __name__ == '__main__':
	"""Expects path to directory with CSS files and assets to be base64 encoded.
	   Traveres a directory and encodes al files matching /([^\s]+(\.(?i)(jpg|jpeg|png|gif|bmp))$)/, then locates the declaration of each file in CSS and replaces with base64 string (data:uri)self.

	   $> python css_datauri style/
	"""
	directory = sys.argv[1] if os.path.isabs(sys.argv[1]) else os.path.abspath(sys.argv[1])

	encode_files_from_directory(directory)
	replace_url_with_base64(directory)




