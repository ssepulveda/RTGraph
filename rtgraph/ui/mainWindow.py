import multiprocessing
from enum import Enum

from rtgraph.ui.mainWindow_ui import *

from rtgraph.common.logger import Logger as Log
from rtgraph.core.ringBuffer import RingBuffer
from rtgraph.core.constants import Constants, SourceType
from rtgraph.processors.Csv import CSVProcess
from rtgraph.processors.Parser import ParserProcess
from rtgraph.processors.Serial import SerialProcess
from rtgraph.processors.Simulator import SimulatorProcess
from rtgraph.ui.popUp import PopUp


TAG = "MainWindow"


class MainWindow(QtGui.QMainWindow):
    def __init__(self, port=None, bd=115200, samples=500):
        """
        Initializes values for the UI.
        :param port: Default port name to be used. It will also disable scanning available ports.
        :type port: basestring
        :param bd: Default baud rate to be used. It will be added to the common baud rate list if not available.
        :type bd: int
        :param samples: Default samples per second to be shown in the plot.
        :type samples: int
        """
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Shared variables, initial values
        self._plt = None
        self._timer_plot = None
        self._data_buffers = None
        self._time_buffer = None
        self._acquisition_process = None
        self._parser_process = None
        self._csv_process = None
        self.lines = 0
        self.queue = multiprocessing.Queue()

        # configures
        self.ui.cBox_Source.addItems(Constants.app_sources)
        self._configure_plot()
        self._configure_timers()
        self._configure_signals()

        # populate combo box for serial ports
        self.ui.cBox_Source.setCurrentIndex(SourceType.serial.value)

        self.ui.sBox_Samples.setValue(samples)

        # enable ui
        self._enable_ui(True)

    def start(self):
        """
        Starts the acquisition of the selected serial port.
        This function is connected to the clicked signal of the Start button.
        :return:
        """
        Log.i(TAG, "Clicked start")
        self._reset_buffers()
        port = self.ui.cBox_Port.currentText()
        if self.ui.chBox_export.isChecked():
            self._csv_process = CSVProcess(path=Constants.app_export_path)
            self._parser_process = ParserProcess(self.queue, store_reference=self._csv_process)
        else:
            self._parser_process = ParserProcess(self.queue)

        if self._get_source() == SourceType.serial:
            self._acquisition_process = SerialProcess(self._parser_process)
        elif self._get_source() == SourceType.simulator:
            self._acquisition_process = SimulatorProcess(self._parser_process)
        if self._acquisition_process.open(port=port, speed=float(self.ui.cBox_Speed.currentText())):
            self._parser_process.start()
            if self.ui.chBox_export.isChecked():
                self._csv_process.start()
            self._acquisition_process.start()
            self._timer_plot.start(Constants.plot_update_ms)
            self._enable_ui(False)
        else:
            Log.i(TAG, "Port is not available")
            PopUp.warning(self, Constants.app_title, "Selected port \"{}\" is not available"
                          .format(self.ui.cBox_Port.currentText()))

    def stop(self):
        """
        Stops the acquisition of the selected serial port.
        This function is connected to the clicked signal of the Stop button.
        :return:
        """
        Log.i(TAG, "Clicked stop")
        self._timer_plot.stop()
        self._enable_ui(True)
        if self._acquisition_process is not None and self._acquisition_process.is_alive():
            self._acquisition_process.stop()
            self._acquisition_process.join(Constants.process_join_timeout_ms)
            self._reset_buffers()

        if self._parser_process is not None and self._parser_process.is_alive():
            self._parser_process.stop()
            self._parser_process.join(Constants.process_join_timeout_ms)

        if self._csv_process is not None and self._csv_process.is_alive():
            self._csv_process.stop()
            self._csv_process.join(Constants.process_join_timeout_ms)

    def closeEvent(self, evnt):
        """
        Overrides the QTCloseEvent.
        This function is connected to the clicked signal of the close button of the window.
        :param evnt: QT evnt.
        :return:
        """
        if self._acquisition_process is not None and self._acquisition_process.is_alive():
            Log.i(TAG, "Window closed without stopping capture, stopping it")
            self.stop()

    def _enable_ui(self, enabled):
        """
        Enables or disables the UI elements of the window.
        :param enabled: The value to be set at the enabled characteristic of the UI elements.
        :type enabled: bool
        :return:
        """
        self.ui.cBox_Port.setEnabled(enabled)
        self.ui.cBox_Speed.setEnabled(enabled)
        self.ui.pButton_Start.setEnabled(enabled)
        self.ui.chBox_export.setEnabled(enabled)
        self.ui.pButton_Stop.setEnabled(not enabled)

    def _configure_plot(self):
        """
        Configures specific elements of the PyQtGraph plots.
        :return:
        """
        self.ui.plt.setBackground(background=None)
        self.ui.plt.setAntialiasing(True)
        self._plt = self.ui.plt.addPlot(row=1, col=1)
        self._plt.setLabel('bottom', Constants.plot_xlabel_title, Constants.plot_xlabel_unit)

    def _configure_timers(self):
        """
        Configures specific elements of the QTimers.
        :return:
        """
        self._timer_plot = QtCore.QTimer(self)
        self._timer_plot.timeout.connect(self._update_plot)

    def _configure_signals(self):
        """
        Configures the connections between signals and UI elements.
        :return:
        """
        self.ui.pButton_Start.clicked.connect(self.start)
        self.ui.pButton_Stop.clicked.connect(self.stop)
        self.ui.sBox_Samples.valueChanged.connect(self._update_sample_size)
        self.ui.cBox_Source.currentIndexChanged.connect(self._source_changed)

    def _reset_buffers(self):
        """
        Set up/clear the internal buffers used to store and display the signals.
        :return:
        """
        samples = self.ui.sBox_Samples.value()
        self._data_buffers = []
        for tmp in Constants.plot_colors:
            self._data_buffers.append(RingBuffer(samples))
        self._time_buffer = RingBuffer(samples)
        while not self.queue.empty():
            self.queue.get()
        Log.i(TAG, "Buffers cleared")

    def _update_sample_size(self):
        """
        Updates the sample size of the plot.
        This function is connected to the valueChanged signal of the sample Spin Box.
        :return:
        """
        Log.i(TAG, "Changing sample size")
        self._reset_buffers()

    def _update_plot(self):
        """
        Updates and redraws the graphics in the plot.
        This function us connected to the timeout signal of a QTimer.
        :return:
        """
        while not self.queue.empty():
            data = self.queue.get(False)

            # add timestamp
            self._time_buffer.append(data[0])
            value = data[1]

            # detect how many lines are present to plot
            size = len(value)
            if self.lines < size:
                if size > len(Constants.plot_colors):
                    self.lines = len(Constants.plot_colors)
                else:
                    self.lines = size

            # store the data in respective buffers
            for idx in range(self.lines):
                self._data_buffers[idx].append(value[idx])

        # plot data
        self._plt.clear()
        for idx in range(self.lines):
            self._plt.plot(x=self._time_buffer.get_all(),
                           y=self._data_buffers[idx].get_all(),
                           pen=Constants.plot_colors[idx])

    def _source_changed(self):
        """
        Updates the source and depending boxes on change.
        This function is connected to the indexValueChanged signal of the Source ComboBox.
        :return:
        """
        Log.i(TAG, "Scanning source {}".format(self._get_source().name))
        # clear boxes before adding new
        self.ui.cBox_Port.clear()
        self.ui.cBox_Speed.clear()

        if self._get_source() == SourceType.serial:
            speeds = SerialProcess.get_speeds()
            self.ui.cBox_Speed.addItems(speeds)
            self.ui.cBox_Speed.setCurrentIndex(len(speeds) - 1)
            ports = SerialProcess.get_ports()
            if len(ports) > 0:
                self.ui.cBox_Port.addItems(ports)
        elif self._get_source() == SourceType.simulator:
            self.ui.cBox_Speed.addItems(SimulatorProcess.get_speeds())
            self.ui.cBox_Port.addItems(SimulatorProcess.get_ports())
        else:
            Log.w(TAG, "Unknown source selected")

    def _get_source(self):
        """
        Gets the current source type.
        :return: Current Source type.
        :type: SourceType.
        """
        return SourceType(self.ui.cBox_Source.currentIndex())
