"""Concatenates CSS files based on @import directives defined in a single CSS file."""

import sys, os, fileinput, re

double = re.compile('\"(.*?)\"')
single = re.compile('\'(.*?)\'')

def concat(filepath):
	"""Replaces @import directives with resource file contents."""
	path = filepath if os.path.isabs(filepath) else os.path.join(os.getcwd(), filepath)
	with open(path, 'r+') as f:
		if '@import' in f.read():
			for line in fileinput.input([path], inplace=1):
				if '@import' in line:
					url = get_path_from_import(line)
					relpath = url if os.path.isabs(url) else get_directory_path(filepath) + '/' + url
					if os.path.exists(relpath):
						with open(relpath, 'r') as resource:
							sys.stdout.write(resource.read())
					else:
						sys.stdout.write(line)
				else:
					sys.stdout.write(line)

def find_first_from(line, exp):
	"""Returns first item in matched expression if found, otherwise None."""
	found = re.findall(exp, line)
	return found[0] if found else None

def get_path_from_import(line):
	"""Returns path from @import directive."""
	f = find_first_from(line, double)
	return f if f else find_first_from(line, single)

def get_directory_path(filepath):
	"""Returns the directory path from filepath."""
	absolute = filepath if os.path.isabs(filepath) else os.path.abspath(filepath)
	fullrel = os.path.split(absolute)
	return fullrel[0] if fullrel else None

if __name__ == '__main__':
	concat(sys.argv[1])