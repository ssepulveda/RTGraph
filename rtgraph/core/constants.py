from enum import Enum


class Constants:
    app_title = "RTGraph"
    app_version = '0.2.0'
    app_export_path = "data"
    app_sources = ["Serial", "Simulator"]
    app_encoding = "utf-8"

    plot_update_ms = 16
    plot_xlabel_title = "Time"
    plot_xlabel_unit = "s"
    plot_colors = ['#0072bd', '#d95319', '#edb120', '#7e2f8e', '#77ac30', '#4dbeee', '#a2142f']

    process_join_timeout_ms = 1000

    argument_default_samples = 500

    serial_default_speed = 115200
    serial_timeout_ms = 0.5

    simulator_default_speed = 0.002

    csv_default_filename = "%Y-%m-%d_%H-%M-%S"
    csv_delimiter = ","
    csv_extension = "csv"

    parser_timeout_ms = 0.05

    log_filename = "{}.log".format(app_title)
    log_max_bytes = 5120
    log_default_level = 1
    log_default_console_log = False


class MinimalPython:
    major = 3
    minor = 2
    release = 0


class SourceType(Enum):
    simulator = 1
    serial = 0

