python-tasks-for-webdev
=======================

handful of python scripts to facilitate in web development and deployment.

#css-concatenate#
Concatenates url resource contents declared in @import directives of a single file.
###example###
_directory structure_

	|-project
		|-tools
			-css-concatenate.py
		|-style
			-main.css
			-one.css
			-two.css
		-index.html

_main.css_

	@import(url="one.css");
	@import(url="two.css");
	body {
		margin: 0;
		padding: 0;
	}

###usage###

	$project> ./tools/css-concatenate.py ./style/main.css

##known shortcomings##
* Currently only supports @import from local disk.
* Overwrites to input file