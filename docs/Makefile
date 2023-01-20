# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXAPIDOC  ?= sphinx-apidoc
APIDOCSOURCE  = ../taegel
SOURCEDIR     = .
BUILDDIR      = _build

GENDOC_ARGS          ?= --force -o $(SOURCEDIR) $(APIDOCSOURCE)
BUILD_ARGS           ?= -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
SPHINXBUILD_POETRY   ?= poetry run $(SPHINXBUILD)
SPHINXAPIDOC_POETRY  ?= poetry run $(SPHINXAPIDOC)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# NOTE: if the poetry command fails, it will try to run the pip installed one
%: Makefile
	@$(SPHINXAPIDOC_POETRY) $(GENDOC_ARGS) || $(SPHINXAPIDOC) $(GENDOC_ARGS) 
	@$(SPHINXBUILD_POETRY) $(BUILD_ARGS) || $(SPHINXBUILD) $(BUILD_ARGS)
