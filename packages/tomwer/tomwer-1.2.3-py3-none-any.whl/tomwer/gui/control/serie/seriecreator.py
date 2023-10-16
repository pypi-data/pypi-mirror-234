# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "12/01/2022"


import logging
from contextlib import AbstractContextManager
from typing import Iterable, Optional

from silx.gui import qt
from silx.gui.utils import blockSignals
from silx.utils.enum import Enum as _Enum
from tomoscan.serie import Serie

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.gui.control.datalist import TomoObjList
from tomwer.gui.qfolderdialog import QDataDialog
from tomwer.gui.visualization.tomoobjoverview import TomoObjOverview

_logger = logging.getLogger(__name__)


class SerieWidgetDialog(qt.QDialog):
    sigSerieSelected = qt.Signal(Serie)
    """
    emit when a serie is selected / triggered by the user
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setLayout(qt.QVBoxLayout())
        # add list
        self._widget = SerieWidget()
        self.layout().addWidget(self._widget)
        # add buttons
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._selectButton = qt.QPushButton("Select (active) serie", parent=self)
        self._buttons.addButton(self._selectButton, qt.QDialogButtonBox.ActionRole)
        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._selectButton.released.connect(self._serieSelected)

    def getSelectedSerie(self) -> Optional[Serie]:
        return self._widget.getSelectedSerie()

    def _serieSelected(self, *args, **kwargs):
        serie = self.getSelectedSerie()
        if serie is not None:
            self.sigSerieSelected.emit(serie)

    # expose API
    def add(self, tomo_obj):
        self._widget.add(tomo_obj=tomo_obj)


class SerieWidget(qt.QTabWidget):
    sigCurrentSerieChanged = qt.Signal()
    """signal emit when the current serie changes"""

    sigHistoryChanged = qt.Signal()
    """signal emit when the history changed (a serie has been added or removed"""

    sigSerieSend = qt.Signal(Serie)
    """Signal emited when a serie has been send"""

    _HISTORY_MODE = "history"
    _DEFINITION_MODE = "serie definition"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("serie of scans")
        self._serieDefinitionWidget = SerieDefinition(parent=self)
        self.addTab(self._serieDefinitionWidget, self._DEFINITION_MODE)
        self._historyWidget = SerieHistoryDialog(parent=self)
        self._historyWidget.setWindowFlags(qt.Qt.Widget)
        self.addTab(self._historyWidget, self._HISTORY_MODE)

        # conenct signal / slot
        self._historyWidget.sigEditSerie.connect(self._serieEditionRequested)
        self._historyWidget.sigSerieSend.connect(self._repeatSerieSend)
        self._historyWidget.sigHistoryUpdated.connect(self._repeatHistoryUpdated)
        self._serieDefinitionWidget.sigSerieChanged.connect(self._repeatSerieChanged)
        self._serieDefinitionWidget.sigSerieSend.connect(self._repeatSerieSend)
        self._serieDefinitionWidget.sigSerieSend.connect(self._historyWidget.addSerie)

    def getHistoryWidget(self):
        return self._historyWidget

    def getDefinitionWidget(self):
        return self._serieDefinitionWidget

    def getSelectedSerie(self) -> Optional[Serie]:
        return self._serieDefinitionWidget.getSelectedSerie()

    def setMode(self, mode: str, definition_mode: Optional[str] = None):
        valid_modes = (self._HISTORY_MODE, self._DEFINITION_MODE)
        if mode == self._HISTORY_MODE:
            self.setCurrentWidget(self._historyWidget)
        elif mode == self._DEFINITION_MODE:
            self.setCurrentWidget(self._serieDefinitionWidget)
            self._serieDefinitionWidget.setMode(definition_mode)
        else:
            raise ValueError(
                f"mode {mode} is no recognized. Valid modes are {valid_modes}"
            )

    def _serieEditionRequested(self, serie: Serie):
        if not isinstance(serie, Serie):
            raise TypeError(f"serie is expected to be a serie not {type(serie)}")
        self.setMode("serie definition", "manual")
        self.getDefinitionWidget().getManualDefinitionWidget().setSerie(serie)

    def _repeatSerieChanged(self, *args, **kwargs):
        self.sigCurrentSerieChanged.emit()

    def _repeatSerieSend(self, serie: Serie):
        self.sigSerieSend.emit(serie)

    def _repeatHistoryUpdated(self, *args, **kwargs):
        self.sigHistoryChanged.emit()

    def add(self, tomo_obj):
        return self._serieDefinitionWidget.addTomoObj(tomo_obj)


class _SerieDefinitionMode(_Enum):
    MANUAL = "manual"
    AUTO = "auto"


class SerieDefinition(qt.QWidget):
    sigSerieChanged = qt.Signal()
    ### signal emit when a the serie defined manually changed

    sigSerieSend = qt.Signal(Serie)
    ### signal emit when a serie is send

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QGridLayout())

        self._modeLabel = qt.QLabel("Mode", self)
        self.layout().addWidget(self._modeLabel, 0, 0, 1, 1)

        self._modeCB = qt.QComboBox(self)
        for mode in _SerieDefinitionMode.values():
            self._modeCB.addItem(mode)
        self.layout().addWidget(self._modeCB, 0, 1, 1, 1)

        self._manualDefWidget = SerieManualFromTomoObj(parent=self)
        self.layout().addWidget(self._manualDefWidget, 1, 0, 1, 2)
        self._manualDefWidget.setWindowFlags(qt.Qt.Widget)

        self._automaticDefWidget = SerieAutomaticDefinitionWidget(parent=self)
        self.layout().addWidget(self._automaticDefWidget, 2, 0, 1, 2)

        # connect signal / slot
        self._modeCB.currentIndexChanged.connect(self._updateVisibility)
        self._manualDefWidget._newSerieWidget.sigUpdated.connect(
            self._repeatSerieChanged
        )

        # set up
        self._updateVisibility()

    def getSelectedSerie(self) -> Optional[Serie]:
        if self.getMode() == _SerieDefinitionMode.MANUAL:
            return self._manualDefWidget.getSerie()
        else:
            raise ValueError(f"mode {self.getMode()} is not handled yet")

    def getMode(self) -> str:
        return _SerieDefinitionMode.from_value(self._modeCB.currentText())

    def setMode(self, mode: str):
        mode = _SerieDefinitionMode.from_value(mode)
        idx = self._modeCB.findText(mode.value)
        self._modeCB.setCurrentIndex(idx)

    def _updateVisibility(self):
        self._manualDefWidget.setVisible(self.getMode() == _SerieDefinitionMode.MANUAL)
        self._automaticDefWidget.setVisible(self.getMode() == _SerieDefinitionMode.AUTO)

    def getManualDefinitionWidget(self):
        return self._manualDefWidget

    def getAutoDefinitionWidget(self):
        return self._automaticDefWidget

    def _repeatSerieChanged(self, *args, **kwargs):
        self.sigSerieChanged.emit()

    def _repeatSerieSend(self, serie: Serie):
        self.sigSerieSend.emit(serie)

    def createManualSerie(self):
        self._manualDefWidget.createSerie()

    def addTomoObj(self, tomo_obj: TomwerObject):
        self._manualDefWidget.addTomoObj(tomo_obj=tomo_obj)

    def setSerieName(self, name: str):
        self._manualDefWidget.setSerieName(name=name)


class _SerieDefinitionTree(qt.QWidget):
    """
    Tree used to define manually serie of scan.
    Drag and drop of files is handled
    """

    sigUpdated = qt.Signal()
    """Signal emit when the serie is updated"""

    class SignalBlocker(AbstractContextManager):
        """Simple context manager to hide / show button dialogs"""

        def __init__(self, serie_definition_widget) -> None:
            super().__init__()
            self.serie_definition_widget = serie_definition_widget

        def __enter__(self):
            self.old_widget = self.serie_definition_widget.blockSignals(True)
            self.old_tree = self.serie_definition_widget._tree.blockSignals(True)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.serie_definition_widget.blockSignals(self.old_widget)
            self.serie_definition_widget._tree.blockSignals(self.old_tree)

    def __init__(self, parent=None, serie_name="my_serie") -> None:
        self._tomo_objs = {}
        # associated serie name (key) to tuple (serie, QTreeWidgetItem)
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self._tree = qt.QTreeWidget(self)
        self._tree.setSelectionMode(qt.QAbstractItemView.MultiSelection)
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(("serie", "scan ids"))
        self._tree.setItemsExpandable(False)
        self.layout().addWidget(self._tree)

        # set up the tree with the serie name that will stay during the entire
        # life time of the tree
        self._serieItem = qt.QTreeWidgetItem(self._tree)
        self._serieItem.setFlags(self._serieItem.flags() | qt.Qt.ItemIsEditable)
        self._serieItem.setExpanded(True)

        self.setAcceptDrops(True)

        # connect signal / slot
        self._tree.itemChanged.connect(self._updated)

        # set up
        self.setSerieName(name=serie_name)

        # expose API
        self.itemChanged = self._tree.itemChanged

    @property
    def rootItem(self):
        return self._serieItem

    def setSerieName(self, name: str):
        with self.SignalBlocker(self):
            self._serieItem.setText(0, name)
        self.sigUpdated.emit()

    def getSerieName(self):
        return self._serieItem.text(0)

    def addTomoObj(self, tomo_obj: TomwerObject):
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"{tomo_obj} is expected to be an instance of {TomwerObject} not {type(tomo_obj)}"
            )
        identifier = tomo_obj.get_identifier().to_str()
        if identifier in self._tomo_objs:
            _logger.warning(f"scan {identifier} already part of the serie")
            return

        with self.SignalBlocker(self):
            tomo_obj_item = qt.QTreeWidgetItem(self.rootItem)
            tomo_obj_item.setText(1, identifier)
            tomo_obj_item.setFlags(tomo_obj_item.flags() | qt.Qt.ItemIsUserCheckable)
            self._tomo_objs[identifier] = (tomo_obj, tomo_obj_item)
        self.sigUpdated.emit()

    def removeTomoObj(self, tomo_obj: TomwerObject):
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"{tomo_obj} is expected to be an instance of {TomwerObject} not {type(tomo_obj)}"
            )

        with self.SignalBlocker(self):
            identifier = tomo_obj.get_identifier().to_str()
            if identifier not in self._tomo_objs:
                _logger.warning(f"{identifier} is not in the serie")
            else:
                _, tomo_obj_item = self._tomo_objs.pop(identifier)
                root = self._tree.invisibleRootItem()
                root.removeChild(tomo_obj_item)
        self.sigUpdated.emit()

    @property
    def n_tomo_objs(self):
        return len(self._tomo_objs)

    def setSerie(self, serie: Serie) -> None:
        if not isinstance(serie, Serie):
            raise TypeError(
                f"serie is expected to be an instance of {Serie} not {type(serie)}"
            )

        with self.SignalBlocker(self):
            self.clearTomoObjs()
            self.setSerieName(serie.name)
            for tomo_obj in serie:
                if isinstance(tomo_obj, str):
                    try:
                        tomo_obj = ScanFactory.create_tomo_object_from_identifier(
                            identifier=tomo_obj
                        )
                    except Exception:
                        try:
                            tomo_obj = VolumeFactory.create_tomo_object_from_identifier(
                                identifier=tomo_obj
                            )
                        except Exception:
                            _logger.warning(f"Fail to recreate scan from {tomo_obj}.")
                            return
                elif not isinstance(tomo_obj, TomwerObject):
                    raise TypeError(
                        f"tomo_obj is expected to be an instance of {TomwerObject}. Not {type(tomo_obj)}"
                    )
                self.addTomoObj(tomo_obj)
        self.sigUpdated.emit()

    def getSerie(self, use_identifiers=False) -> Serie:
        scans = [scan for scan, _ in self._tomo_objs.values()]
        return Serie(
            name=self.getSerieName(),
            iterable=scans,
            use_identifiers=use_identifiers,
        )

    def clearTomoObjs(self):
        with self.SignalBlocker(self):
            keys = list(self._tomo_objs.keys())
            for key in keys:
                _, scan_item = self._tomo_objs.pop(key)
                root = self._tree.invisibleRootItem()
                root.removeChild(scan_item)
        self.sigUpdated.emit()

    def setSelectedTomoObjs(self, objs):
        self.clearSelection()
        for scan in objs:
            scan_item = self._getTomoObjItem(scan)
            if scan_item is not None:
                scan_item.setSelected(True)

    def _getTomoObjItem(self, tomo_obj: TomwerObject) -> Optional[qt.QTreeWidgetItem]:
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"scan is expected to be an instance of {TomwerObject} not {type(tomo_obj)}"
            )
        return self._tomo_objs.get(tomo_obj.get_identifier().to_str(), (None, None))[1]

    def getSelectedTomoObjs(self) -> tuple():
        """return selected scans"""
        selected = []
        for _, (scan, item) in self._tomo_objs.items():
            if item.isSelected():
                selected.append(scan)
        return tuple(selected)

    def removeSelectedTomoObjs(self) -> None:
        with self.SignalBlocker(self):
            for tomo_obj in self.getSelectedTomoObjs():
                self.removeTomoObj(tomo_obj)

    def _updated(self, *args, **kwargs):
        self.sigUpdated.emit()

    def clearSelection(self) -> None:
        self._tree.selectionModel().clearSelection()

    def addScanFromNxFile(self, file_: str, entry: Optional[str] = None):
        try:
            if entry is None:
                scans = ScanFactory.create_scan_objects(scan_path=file_)
            else:
                scans = [ScanFactory.create_scan_object(scan_path=file_, entry=entry)]
        except Exception as e:
            _logger.error(f"cannot create scan instances from {file_}. Error is {e}")
        else:
            changed = False
            with self.SignalBlocker(self):
                for scan in scans:
                    if scan is not None:
                        try:
                            self.addTomoObj(tomo_obj=scan)
                        except TypeError:
                            _logger.error(
                                f"fail to add scan {scan}. Invalid type encountered ({type(scan)})"
                            )
                        else:
                            changed = True
            if changed:
                self.sigUpdated.emit()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            for url in event.mimeData().urls():
                self.addScanFromNxFile(file_=str(url.path()), entry=None)

    def supportedDropActions(self):
        """Inherited method to redefine supported drop actions."""
        return qt.Qt.CopyAction | qt.Qt.MoveAction

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.accept()
            event.setDropAction(qt.Qt.CopyAction)
        else:
            qt.QListWidget.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.setDropAction(qt.Qt.CopyAction)
            event.accept()
        else:
            qt.QListWidget.dragMoveEvent(self, event)


class SerieManualControlDialog(qt.QDialog):
    """
    Same as the :class:`SerieManualDefinitionDialog` but with control of the serie.
    This include a `create serie` and a `create serie and clear button`
    """

    sigSerieSend = qt.Signal(Serie)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self._mainWidget = SerieManualDefinitionDialog(parent=self)
        self._mainWidget.setWindowFlags(qt.Qt.Widget)
        self.layout().addWidget(self._mainWidget)

        self._buttons = qt.QDialogButtonBox(parent=self)
        self._createButton = qt.QPushButton("create serie", parent=self)
        self._buttons.addButton(self._createButton, qt.QDialogButtonBox.ActionRole)

        # connect signal / slot
        self._createButton.clicked.connect(self._sendSerie)
        self.layout().addWidget(self._buttons)

        # expose API
        self.sigUpdated = self._mainWidget.sigUpdated

    def _sendSerie(self):
        self.sigSerieSend.emit(self._mainWidget.getSerie())

    @property
    def n_tomo_objs(self):
        return self._mainWidget.n_tomo_objs

    def setSerieName(self, name: str):
        self._mainWidget.setSerieName(name=name)

    def getSerieName(self) -> str:
        return self._mainWidget.getSerieName()

    def setSerie(self, serie: Serie) -> None:
        self._mainWidget.setSerie(serie)

    def getSerie(self, *args, **kwargs) -> Serie:
        return self._mainWidget.getSerie(*args, **kwargs)

    def addScanFromNxFile(self, file_: str, entry: Optional[str] = None):
        return self._mainWidget.addScanFromNxFile(file_=file_, entry=entry)

    def removeSelectedScans(self) -> None:
        return self._mainWidget.removeSelectedTomoObjs()

    def getSelectedScans(self) -> tuple:
        return self._mainWidget.getSelectedTomoObjs()

    def setSelectedScans(self, scans: Iterable) -> None:
        self._mainWidget.setSelectedTomoObjs(scans=scans)

    def addScan(self, scan: TomwerScanBase) -> None:
        self._mainWidget.addTomoObj(scan=scan)

    def removeScan(self, scan: TomwerScanBase) -> None:
        self._mainWidget.removeTomoObj(scan=scan)

    def clearSerie(self) -> None:
        self._mainWidget.clearSerie()

    def createSerie(self):
        self.sigSerieSend.emit(self.getSerie())


class SerieManualFromTomoObj(qt.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        style = qt.QApplication.style()
        self.setLayout(qt.QGridLayout())

        # tomo objs list
        self._tomoObjList = TomoObjList(self)
        self._tomoObjList.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding
        )
        self._tomoObjListScrollArea = qt.QScrollArea(self)
        self._tomoObjListScrollArea.setWidgetResizable(True)
        self._tomoObjListScrollArea.setWidget(self._tomoObjList)
        self.layout().addWidget(self._tomoObjListScrollArea, 0, 0, 4, 2)

        # right arrow
        self._rightArrowButton = qt.QPushButton(self)
        rightArrowIcon = style.standardIcon(qt.QStyle.SP_ArrowRight)
        self._rightArrowButton.setIcon(rightArrowIcon)
        self._rightArrowButton.setFixedWidth(30)
        self.layout().addWidget(self._rightArrowButton, 1, 2, 1, 1)

        # left arrow
        self._leftArrowButton = qt.QPushButton(self)
        leftArrowIcon = style.standardIcon(qt.QStyle.SP_ArrowLeft)
        self._leftArrowButton.setIcon(leftArrowIcon)
        self._leftArrowButton.setFixedWidth(30)
        self.layout().addWidget(self._leftArrowButton, 2, 2, 1, 1)

        # new serie
        self._newSerieWidget = NewSerieWidget(self)
        self._newSerieWidgetScrollArea = qt.QScrollArea(self)
        self._newSerieWidgetScrollArea.setWidgetResizable(True)
        self._newSerieWidgetScrollArea.setWidget(self._newSerieWidget)
        self.layout().addWidget(self._newSerieWidgetScrollArea, 0, 3, 4, 2)

        # tomo obj details
        self._tomoObjInfos = TomoObjOverview(self)
        self._tomoObjInfos.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._tomoObjInfos, 4, 0, 2, 2)

        # connect signals / slot
        self._leftArrowButton.released.connect(self._removeSelectedObjs)
        self._rightArrowButton.released.connect(self._addSelectedObjs)
        self._tomoObjList.selectionModel().selectionChanged.connect(
            self._updateTomoObjInfos
        )

    def selectedTomoObjects(self) -> tuple:
        """
        :return: tuple of tomo object selected on the list
        :rtype: tuple
        """
        items = self._tomoObjList.selectedItems()
        return [item.data(qt.Qt.UserRole) for item in items]

    def _removeSelectedObjs(self, *args, **kwargs):
        for tomo_obj in self.selectedTomoObjects():
            self._newSerieWidget.removeTomoObjToCurrentSerie(tomo_obj)

    def _addSelectedObjs(self, *args, **kwargs):
        for tomo_obj in self.selectedTomoObjects():
            self._newSerieWidget.addTomoObjToCurrentSerie(tomo_obj)

    def _updateTomoObjInfos(self, *args, **kwargs):
        # should
        select_objs = self._tomoObjList.selectedItems()
        if select_objs and len(select_objs) > 0:
            tomo_obj = select_objs[0].data(qt.Qt.UserRole)
            self._tomoObjInfos.setTomoObj(tomo_obj)
        else:
            self._tomoObjInfos.setTomoObj(None)

    # expose API
    def setSerie(self, serie: Serie):
        self._newSerieWidget.setSerie(serie=serie)

    def getSerie(self, *args, **kwargs) -> Serie:
        return self._newSerieWidget.getSerie(*args, **kwargs)

    def addTomoObj(self, tomo_obj):
        self._tomoObjList.add(tomo_obj)

    def addToCurrentSerie(self, tomo_obj):
        self._newSerieWidget.addTomoObjToCurrentSerie(tomo_obj)

    def setSerieName(self, name: str):
        self._newSerieWidget.setSerieName(name=name)


class NewSerieWidget(qt.QWidget):
    sigNameChanged = qt.Signal()
    """Emit when serie name changed"""

    sigUpdated = qt.Signal()
    """
    Emit when the serie has been updated by the tree
    """

    DEFAULT_SERIE_NAME = "my_serie"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self._nameWidget = qt.QWidget(self)
        self._nameWidget.setLayout(qt.QHBoxLayout())
        self._nameWidget.layout().addWidget(qt.QLabel("serie name", self))
        self._nameQLE = qt.QLineEdit(self.DEFAULT_SERIE_NAME, self)
        self._nameWidget.layout().addWidget(self._nameQLE)
        self.layout().addWidget(self._nameWidget)

        self._serieTree = _SerieDefinitionTree(self, serie_name=self.DEFAULT_SERIE_NAME)
        self.layout().addWidget(self._serieTree)

        # Signal / slot connection
        self._serieTree.itemChanged.connect(self._handleItemUpdate)
        self._serieTree.sigUpdated.connect(self._repeatUpdateSignal)
        self._nameQLE.textChanged.connect(self._nameChangedOnQLE)

    def setSerie(self, serie: Serie) -> None:
        with blockSignals(self._nameQLE):
            self._nameQLE.setText(serie.name)
        self._serieTree.setSerie(serie=serie)

    def getSerie(self, *args, **kwargs) -> Serie:
        return self._serieTree.getSerie(*args, **kwargs)

    def _nameChangedOnQLE(self, name):
        with blockSignals(self._serieTree):
            self._serieTree.setSerieName(name)
        self.sigNameChanged.emit()

    def _handleItemUpdate(self, item, column):
        if item == self._serieTree.rootItem:
            old = self.blockSignals(True)
            self._nameQLE.setText(self._serieTree.rootItem.text(0))
            self.blockSignals(old)
        self.sigUpdated.emit()

    def _repeatUpdateSignal(self):
        self.sigUpdated.emit()

    def addTomoObjToCurrentSerie(self, tomo_obj: TomwerObject):
        assert isinstance(
            tomo_obj, TomwerObject
        ), f"invalid type {type(tomo_obj)}. {TomwerObject} expected"
        self._serieTree.addTomoObj(tomo_obj)

    def removeTomoObjToCurrentSerie(self, tomo_obj: TomwerObject):
        assert isinstance(
            tomo_obj, TomwerObject
        ), f"invalid type {type(tomo_obj)}. {TomwerObject} expected"
        self._serieTree.removeTomoObj(tomo_obj)

    def getSerieName(self) -> str:
        return self._serieTree.getSerieName()

    def setSerieName(self, name: str):
        self._serieTree.setSerieName(name=name)


class SerieManualDefinitionDialog(qt.QDialog):
    """Dialog to define a serie manually"""

    sigUpdated = qt.Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self._newSerieWidget = NewSerieWidget(self)

        self._buttons = qt.QDialogButtonBox(parent=self)

        self._addScanButton = qt.QPushButton("Add scan to the serie", parent=self)
        self._buttons.addButton(self._addScanButton, qt.QDialogButtonBox.ActionRole)

        self._removeSelectedButton = qt.QPushButton(
            "Remove selected scans", parent=self
        )
        self._buttons.addButton(
            self._removeSelectedButton, qt.QDialogButtonBox.ActionRole
        )

        self._clearButton = qt.QPushButton("Clear", parent=self)
        self._buttons.addButton(self._clearButton, qt.QDialogButtonBox.ActionRole)

        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._newSerieWidget.sigNameChanged.connect(self._nameChanged)
        self._newSerieWidget.sigUpdated.connect(self._repeatUpdateSignal)
        self._addScanButton.clicked.connect(self.addScanFromFileDialog)
        self._removeSelectedButton.clicked.connect(self.removeSelectedTomoObjs)
        self._clearButton.clicked.connect(self.clearSerie)

    @property
    def n_tomo_objs(self):
        serieTree = self._newSerieWidget._serieTree
        return serieTree.n_tomo_objs

    def _nameChanged(self, new_name):
        serieTree = self._newSerieWidget._serieTree
        with blockSignals(self._serieTree):
            serieTree.setSerieName(name=new_name)
        self.sigUpdated.emit()

    def _repeatUpdateSignal(self):
        self.sigUpdated.emit()

    def setSerieName(self, name: str):
        self._newSerieWidget.setSerieName(name=name)

    def getSerieName(self) -> str:
        return self._newSerieWidget.getSerieName()

    def setSerie(self, serie: Serie) -> None:
        self._newSerieWidget.setSerie(serie)

    def getSerie(self, *args, **kwargs) -> Serie:
        return self._newSerieWidget.getSerie(*args, **kwargs)

    def addScanFromFileDialog(self) -> None:
        dialog = QDataDialog(self, multiSelection=True)

        if not dialog.exec_():
            dialog.close()
            return

        foldersSelected = dialog.files_selected()
        for folder in foldersSelected:
            self.addScanFromNxFile(file_=folder, entry=None)

    def addScanFromNxFile(self, file_: str, entry: Optional[str] = None):
        serieTree = self._newSerieWidget._serieTree
        return serieTree.addScanFromNxFile(file_=file_, entry=entry)

    def removeSelectedTomoObjs(self) -> None:
        serieTree = self._newSerieWidget._serieTree
        return serieTree.removeSelectedTomoObjs()

    def getSelectedTomoObjs(self) -> tuple:
        serieTree = self._newSerieWidget._serieTree
        return serieTree.getSelectedTomoObjs()

    def setSelectedTomoObjs(self, scans: Iterable) -> None:
        serieTree = self._newSerieWidget._serieTree
        serieTree.setSelectedTomoObjs(objs=scans)

    def addTomoObj(self, scan: TomwerScanBase) -> None:
        serieTree = self._newSerieWidget._serieTree
        return serieTree.addTomoObj(tomo_obj=scan)

    def removeTomoObj(self, scan: TomwerScanBase) -> None:
        serieTree = self._newSerieWidget._serieTree
        serieTree.removeTomoObj(tomo_obj=scan)

    def clearSerie(self) -> None:
        serieTree = self._newSerieWidget._serieTree
        serieTree.clearTomoObjs()


class SerieAutomaticDefinitionWidget(qt.QWidget):
    pass


class SerieTree(qt.QWidget):
    """
    Widget used to define a scan serie from a list of scans.
    """

    def __init__(self, parent=None, scans=tuple()) -> None:
        self._series = {}
        # associated serie name (key) to tuple (serie, QTreeWidgetItem)
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self._tree = qt.QTreeWidget(self)
        self._tree.setSelectionMode(qt.QAbstractItemView.MultiSelection)
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(("serie", "scan ids"))
        self.layout().addWidget(self._tree)

        # set up
        [self.addSerie(scan) for scan in scans]

    def addSerie(self, serie: Serie):
        if not isinstance(serie, Serie):
            raise TypeError(
                f"{serie} is expected to be an instance of {Serie} not {type(serie)}"
            )
        if serie.name in self._series:
            self.removeSerie(self._series[serie.name][0])

        root_item = qt.QTreeWidgetItem(self._tree)
        root_item.setText(0, serie.name)
        self._series[serie.name] = (serie, root_item)
        for obj in serie:
            scan_item = qt.QTreeWidgetItem(root_item)
            if isinstance(obj, TomwerObject):
                text = obj.get_identifier().to_str()
            else:
                text = obj
            scan_item.setText(1, text)
            scan_item.setFlags(qt.Qt.NoItemFlags)

    def removeSerie(self, serie: Serie):
        if not isinstance(serie, Serie):
            raise TypeError(
                f"{serie} is expected to be an instance of {Serie} not {type(serie)}"
            )
        if serie.name in self._series:
            _, serie_item = self._series.pop(serie.name)
            root = self._tree.invisibleRootItem()
            root.removeChild(serie_item)

    @property
    def n_series(self):
        return len(self._series)

    def series(self) -> tuple:
        series = []
        [series.append(serie) for serie, _ in self._series.values()]
        return tuple(series)

    def clearSelection(self):
        self._tree.selectionModel().clearSelection()

    def setSelectedSeries(self, series):
        self.clearSelection()
        for serie in series:
            serie_item = self._getSerieItem(serie)
            if serie_item is not None:
                serie_item.setSelected(True)

    def _getSerieItem(self, serie: Serie) -> Optional[qt.QTreeWidgetItem]:
        if not isinstance(serie, Serie):
            raise TypeError(
                f"serie is expected to be an instance of {Serie} not {type(serie)}"
            )
        return self._series.get(serie.name, (None, None))[1]

    def getSelectedSeries(self) -> tuple():
        """return selected series"""
        selected = []
        for _, (serie, item) in self._series.items():
            if item.isSelected():
                selected.append(serie)
        return tuple(selected)

    def removeSelected(self) -> None:
        for serie in self.getSelectedSeries():
            self.removeSerie(serie)


class SerieHistoryDialog(qt.QDialog):
    sigSerieSend = qt.Signal(Serie)
    """signal emit when a serie has been selected by the user"""

    sigEditSerie = qt.Signal(Serie)
    """Signal emit when user request to edit a serie"""

    sigHistoryUpdated = qt.Signal()
    """Signal emit when the history has been modified"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self._serieList = SerieTree(self)
        self.layout().addWidget(self._serieList)

        self._buttons = qt.QDialogButtonBox(parent=self)

        self._editButton = qt.QPushButton("Edit", parent=self)
        self._buttons.addButton(self._editButton, qt.QDialogButtonBox.ActionRole)

        self._sendButton = qt.QPushButton("Resend", parent=self)
        self._buttons.addButton(self._sendButton, qt.QDialogButtonBox.ActionRole)

        self._removeButton = qt.QPushButton("Remove", parent=self)
        self._buttons.addButton(self._removeButton, qt.QDialogButtonBox.ActionRole)

        self._clearButton = qt.QPushButton("Clear", parent=self)
        self._buttons.addButton(self._clearButton, qt.QDialogButtonBox.ActionRole)

        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._sendButton.clicked.connect(self.sendSelected)
        self._removeButton.clicked.connect(self.removeSelected)
        self._clearButton.clicked.connect(self.clearSelection)
        self._editButton.clicked.connect(self.editSelected)

    def addSerie(self, serie: Serie):
        old = self.blockSignals(True)
        self._serieList.addSerie(serie)
        self.blockSignals(old)
        self.sigHistoryUpdated.emit()

    def removeSerie(self, serie: Serie):
        old = self.blockSignals(True)
        self._serieList.removeSerie(serie)
        self.blockSignals(old)
        self.sigHistoryUpdated.emit()

    def getSelectedSeries(self):
        return self._serieList.getSelectedSeries()

    def setSelectedSeries(self, series):
        old = self.blockSignals(True)
        self._serieList.setSelectedSeries(series)
        self.blockSignals(old)
        self.sigHistoryUpdated.emit()

    def sendSelected(self):
        for serie in self.getSelectedSeries():
            self.sigSerieSend.emit(serie)

    def editSelected(self):
        selected = self.getSelectedSeries()
        if len(selected) == 0:
            return
        if len(selected) > 1:
            _logger.warning(
                "more than one serie selected for edition. Will only edit the first one"
            )
        self.sigEditSerie.emit(selected[0])

    def removeSelected(self):
        old = self.blockSignals(True)
        self._serieList.removeSelected()
        self.blockSignals(old)
        self.sigHistoryUpdated.emit()

    def clearSelection(self):
        self._serieList.clearSelection()

    def series(self) -> tuple:
        return self._serieList.series()
