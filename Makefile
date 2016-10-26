all: gui

gui:
	$(MAKE) -C res

run:
	python3 src/RTGraph.py

clean:
	rm -rf *.pyc
	rm -rf *.log*
	rm -rf src/*.log
	rm -rf __pycache__
