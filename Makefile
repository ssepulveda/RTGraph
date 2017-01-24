all: gui

gui:
	$(MAKE) -C rtgraph/res

run:
	python -m rtgraph -v

doc:
	$(MAKE) html -C docs

.PHONY: clean
clean:
	$(MAKE) clean -C rtgraph/res
	$(MAKE) clean -C docs
	rm -rf rtgraph/*.pyc
	rm -rf rtgraph/__pycache__
	rm -rf data