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

ci-push:
	@echo "+ $@"
	twine upload -u $(PYPI_USERNAME) -p $(PYPI_PASSWORD) dist/* -r pypi

.PHONY: build