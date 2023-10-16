from typing import Optional
from silx.gui import qt
from tomwer.gui import icons as tomwericons
from tomwer.core.utils import concatenate_dict


class EmailComposition(qt.QWidget):
    """
    Widget used to compose an email

    Please see https://confluence.esrf.fr/display/SCKB/Rules+about+email for email rules at esrf
    """

    sigChanged = qt.Signal()
    """emit when the composition changed"""

    def __init__(self, parent: Optional[qt.QWidget]) -> None:
        super().__init__(parent)
        self.setLayout(qt.QFormLayout())
        # from
        self._fromAddressesQLE = qt.QLineEdit(self)
        singleEmailValidator = qt.QRegularExpressionValidator(
            qt.QRegularExpression(
                r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            ),
            self._fromAddressesQLE,
        )
        self._fromAddressesQLE.setValidator(singleEmailValidator)
        self.layout().addRow("from", self._fromAddressesQLE)
        # to
        self._toAdressesQLE = qt.QLineEdit(self)
        severalEmailValidator = qt.QRegularExpressionValidator(
            qt.QRegularExpression(
                r"(([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)(\s*;\s*|\s*$))*"
            ),
            self,
        )
        self._toAdressesQLE.setValidator(severalEmailValidator)
        self.layout().addRow("to", self._toAdressesQLE)
        # subject
        self._subjectQLE = qt.QLineEdit("tomwer: {tomo_obj_short_id} received", self)
        tooltip = """
        this section can contain some predefine `keywords` and will be formatting before sending the email.\n
        Reserve keywords are: \n
        - {tomo_obj_short_id}: tomo_obj short identifier
        - {tomo_obj_id}: tomo_obj id
        - {ls_tomo_obj}: ls of the scan folder
        - {timestamp}: current time
        - {footnote}: some footnote defined by tomwer
        - {dataset_processing_states}: list dataset state regarding met processes
        """
        self._subjectQLE.setToolTip(tooltip)
        self.layout().addRow("subject", self._subjectQLE)
        # text
        self._textQLE = qt.QPlainTextEdit(
            "{tomo_obj_id} received at {timestamp} \n\nprocesses:\n{dataset_processing_states}\n\nfile listening:\n{ls_tomo_obj}\n\nInfo: {footnote}"
        )
        self._textQLE.setToolTip(tooltip)
        self.layout().addRow(self._textQLE)

        # connect signal / slot
        self._fromAddressesQLE.editingFinished.connect(self._changed)
        self._toAdressesQLE.editingFinished.connect(self._changed)
        self._subjectQLE.editingFinished.connect(self._changed)
        self._textQLE.textChanged.connect(self._changed)

    def _changed(self):
        self.sigChanged.emit()

    def getToAddrs(self) -> tuple:
        adresses = self._toAdressesQLE.text().replace(" ", "")
        adresses.replace(",", ";")
        return tuple(set(adresses.split(";")))

    def getConfiguration(self) -> dict:
        return {
            "subject": self._subjectQLE.text(),
            "from_addr": self._fromAddressesQLE.text(),
            "to_addrs": self.getToAddrs(),
            "text": self._textQLE.toPlainText(),
        }

    def setConfiguration(self, config: dict):
        assert isinstance(config, dict)
        subject = config.get("subject", None)
        if subject is not None:
            self._subjectQLE.setText(str(subject))
        from_addr = config.get("from_addr", None)
        if from_addr is not None:
            self._fromAddressesQLE.setText(str(from_addr))
        to_addrs = config.get("to_addrs", None)
        if to_addrs is not None:
            if not isinstance(to_addrs, str):
                to_addrs = ";".join(to_addrs)
            self._toAdressesQLE.setText(str(to_addrs))
        text = config.get("text", None)
        if text is not None:
            self._textQLE.setPlainText(str(text))


class EmailSettings(qt.QWidget):
    """
    Widget to set up mail server
    """

    sigChanged = qt.Signal()
    """emit when the settings changed"""

    def __init__(self, parent: Optional[qt.QWidget]) -> None:
        super().__init__(parent)
        self.setLayout(qt.QFormLayout(self))
        # server
        self._hostQLE = qt.QLineEdit("smtps.esrf.fr", self)
        self.layout().addRow("host", self._hostQLE)
        # port
        self._portQLE = qt.QLineEdit("0", self)
        self._portQLE.setValidator(qt.QIntValidator(self._portQLE))
        self.layout().addRow("port", self._portQLE)

        # connect signal / slot
        self._hostQLE.editingFinished.connect(self._changed)
        self._portQLE.editingFinished.connect(self._changed)

    def _changed(self):
        self.sigChanged.emit()

    def getConfiguration(self) -> dict:
        return {"host": self._hostQLE.text(), "port": int(self._portQLE.text())}

    def setConfiguration(self, config: dict):
        server = config.get("host", None)
        if server is not None:
            self._hostQLE.setText(str(server))
        port = config.get("port", None)
        if port is not None:
            self._portQLE.setText(str(port))


class Emailwidget(qt.QTabWidget):
    """
    Main widget to send email
    """

    sigChanged = qt.Signal()
    """emit when the email settings or composition changed"""

    def __init__(self, parent: Optional[qt.QWidget] = None) -> None:
        super().__init__(parent)

        self.setTabPosition(qt.QTabWidget.East)

        self._compositionWidget = EmailComposition(self)
        composeIcon = tomwericons.getQIcon("compose")
        self.addTab(
            self._compositionWidget,
            composeIcon,
            "",
        )

        self._serverSettingsWidget = EmailSettings(self)
        settingsIcon = tomwericons.getQIcon("parameters")
        self.addTab(
            self._serverSettingsWidget,
            settingsIcon,
            "",
        )

        # connect signal / slot
        self._compositionWidget.sigChanged.connect(self._changed)
        self._serverSettingsWidget.sigChanged.connect(self._changed)

    def _changed(self):
        self.sigChanged.emit()

    def getConfiguration(self) -> dict:
        return concatenate_dict(
            self._serverSettingsWidget.getConfiguration(),
            self._compositionWidget.getConfiguration(),
        )

    def setConfiguration(self, config: dict):
        self._serverSettingsWidget.setConfiguration(config)
        self._compositionWidget.setConfiguration(config)
