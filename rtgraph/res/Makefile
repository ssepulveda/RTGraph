# UI files from qt
UI_FILES = $(wildcard *.ui)

# Resources files from qt
RES_FILES = $(wildcard *.qrc)

### CONFIGURABLE
OUT_FOLDER = ../ui/

# Binaries
PYUIC = pyuic5
PYRCC = pyrcc5
# PYUIC = pyuic4
# PYRCC = pyrcc4

PY_UI_FILES = $(UI_FILES:%.ui=%_ui.py)
PY_RES_FILES = $(RES_FILES:%.qrc=%_rc.py)

all : resources ui

resources : $(PY_RES_FILES)
%_rc.py : %.qrc
	$(PYRCC) $< -o $(OUT_FOLDER)$@

ui : $(PY_UI_FILES)
%_ui.py : %.ui
	$(PYUIC) $< -o $(OUT_FOLDER)$@

clean :
	$(RM) $(OUT_FOLDER)$(PY_UI_FILES)
#	$(RM) $(OUT_FOLDER)$(PY_RES_FILES)