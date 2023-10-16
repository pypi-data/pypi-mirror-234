import pytest

from tomwer.gui.qfolderdialog import QDataDialog
from tomwer.tests.conftest import qtapp  # noqa F401


@pytest.mark.parametrize("multi_selection", (True, False))
def test_qdata_dialog(
    qtapp,  # noqa F401
    multi_selection,
):
    dialog = QDataDialog(parent=None, multiSelection=multi_selection)
    dialog.files_selected()
