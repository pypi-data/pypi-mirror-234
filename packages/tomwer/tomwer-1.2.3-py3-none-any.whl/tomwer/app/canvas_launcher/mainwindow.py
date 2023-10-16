import argparse
import logging
import os
import shutil
import signal
import sys
from typing import List
from contextlib import closing
from logging.handlers import RotatingFileHandler
from urllib.request import urlopen
from xml.sax.saxutils import escape

import pyqtgraph
from orangecanvas.application.canvasmain import DockWidget
from orangecanvas.application.outputview import (
    ExceptHook,
    TerminalTextDocument,
    TextStream,
)
from orangecanvas.document.usagestatistics import UsageStatistics
from orangecanvas.main import Main as ocMain
from orangewidget.workflow import config
from orangewidget.workflow.config import data_dir_base
from orangewidget.workflow.errorreporting import handle_exception
from orangewidget.workflow.mainwindow import OWCanvasMainWindow as _MainWindow
from processview.gui.processmanager import ProcessManagerWindow
from silx.gui import qt

import tomwer.version
from tomwer.core.log.logger import TomwerLogger
from orangecanvas.preview import previewdialog, previewmodel
from orangecanvas.application import examples as orange_examples
import ewoks
import tomoscan.version

from .config import TomwerConfig, TomwerSplashScreen

try:
    import nabu
except ImportError:
    has_nabu = False
else:
    has_nabu = True
try:
    import nxtomomill.version
except ImportError:
    has_nxtomomill = False
else:
    has_nxtomomill = True
try:
    import nxtomo
except ImportError:
    has_nxotmo = False
else:
    has_nxotmo = True
try:
    import sluurp
except ImportError:
    has_sluurp = False
else:
    has_sluurp = True

_logger = logging.getLogger(__file__)

MAX_LOG_FILE = 10
"""Maximal log file kepts for orange"""

LOG_FILE_NAME = "tomwer.log"

LOG_FOLDER = "/var/log/tomwer"


class MainWindow(_MainWindow):
    HELPDESK_URL = "https://requests.esrf.fr/plugins/servlet/desk/portal/41"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_supervisor_dock = DockWidget(
            self.tr("object supervisor"),
            self,
            objectName="processes-dock",
            allowedAreas=qt.Qt.BottomDockWidgetArea,
            visible=self.show_processes_manager_action.isChecked(),
        )

        self.process_supervisor_dock.setWidget(ProcessManagerWindow(parent=None))
        self.process_supervisor_dock.visibilityChanged[bool].connect(
            self.show_processes_manager_action.setChecked
        )
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.process_supervisor_dock)

    def setup_actions(self):
        super().setup_actions()
        # create the action to connect with it
        self.show_processes_manager_action = qt.QAction(
            self.tr("&object supervisor"),
            self,
            toolTip=self.tr("Show object states relative to processes."),
            checkable=True,
            triggered=lambda checked: self.process_supervisor_dock.setVisible(checked),
        )

    def setup_menu(self):
        super().setup_menu()
        self.view_menu.addAction(self.show_processes_manager_action)

        self.simple_example_action = qt.QAction(
            self.tr("simple use cases"),
            self,
            objectName="simple-use-cases",
            toolTip=self.tr("Some simple examples."),
            triggered=self.open_simple_examples,
            menuRole=qt.QAction.AboutRole,
        )

        self.dark_flat_example_action = qt.QAction(
            self.tr("darks and flats manipulations"),
            self,
            objectName="dark-flat-manipulation",
            toolTip=self.tr("Examples around dark and flat."),
            triggered=self.open_dark_flat_examples,
            menuRole=qt.QAction.AboutRole,
        )
        self.slurm_execution_example_action = qt.QAction(
            self.tr("remote processing with slurm"),
            self,
            objectName="execution-on-slurm",
            toolTip=self.tr("Examples of some execution over slurm."),
            triggered=self.open_slurm_execution_example,
            menuRole=qt.QAction.AboutRole,
        )
        self.cor_search_example_action = qt.QAction(
            self.tr("cor search advance example"),
            self,
            objectName="cor-search-example",
            toolTip=self.tr("Examples of ways to search for the Center of rotation."),
            triggered=self.open_cor_search_example,
            menuRole=qt.QAction.AboutRole,
        )
        self.python_script_example_action = qt.QAction(
            self.tr("python script examples"),
            self,
            objectName="python-script-example",
            toolTip=self.tr("Examples of some python script usage."),
            triggered=self.open_python_script_example,
            menuRole=qt.QAction.AboutRole,
        )
        # Predefined workflows menu.
        self.predefined_workflows_menu = qt.QMenu(
            self.tr("&Examples"),
            self.menuBar(),
            objectName="examples-menu",
        )
        self.predefined_workflows_menu.addActions(
            [
                self.simple_example_action,
                self.cor_search_example_action,
                self.dark_flat_example_action,
                self.slurm_execution_example_action,
                self.python_script_example_action,
            ]
        )

        self.menuBar().addMenu(self.predefined_workflows_menu)

        self._helpdeskButton = qt.QAction(
            self.tr("&Helpdesk"),
            self,
            objectName="helpdeskButton",
            triggered=self._contactUs,
            toolTip="contact esrf data processing helpdesk if you have some troubles with the application",
        )
        self.menuBar().addAction(self._helpdeskButton)

    def _contactUs(self, *args, **kwargs):
        try:
            qt.QDesktopServices.openUrl(qt.QUrl(self.HELPDESK_URL))
        except Exception as e:
            _logger.error(
                f"Failed to launch helpdesk web page ({self.HELPDESK_URL}). Error is {e}"
            )

    def __open_examples(self, examples, filter_names=None):
        """
        filter the existing tutorials by names contained in the file name
        """
        items = [previewmodel.PreviewItem(path=t.abspath()) for t in examples]

        def my_filter(value):
            for filter_name in filter_names:
                if filter_name in value:
                    return True
            return False

        if filter_names is not None:
            items = filter(
                lambda item: my_filter(os.path.basename(item.path())),
                items,
            )
        dialog = previewdialog.PreviewDialog(self)
        model = previewmodel.PreviewModel(dialog, items=items)
        title = self.tr("Example Workflows")
        dialog.setWindowTitle(title)
        template = '<h3 style="font-size: 26px">\n' "{0}\n" "</h3>"

        dialog.setHeading(template.format(title))
        dialog.setModel(model)

        model.delayedScanUpdate()
        status = dialog.exec()
        index = dialog.currentIndex()

        dialog.deleteLater()

        if status == qt.QDialog.Accepted:
            selected = model.item(index)
            self.open_example_scheme(selected.path())
        return status

    def open_about(self):
        dlg = AboutDialog(self)
        dlg.setAttribute(qt.Qt.WA_DeleteOnClose)
        dlg.exec()

    def open_simple_examples(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("simple", "EBS_tomo_listener")
        )

    def open_slurm_execution_example(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("slurm",)
        )

    def open_dark_flat_examples(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("darks",)
        )

    def open_python_script_example(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("_script",)
        )

    def open_cor_search_example(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("find_cor", "cor_search")
        )


log = logging.getLogger(__name__)


def check_for_updates() -> bool:
    return False


def send_usage_statistics() -> bool:
    return False


def pull_notifications() -> bool:
    return False


def make_sql_logger(level=logging.INFO):
    sql_log = logging.getLogger("sql_log")
    sql_log.setLevel(level)
    handler = RotatingFileHandler(
        os.path.join(config.log_dir(), "sql.log"), maxBytes=1e7, backupCount=2
    )
    sql_log.addHandler(handler)


class _OMain(ocMain):
    DefaultConfig = "tomwer.app.canvas_launcher.launcher.TomwerConfig"

    def run(self, argv):
        # Allow termination with CTRL + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        # Disable pyqtgraph's atexit and QApplication.aboutToQuit cleanup handlers.
        pyqtgraph.setConfigOption("exitCleanup", False)
        print("argv are", argv)
        super().run(argv)

    def argument_parser(self) -> argparse.ArgumentParser:
        parser = super().argument_parser()
        parser.add_argument(
            "--use-opengl-plot",
            help="Use OpenGL for plots (instead of matplotlib)",
            action="store_true",
            default=False,
        )
        return parser

    def parse_arguments(self, argv: List[str]):
        super().parse_arguments(argv)
        # define silx plot backend. For now the si;pler is to
        # define an environment variable.
        # this way we should also be able to let the user define it
        # on it's own later...
        if self.options.use_opengl_plot:
            import silx

            # other standalones are not passing by the silx.config
            # but for the canvas this is way simpler to use it.
            # then all plot which have backend==None will pick the default plot backend
            silx.config.DEFAULT_PLOT_BACKEND = "gl"

    def setup_logging(self):
        super().setup_logging()
        make_sql_logger(self.options.log_level)

    def setup_application(self):
        super().setup_application()
        # NOTE: No OWWidgetBase subclass should be imported before this

        self._update_check = check_for_updates()
        self._send_stat = send_usage_statistics()
        self._pull_notifs = pull_notifications()

        settings = qt.QSettings()
        settings.setValue(
            "startup/launch-count",
            settings.value("startup/launch-count", 0, int) + 1,
        )

        UsageStatistics.set_enabled(False)

    def show_splash_message(self, message: str, color=qt.QColor("#FFD39F")):
        super().show_splash_message(message, color)

    def create_main_window(self):
        window = MainWindow()
        return window

    def setup_sys_redirections(self):
        super().setup_sys_redirections()
        if isinstance(sys.excepthook, ExceptHook):
            sys.excepthook.handledException.connect(handle_exception)

    def tear_down_sys_redirections(self):
        if isinstance(sys.excepthook, ExceptHook):
            sys.excepthook.handledException.disconnect(handle_exception)
        super().tear_down_sys_redirections()

    def splash_screen(self):
        """Return the application splash screen"""
        settings = qt.QSettings()
        options = self.options
        want_splash = (
            settings.value("startup/show-splash-screen", True, type=bool)
            and not options.no_splash
        )

        if want_splash:
            pm, rect = self.config.splash_screen()
            splash_screen = TomwerSplashScreen(pixmap=pm, textRect=rect)
            splash_screen.setAttribute(qt.Qt.WA_DeleteOnClose)
            splash_screen.setFont(qt.QFont("Helvetica", 12))
            palette = splash_screen.palette()
            color = qt.QColor("#b3baba")
            palette.setColor(qt.QPalette.Text, color)
            splash_screen.setPalette(palette)
        else:
            splash_screen = None
        return splash_screen


def data_dir():
    return os.path.join(data_dir_base(), "tomwer", tomwer.version.version)


def widget_settings_dir():
    return os.path.join(data_dir(), "widgets")


ABOUT_TEMPLATE = """\
<h4>{name}</h4>
<p>tomwer version: {tomwer_version}</p>
<p>nabu version: {nabu_version}</p>
<p>nxtomomill version: {nxtomomill_version}</p>
<p>nxtomo version: {nxtomo_version}</p>
<p>tomoscan version: {tomoscan_version}</p>
<p>sluurp version: {sluurp_version}</p>
<p>ewoks version: {ewoks_version}</p>
"""


class AboutDialog(qt.QDialog):
    def __init__(self, parent=None, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        layout = qt.QVBoxLayout()
        label = qt.QLabel(self)

        pixmap, _ = TomwerConfig.splash_screen()
        pixmap = pixmap.scaled(150, 150)

        label.setPixmap(pixmap)

        layout.addWidget(label, qt.Qt.AlignCenter)

        text = ABOUT_TEMPLATE.format(
            name=escape("tomwer"),
            tomwer_version=escape(tomwer.version.version),
            nabu_version=escape(nabu.version if has_nabu else "not installed"),
            nxtomomill_version=escape(
                nxtomomill.version.version if has_nxtomomill else "not installed"
            ),
            nxtomo_version=escape(
                nxtomo.__version__ if has_nxotmo else "not installed"
            ),
            tomoscan_version=escape(tomoscan.version.version),
            sluurp_version=escape(
                sluurp.__version__ if has_sluurp else "not installed"
            ),
            ewoks_version=escape(
                ewoks.__version__ if hasattr(ewoks, "__version__") else "???"
            ),
        )
        text_label = qt.QLabel(text)
        layout.addWidget(text_label, qt.Qt.AlignCenter)

        buttons = qt.QDialogButtonBox(qt.QDialogButtonBox.Close, qt.Qt.Horizontal, self)
        layout.addWidget(buttons)
        buttons.rejected.connect(self.accept)
        layout.setSizeConstraint(qt.QVBoxLayout.SetFixedSize)
        self.setLayout(layout)


class OMain(_OMain):
    config: TomwerConfig
    DefaultConfig = "tomwer.app.canvas_launcher.config.TomwerConfig"

    def run(self, argv):
        log.info("Clearing widget settings")
        shutil.rmtree(widget_settings_dir(), ignore_errors=True)
        dealWithLogFile()
        super().run(argv)

    def setup_application(self):
        qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
        return super().setup_application()

    def setup_logging(self):
        super().setup_logging()
        rootlogger = logging.getLogger()
        rootlogger = TomwerLogger(rootlogger)
        logging.setLoggerClass(TomwerLogger)

    def setup_sys_redirections(self):
        self._tomwLogger = TomwerLogger("tomwer")
        try:
            self.output = doc = TerminalTextDocument()

            stdout = TextStream(objectName="-stdout")
            stderr = TextStream(objectName="-stderr")
            doc.connectStream(stdout)
            doc.connectStream(stderr, color=qt.Qt.red)

            if sys.stdout is not None:
                stdout.stream.connect(sys.stdout.write, qt.Qt.DirectConnection)

            self.__stdout__ = sys.stdout
            sys.stdout = stdout

            if sys.stderr is not None:
                stderr.stream.connect(sys.stderr.write, qt.Qt.DirectConnection)

            self.__stderr__ = sys.stderr
            sys.stderr = stderr
            self.__excepthook__ = sys.excepthook
            sys.excepthook = ExceptHook(stream=stderr)

            self.stack.push(closing(stdout))
            self.stack.push(closing(stderr))
        except Exception:
            super().setup_sys_redirections()

    def argument_parser(self) -> argparse.ArgumentParser:
        parser = super().argument_parser()
        for action in parser._actions:
            if action.dest == "clear_widget_settings":
                parser._remove_action(action)
                break

        parser.add_argument(
            "--no-color-stdout-logs",
            "--no-colored-logs",
            action="store_true",
            help="instead of having logs in the log view, color logs of the stdout",
            default=False,
        )
        return parser

    def create_main_window(self):
        window = MainWindow()
        return window


def dealWithLogFile():
    """Move log file history across log file hierarchy and create the new log file"""

    # move log file if exists
    for i in range(MAX_LOG_FILE):
        logFile = LOG_FILE_NAME
        if os.path.exists(LOG_FOLDER) and os.access(LOG_FOLDER, os.W_OK):
            logFile = os.path.join(LOG_FOLDER, logFile)
        defLogName = logFile

        iLog = MAX_LOG_FILE - i
        maxLogNameN1 = logFile + "." + str(iLog)
        if iLog - 1 == 0:
            maxLogNameN2 = defLogName
        else:
            maxLogNameN2 = logFile + "." + str(iLog - 1)
        if os.path.exists(maxLogNameN2):
            try:
                stat = os.stat(maxLogNameN2)
                shutil.copy(maxLogNameN2, maxLogNameN1)
                os.utime(maxLogNameN1, (stat.st_atime, stat.st_mtime))
            except Exception:
                pass
    # create a new log file
    if os.path.exists(LOG_FOLDER) and os.access(LOG_FOLDER, os.W_OK):
        logFile = os.path.join(LOG_FOLDER, logFile)
        logging.basicConfig(
            filename=logFile,
            filemode="w",
            level=logging.WARNING,
            format="%(asctime)s %(message)s",
        )


def check_is_latest_release() -> bool:
    """Check if the current version is the latest release."""
    url = "https://gitlab.esrf.fr/tomotools/tomwer/-/raw/master/tomwer/version.py"
    current_version = tomwer.version.version
    try:
        version_file_html = urlopen(url, data=None, timeout=10)
    except Exception as e:
        _logger.warning(f"Fail to load version of the latest release. Reason is {e}")
        return True
    else:
        latest_release_version = None
        for line in version_file_html.readlines():
            t_line = line.decode("utf-8")
            t_line = t_line.replace(" ", "")
            if t_line.startswith("latest_release_version_info="):
                latest_release_version = t_line.replace(
                    "latest_release_version_info=", ""
                )
                break
        if latest_release_version is None:
            _logger.warning("Unable to find the version of the latest " "release.")

        elif current_version < latest_release_version:
            msg = qt.QMessageBox()
            msg.setIcon(qt.QMessageBox.Question)
            types = qt.QMessageBox.Ok | qt.QMessageBox.Cancel
            message = (
                "The version you want to use ({}) is not the latest "
                "version ({}). Do you want to continue ?"
            )
            msg.setStandardButtons(types)
            msg.setWindowTitle("No the latest version")
            msg.setText(message)
            return msg.exec_() == qt.QMessageBox.Ok
        return True
