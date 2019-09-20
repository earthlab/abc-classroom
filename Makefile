docs: docs/*.rst docs/conf.py docs/Makefile abcclassroom/*.py *.rst #examples/*.py ## generate html docs
	#rm -f docs/earthpy.rst
	#rm -f docs/modules.rst
	sphinx-apidoc -fMeET -o docs/api abcclassroom #abc-classroom/tests
	$(MAKE) -C docs clean
	$(MAKE) -C docs doctest
	$(MAKE) -C docs html
	$(MAKE) -C docs linkcheck
