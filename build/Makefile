clean:
	@echo "+ $@"
	rm -rf build/lib/
	rm -rf dist/

build: clean
	@echo "+ $@"
	python setup.py sdist bdist_wheel


push:
	@echo "+ $@"
	twine upload dist/* -r pypi

.PHONY: build