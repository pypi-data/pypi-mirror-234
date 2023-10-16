from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.control.email import Emailwidget


def test_Emailwidget(qtapp):  # noqa F811
    """test of Emailwidget"""
    widget = Emailwidget()
    widget.show()

    assert widget.getConfiguration() == {
        "from_addr": "",
        "to_addrs": ("",),
        "subject": "tomwer: {tomo_obj_short_id} received",
        "text": "{tomo_obj_id} received at {timestamp} \n\nprocesses:\n{dataset_processing_states}\n\nfile listening:\n{ls_tomo_obj}\n\nInfo: {footnote}",
        "port": 0,
        "host": "smtps.esrf.fr",
    }

    new_configuration = {
        "from_addr": "toto.esrf.fr",
        "to_addrs": "toto.esrf.fr;tata.esrf.fr",
        "subject": "this is a scan",
        "text": "",
        "port": 445,
        "host": "smtps.esrf.en",
    }
    widget.setConfiguration(new_configuration)

    configuration = widget.getConfiguration()
    new_configuration.pop("to_addrs")
    assert configuration.pop("to_addrs") in (
        ("toto.esrf.fr", "tata.esrf.fr"),
        ("tata.esrf.fr", "toto.esrf.fr"),
    )
    assert configuration == new_configuration
