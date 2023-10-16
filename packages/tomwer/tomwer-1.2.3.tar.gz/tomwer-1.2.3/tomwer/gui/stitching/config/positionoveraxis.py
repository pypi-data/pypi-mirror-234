import functools
import numpy
from silx.gui import qt

from tomwer.gui.stitching.axisorderedlist import AxisOrderedTomoObjsModel


class PosEditorOverOneAxis(qt.QWidget):
    """keep it ordered along one axis"""

    DEFAULT_VALUE_WHEM_MISSING = 0

    def __init__(
        self, parent, axis_edited: int, axis_order=None, *args, **kwargs
    ) -> None:
        assert axis_edited in (0, 1, 2)
        super().__init__(parent, *args, **kwargs)
        self._stepSize = 1
        self._axisEdited = axis_edited
        # the axis the spin boxes are editing
        self._axisOrder = axis_order if axis_order is not None else axis_edited
        # the axis along which the tomo obj are ordered
        self._tomoObjtoSpinBoxes = {}
        # list of spin box to edit the position over the axis. Key is the tomo object, value is the spin box
        self.__spinBoxescallback = {}
        self.setLayout(qt.QVBoxLayout())
        # widget to define step size
        self._stepSizeWidget = StepSizeWidget(self)
        self.layout().addWidget(self._stepSizeWidget)

        # table with the different Tomo objects
        self._tomoObjsTableView = qt.QTableView(parent=self)
        model = EditableAxisOrderedTomoObjsModel(axis=self._axisOrder)
        self._tomoObjsTableView.setModel(model)

        self.layout().addWidget(self._tomoObjsTableView)

        # tune table view
        self._tomoObjsTableView.setColumnWidth(0, 15)
        self._tomoObjsTableView.setColumnWidth(2, 120)
        self._tomoObjsTableView.horizontalHeader().setSectionResizeMode(
            1, qt.QHeaderView.Stretch
        )

        # connect signal / slot
        self._stepSizeWidget.stepSB.valueChanged.connect(self.setStepSize)
        self._stepSize = 1

    def setStepSize(self, step_size: int):
        self._stepSize = step_size
        # update SB step size
        for sb in self._tomoObjtoSpinBoxes.values():
            sb.setSingleStep(self._stepSize)

    def addTomoObj(self, tomo_obj):
        if tomo_obj is None:
            return
        else:
            self._tomoObjsTableView.model().addTomoObj(tomo_obj)
            # register tomo obj metadata modification to make sure we keel the z ordered list up to data
            tomo_obj.stitching_metadata.sigChanged.connect(
                self._orderedMightHavechanged
            )
            self._createSpinBox(tomo_obj=tomo_obj)
            self._orderedMightHavechanged()

    def _createSpinBox(self, tomo_obj):
        spinBox = qt.QSpinBox(parent=self)
        spinBox.setRange(numpy.iinfo(numpy.int32).min, numpy.iinfo(numpy.int32).max)
        spinBox.setSuffix("px")
        spinBox.setSingleStep(self._stepSize)
        spinBox.setValue(
            tomo_obj.stitching_metadata.get_abs_position_px(axis=self._axisEdited)
            or self.DEFAULT_VALUE_WHEM_MISSING
        )
        identifier_as_str = tomo_obj.get_identifier().to_str()
        self._tomoObjtoSpinBoxes[identifier_as_str] = spinBox
        # connect signal / slot
        callback = functools.partial(
            self._spinBoxValueChanged, spin_box=spinBox, tomo_obj=tomo_obj
        )
        self.__spinBoxescallback[identifier_as_str] = callback
        spinBox.editingFinished.connect(callback)
        return spinBox

    def _deleteSpinBox(self, tomo_obj):
        identifier_as_str = tomo_obj.get_identifier().to_str()
        if identifier_as_str in self._tomoObjtoSpinBoxes:
            del self._tomoObjtoSpinBoxes[identifier_as_str]
            del self.__spinBoxescallback[identifier_as_str]

    def removeTomoObj(self, tomo_obj):
        self._deleteSpinBox(tomo_obj)
        self._tomoObjsTableView.model().removeTomoObj(tomo_obj)
        tomo_obj.stitching_metadata.sigChanged.disconnect(self._orderedMightHavechanged)

    def _spinBoxValueChanged(self, spin_box, tomo_obj, *args, **kwargs):
        tomo_obj.stitching_metadata.setPxPos(spin_box.value(), axis=self._axisEdited)

    def setTomoObjs(self, tomo_objs: tuple) -> None:
        """
        replace current list of object by the given list
        """
        self._tomoObjsTableView.model().clearTomoObjs()
        for tomo_obj in tomo_objs:
            self.addTomoObj(tomo_obj)

    def clean(self):
        tomo_objs = self._tomoObjsTableView.model().getTomoObjs()
        for tomo_obj in tomo_objs:
            self.removeTomoObj(tomo_obj=tomo_obj)

    def reorderAlongAxis(self):
        pass

    def setSerie(self):
        raise NotImplementedError

    def _orderedMightHavechanged(self, force_sb_update=False):
        # add index widget
        self._tomoObjsTableView.model().reorder_objs()
        self._tomoObjsTableView.model().layoutChanged.emit()

        ordered_objs = self._tomoObjsTableView.model()._axis_decreasing_ordered_objs

        # start update spin box positions
        # check if we need to update one widget. Has this is designed if we need to update one then we need to update them all...
        needs_to_update_widget = force_sb_update
        for i_pos, tomo_obj in enumerate(ordered_objs):
            identifier_as_str = tomo_obj.get_identifier().to_str()
            spinBox = self._tomoObjtoSpinBoxes[identifier_as_str]
            model_index = self._tomoObjsTableView.model().createIndex(i_pos, 2)
            needs_to_update_widget = (
                needs_to_update_widget
                or self._tomoObjsTableView.indexWidget(model_index)
                not in (None, spinBox)
            )

        for i_pos, tomo_obj in enumerate(ordered_objs):
            identifier_as_str = tomo_obj.get_identifier().to_str()
            spinBox = self._tomoObjtoSpinBoxes[identifier_as_str]
            model_index = self._tomoObjsTableView.model().createIndex(i_pos, 2)
            if needs_to_update_widget:
                # if items have been reordered then we must recreated SpinBoxes otherwise if we try
                # to change order then Qt will end up with a seg fault which seems to come from
                # otherwirtting the cell and trying to reuse them
                self._deleteSpinBox(tomo_obj=tomo_obj)
                spinBox = self._createSpinBox(tomo_obj=tomo_obj)
            self._tomoObjsTableView.setIndexWidget(model_index, spinBox)
        # end update spin box positions


class EditableAxisOrderedTomoObjsModel(AxisOrderedTomoObjsModel):
    def __init__(self, axis: int, parent=None) -> None:
        super().__init__(axis, parent)
        self._headers = ["index", "tomo obj", f"axis {axis} pos (px)"]


class StepSizeWidget(qt.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QFormLayout())
        self._stepSB = qt.QSpinBox(self)
        self._stepSB.setRange(1, 9999)
        self.layout().addRow("step size", self._stepSB)

    @property
    def stepSB(self):
        return self._stepSB
