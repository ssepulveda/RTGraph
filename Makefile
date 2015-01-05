all: gui run

gui:
	pyuic4 gui.ui > gui.py

run:
	python main.py

clean:
	rm -r *.pyc
