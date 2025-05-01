PYTHON = python3
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
DOCS = docs
PLANTUML = java -jar ~/plantuml.jar

.PHONY: all
all: create-uml clean
	@echo "All done..."

.PHONY: create-docs-folder
create-docs-folder:
	mkdir -p $(DOCS)

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
	$(PLANTUML) ./uml/process.plantuml
	$(PLANTUML) ./uml/physical.plantuml
	$(PLANTUML) ./uml/developer.plantuml
	$(PLANTUML) ./uml/context.plantuml
	$(PLANTUML) ./uml/scenario.plantuml
	$(PLANTUML) ./uml/camera.plantuml
	$(PLANTUML) ./uml/mesh.plantuml
	$(PLANTUML) ./uml/point.plantuml
	$(PLANTUML) ./uml/engine.plantuml
	$(PLANTUML) ./uml/screen.plantuml
	$(PLANTUML) ./uml/interaction.plantuml
	@echo "UML diagrams created and saved in uml folder"

.PHONY: clean
clean:
	rm -rf `find . -type d -name __pycache__`
	rm -rf `find . -type d -name .pytest_cache`
	rm -rf `find . -type d -name .mypy_cache`
	rm -rf `find . -type d -name .hypothesis`
	rm -rf `find . -name .coverage`