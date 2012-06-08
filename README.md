python-tasks-for-webdev
=======================

handful of python scripts to facilitate in web development and deployment.

#css-concatenate#
Concatenates url resource contents declared in @import directives of a single file.
###example###
_directory structure_

	|-project
		|---tools
			+- css-concatenate.py
		|---style
			+- main.css
			+- one.css
			+- two.css
		+- index.html

_main.css_

	@import url("one.css");
	@import url("two.css");
	body {
		margin: 0;
		padding: 0;
	}

_one.css_
	
	ul {
		list-style: none;
	}

_two.css_

	a {
		text-decoration: none;
	}


###usage###

	$project> ./tools/css-concatenate.py ./style/main.css

###produces###
_main.css_

	ul {
		list-style: none;
	}
	a {
		text-decoration: none;
	}
	body {
		margin: 0;
		padding: 0;
	}

##known shortcomings##
* Currently only supports @import from local disk.
* Not recursive; if resource itself has @imports, does not replace those.
* Overwrites to input file.

#css_url2uri#
Data URI util.

Traverses a directory and encodes asset files to base64 and replaces relative URL references in CSS files with the base64 string.
###example###
_directory structure_

	|-project
		|---tools
			+- css_url2uri.py
		|---style
			|-----assets
				+- image.png
			+- main.css

_main.css_

	.background {
		background-image: url('assets/image.png')
	}

###usage##
	
	$project> ./tools/css_url2uri.py ./style

###produces###
_main.css_

	.walter {
		background-image: url('data:img/jpg;base64,/9j/4AAQSkZJRgABAQ...'
	}

##known shortcomings##
* Overwrites CSS files; no option for -output directory. As such, it is recommended first to copy all files over to a distribution directory before running the css_url2uri task.
* Finds only relative paths in CSS.
