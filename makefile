# display all the possible make commands
help:
	@echo "possible make commands:"
	@echo "    make lint         runs the various python linters"
	@echo "    make fix          runs black autofixer"
	@echo "    make tests        runs the testing suite"
	@echo "    make docs         generate the documentation pages (html)"
	@echo "    make opendocs     opens the documentation pages in a browser (utilizes xdg-open)"
	@echo "    make clean        deletes any .pyc files"

lint:
	pylint pytextdiff/*

tests:
	pytest pytextdiff/tests

docs: FORCE
	@cd docs; make html

opendocs: docs
	@cd docs/build/html; xdg-open index.html

clean:
	-rm pytextdiff/*.pyc
	-rm pytextdiff/tests/*.pyc

FORCE:
	
.PHONY: help, tests, docs, opendocs, lint, clean
