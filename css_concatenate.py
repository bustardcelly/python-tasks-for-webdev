"""Concatenates CSS files based on @import directives defined in a single CSS file."""

import sys, os, fileinput, re

double_quotes = re.compile('\"(.*?)\"')
single_quotes = re.compile('\'(.*?)\'')
non_quotes = re.compile('\((.*?)\)')
trials = [double_quotes, single_quotes, non_quotes]

def concat(filepath):
	"""Replaces @import directives with resource file contents."""
	path = filepath if os.path.isabs(filepath) else os.path.join(os.getcwd(), filepath)
	with open(path, 'r+') as f:
		if '@import' in f.read():
			for line in fileinput.input([path], inplace=1):
				if '@import' in line:
					url = get_path_from_import(line, 0)
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

def get_path_from_import(line, index):
	"""Returns path from @import directive, recursively going through matches to find possible declaration."""
	f = find_first_from(line, trials[index])
	if f:
		return f;
	elif index < len(trials) - 1:
		return get_path_from_import(line, index+1)
	else:
		return None

def get_directory_path(filepath):
	"""Returns the directory path from filepath."""
	absolute = filepath if os.path.isabs(filepath) else os.path.abspath(filepath)
	fullrel = os.path.split(absolute)
	return fullrel[0] if fullrel else None

if __name__ == '__main__':
	concat(sys.argv[1])