from rtgraph.ui.mainWindow_ui import *

from rtgraph.core.worker import Worker
from rtgraph.core.constants import Constants, SourceType
from rtgraph.ui.popUp import PopUp
from rtgraph.common.logger import Logger as Log


TAG = "MainWindow"


class MainWindow(QtGui.QMainWindow):
    """
    Handles the ui elements and connects to worker service to execute processes.
    """
    def __init__(self, port=None, bd=115200, samples=500):
        """
        Initializes values for the UI.
        :param port: Default port name to be used. It will also disable scanning available ports.
        :type port: str.
        :param bd: Default baud rate to be used. It will be added to the common baud rate list if not available.
        :type bd: int.
        :param samples: Default samples per second to be shown in the plot.
        :type samples: int.
        """
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Shared variables, initial values
        self._plt = None
        self._timer_plot = None
        self.worker = Worker()

        # configures
        self.ui.cBox_Source.addItems(Constants.app_sources)
        self._configure_plot()
        self._configure_timers()
        self._configure_signals()

        # populate combo box for serial ports
        self._source_changed()
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
        self.worker = Worker(port=self.ui.cBox_Port.currentText(),
                             speed=float(self.ui.cBox_Speed.currentText()),
                             samples=self.ui.sBox_Samples.value(),
                             source=self._get_source(),
                             export_enabled=self.ui.chBox_export.isChecked())
        if self.worker.start():
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
        self.worker.stop()

    def closeEvent(self, evnt):
        """
        Overrides the QTCloseEvent.
        This function is connected to the clicked signal of the close button of the window.
        :param evnt: QT evnt.
        :return:
        """
        if self.worker.is_running():
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
        self.ui.cBox_Source.setEnabled(enabled)
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

    def _update_sample_size(self):
        """
        Updates the sample size of the plot.
        This function is connected to the valueChanged signal of the sample Spin Box.
        :return:
        """
        if self.worker is not None:
            Log.i(TAG, "Changing sample size")
            self.worker.reset_buffers(self.ui.sBox_Samples.value())

    def _update_plot(self):
        """
        Updates and redraws the graphics in the plot.
        This function us connected to the timeout signal of a QTimer.
        :return:
        """
        self.worker.consume_queue()

        # plot data
        self._plt.clear()
        for idx in range(self.worker.get_lines()):
            self._plt.plot(x=self.worker.get_time_buffer(),
                           y=self.worker.get_values_buffer(idx),
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

        source = self._get_source()
        ports = self.worker.get_source_ports(source)
        speeds = self.worker.get_source_speeds(source)

        if ports is not None:
            self.ui.cBox_Port.addItems(ports)
        if speeds is not None:
            self.ui.cBox_Speed.addItems(speeds)
        if self._get_source() == SourceType.serial:
            self.ui.cBox_Speed.setCurrentIndex(len(speeds) - 1)

    def _get_source(self):
        """
        Gets the current source type.
        :return: Current Source type.
        :rtype: SourceType.
        """
        return SourceType(self.ui.cBox_Source.currentIndex())
