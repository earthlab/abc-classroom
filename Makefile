docs: docs/*.rst docs/conf.py docs/Makefile abcclassroom/*.py *.rst #examples/*.py ## generate html docs
	sphinx-apidoc -fMeET -o docs/api abcclassroom #abc-classroom/tests
	$(MAKE) -C docs clean
	$(MAKE) -C docs doctest
	$(MAKE) -C docs html
	$(MAKE) -C docs linkcheck
