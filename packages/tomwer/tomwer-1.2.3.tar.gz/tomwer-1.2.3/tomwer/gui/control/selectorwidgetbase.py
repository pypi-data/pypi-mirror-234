import logging

from silx.gui import qt

from tomwer.gui.utils.qt_utils import block_signals

_logger = logging.getLogger(__name__)


class _SelectorWidget(qt.QWidget):
    """widget used to select a dataset on a list (a scan or a volume for now)"""

    sigSelectionChanged = qt.Signal(list)
    """Signal emitted when the selection changed. List elements are tomo object identifier as str"""

    sigUpdated = qt.Signal()
    """signal emitted when the scan list change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self.dataList = self._buildDataList()
        self.dataList.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        self.layout().addWidget(self.dataList)
        self.layout().addWidget(self._getAddAndRmButtons())
        self.layout().addWidget(self._getSendButtons())
        self.setAcceptDrops(True)

        # connect signal / slot
        # for drag / drop we need to have an indirect call to the sigUpdated
        self.dataList.listChanged.connect(self._updatedFromDragDrop)

    def _updatedFromDragDrop(self, *args, **kwargs):
        self.sigUpdated.emit()

    def add(self, scan):
        added_scans = self.dataList.add(scan)
        self.sigUpdated.emit()
        return added_scans

    def remove(self, scan):
        self.dataList.remove(scan)
        self.sigUpdated.emit()

    def n_data(self) -> int:
        return len(self.dataList.items)

    def _buildDataList(self):
        raise NotImplementedError("Base class")

    def _getAddAndRmButtons(self):
        lLayout = qt.QHBoxLayout()
        w = qt.QWidget(self)
        w.setLayout(lLayout)
        self._addButton = qt.QPushButton("Add")
        self._addButton.clicked.connect(self._callbackAddData)
        self._rmButton = qt.QPushButton("Remove")
        self._rmButton.clicked.connect(self._callbackRemoveSelectedDatasets)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        lLayout.addWidget(spacer)
        lLayout.addWidget(self._addButton)
        lLayout.addWidget(self._rmButton)

        return w

    def _getSendButtons(self):
        lLayout = qt.QHBoxLayout()
        widget = qt.QWidget(self)
        widget.setLayout(lLayout)

        # spacer
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        lLayout.addWidget(spacer)

        # send all button
        self._sendAllButton = qt.QPushButton("Send all")
        self._sendAllButton.clicked.connect(self._sendAll)
        lLayout.addWidget(self._sendAllButton)

        # send selected button
        self._sendButton = qt.QPushButton("Send selected")
        self._sendButton.clicked.connect(self._selectActiveData)
        lLayout.addWidget(self._sendButton)

        return widget

    def selectAll(self):
        self.dataList.selectAll()

    def setMySelection(self, selection: tuple):
        self.dataList.setMySelection(selection)

    def _callbackAddData(self):
        raise NotImplementedError("Base class")

    def _selectActiveData(self):
        sItem = self.dataList.selectedItems()
        if sItem and len(sItem) >= 1:
            selection = [_item.text() for _item in sItem]
            self.sigSelectionChanged.emit(list(selection))
        else:
            _logger.warning("No active scan detected")

    def _sendAll(self):
        allItems = list(self.dataList._myitems.keys())
        if len(allItems) > 0:
            self.sigSelectionChanged.emit(allItems)

    def _callbackRemoveSelectedDatasets(self):
        """ """
        selected_items = self.dataList.selectedItems()
        tomwer_objs_to_remove = [item.data(qt.Qt.UserRole) for item in selected_items]
        for tomwer_obj in tomwer_objs_to_remove:
            self.remove(tomwer_obj)
        self.sigUpdated.emit()

    def setActiveData(self, data):
        """
        set the given scan as the active one

        :param scan: the scan to set active
        :type scan: Union[str, TomoBase]
        """
        data_id = data
        self.dataList.setCurrentItem(self.dataList.items[data_id])

    def removeSelectedDatasets(self):
        sItem = self.dataList.selectedItems()
        selection = [_item.text() for _item in sItem]

        with block_signals(self):
            # make sure sigUpdated is called only once.
            for identifier in selection:
                self.remove(identifier)
        self.sigUpdated.emit()
