vaticinator(6)
==============
v0.0.7
======

Vaticinator is yet another Python implementation of the
ancient and (in)famous `fortune` program from the 
`bsdgames` package.

My motivation for writing it was more to have a 
portable library I could use to fetch fortunes for
use in other projects.  It's possible that one or
more of the existing ones have this (I looked
albeit briefly), but it was an itch I didn't mind
scratching.

It is still alpha maturity level, though the majority 
of `fortune` behavior is implemented at the moment.

Example integration
=====================

This is a the code for a Django template tag that
displays a random fortune inside a template (with
all the options from the command line available).
This is basically why I created this project::

	from django.template import Library
	from vaticinator.vaticinator import Vaticinator

	register = Library()
	vaticinator = Vaticinator()

	@register.simple_tag
	def random_fortune(**kwargs):
		vaticinator.set_default_options()
		vaticinator.process_options(**kwargs)
		return vaticinator.fortune

And the template::

	<span>{% random_fortune 'short' 'all' %}</span>
