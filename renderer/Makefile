PYTHON = python3
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
DOCS = docs
PLANTUML = java -jar ~/plantuml.jar

.PHONY: all
all: fix-style style-check type-check unittest create-cov-report clean
	@echo "All done..."

.PHONY: unittest
unittest:
	$(PYTHON) -m pytest -v

.PHONY: type-check
type-check:
	$(TYPE_CHECK) .

.PHONY: style-check
style-check:
	flake8 .

.PHONY: fix-style
fix-style:
	autopep8 --in-place --recursive --aggressive --aggressive .

.PHONY: create-docs-folder
create-docs-folder:
	mkdir -p $(DOCS)

.PHONY: create-docs
create-docs: create-docs-folder
	pdoc --output-dir $(DOCS)/code-docs \
		geometry \
		scene \
		utility \
		engine.py

.PHONY: create-cov-report
create-cov-report:
	@pytest --verbose --color=yes --cov=geometry --cov=scene --cov=utility --cov=engine --cov-report term --cov-report=html:$(DOCS)/pycov tests/
	@echo "Coverage report created in $(DOCS)/pycov folder"

.PHONY: create-uml
create-uml: create-docs-folder
# use shell command which to check if java is installed and is in the $PATH
ifeq ($(shell which java), )
	$(error "No java found in $(PATH). Install java to run plantuml")
endif
# use wildcard function to check if file exists
ifeq ($(wildcard ~/plantuml.jar), )
	@echo "Downloading plantuml.jar in home folder..."
	curl -L -o ~/plantuml.jar https://sourceforge.net/projects/plantuml/files/plantuml.jar/download
	sudo apt install graphviz
endif
	$(PLANTUML) ./uml/example.plantuml
	@echo "UML diagrams created and saved in uml folder"

.PHONY: clean
clean:
	rm -rf `find . -type d -name __pycache__`
	rm -rf `find . -type d -name .pytest_cache`
	rm -rf `find . -type d -name .mypy_cache`
	rm -rf `find . -type d -name .hypothesis`
	rm -rf `find . -name .coverage`