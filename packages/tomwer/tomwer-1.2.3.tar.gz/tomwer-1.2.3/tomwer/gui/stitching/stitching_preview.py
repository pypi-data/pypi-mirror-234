import logging
from typing import Union

import numpy
from nabu.stitching.frame_composition import ZFrameComposition
from silx.gui import qt
from tomoscan.esrf.scan.utils import get_data
from tomoscan.identifier import BaseIdentifier
from tomoscan.scanbase import TomoScanBase

from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.gui import icons as tomwer_icons
from tomwer.gui import settings
from tomwer.gui.stitching.stitchandbackground import StitchAndBackgroundAlphaMixIn

try:
    from silx.gui.plot.ImageStack import (  # noqa F401
        PlotWithWaitingLabel as _PlotWithWaitingLabel,
    )
except ImportError:
    from silx.gui.plot.ImageStack import _PlotWithWaitingLabel  # noqa F401

_logger = logging.getLogger(__name__)


class PreviewStitchingPlot(_PlotWithWaitingLabel, StitchAndBackgroundAlphaMixIn):
    DEFAULT_STITCHED_IMG_ALPHA = 0.95
    DEFAULT_BACKGROUND_IMG_ALPHA = 0.15

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)  # pylint: disable=E1123
        self._stitched_image = None
        self._composition_background = None

        # tune plot
        self.getPlotWidget().setYAxisInverted(settings.Y_AXIS_DOWNWARD)
        # by default we want to have a full screen display
        self.setAxesDisplayed(False)

        # add an action to plot the url-image 'full size'
        fullScreenIcon = tomwer_icons.getQIcon("full_screen")
        self._fullScreenAction = qt.QAction(fullScreenIcon, "pop up full screen")
        self.toolBar().addAction(self._fullScreenAction)
        self._fullScreenAction.triggered.connect(self._popCurrentImageFullScreen)

        self.setKeepDataAspectRatio(True)
        self.getColorBarWidget().hide()

        # removing some plot action to clear toolbar
        self.getMaskAction().setVisible(False)
        self.getCopyAction().setVisible(False)

        # background action
        self._backgroundToolbar = qt.QToolBar("background")
        self.addToolBar(self._backgroundToolbar)
        self._backgroundToolbar.addAction(self._backGroundAction)

        # alpha channel widget
        self._backgroundToolbar.addWidget(self._alphaChannelWidget)

        # set up
        self.setAlphaBackgroundImg(value=self.DEFAULT_BACKGROUND_IMG_ALPHA)
        self.setAlphaStitchedImg(value=self.DEFAULT_STITCHED_IMG_ALPHA)
        self.setWaiting(False)

        # connect signal / slot
        self._backGroundAction.toggled.connect(self._update)

    def _popCurrentImageFullScreen(self):
        from tomwer.gui.visualization.fullscreenplot import FullScreenStitching

        new_plot = FullScreenStitching(
            stitching_img=self._stitched_image,
            background_img=self._composition_background,
        )
        # update alpha values with the current one
        new_plot.setAlphaBackgroundImg(self.getBackgroundImgAlpha())
        new_plot.setAlphaStitchedImg(self.getStitchedImgAlpha())
        new_plot.setWindowTitle("Stitching")

        # reuse the same colormap for conveniance (user modification on it will be applied everywhere)
        new_plot.setDefaultColormap(self.getDefaultColormap())
        new_plot.showFullScreen()

    def setComposition(self, composition: dict, frame_width: int, update=True):
        self._composition_background = self.buildCompositionBackground(
            composition, frame_width=frame_width
        )
        if update:
            self._updatePlot()

    @staticmethod
    def buildCompositionBackground(composition, frame_width):
        if "raw_compositon" not in composition:
            raise KeyError(
                "composition is expected to have a 'raw_compositon' key with {ZFrameComposition} describing raw composition as key"
            )
        else:
            raw_compositon = composition["raw_compositon"]
            assert isinstance(raw_compositon, ZFrameComposition)
        if "overlap_compositon" not in composition:
            raise KeyError(
                "composition is expected to have a 'overlap_compositon' key with {ZFrameComposition} describing overlap composition as key"
            )
        else:
            overlap_compositon = composition["overlap_compositon"]
            assert isinstance(overlap_compositon, ZFrameComposition)

        background = numpy.zeros(
            shape=(
                (raw_compositon.global_end_y[-1] - raw_compositon.global_start_y[0]),
                frame_width,
            ),
        )
        assert background.ndim == 2

        def get_next_color():
            while True:
                yield qt.QColor(qt.Qt.yellow).hue()
                yield qt.QColor(qt.Qt.magenta).hue()
                yield qt.QColor(qt.Qt.blue).hue()

        colors_raw_frames = []
        for _, color in zip(raw_compositon.local_end_y, get_next_color()):
            colored_frame = numpy.full(
                shape=(
                    raw_compositon.global_end_y[-1] - raw_compositon.global_start_y[0],
                    frame_width,
                ),
                fill_value=color,
            )
            colors_raw_frames.append(colored_frame)

        overlap_compositon.compose(
            background,
            colors_raw_frames,
        )
        return background

    def setStitchedTomoObj(
        self, tomo_obj_id: Union[BaseIdentifier, str], composition: dict
    ):
        """
        :param BaseIdentifier tomo_obj_id: identifier of the stitched object (scan of volume)
        :param dict composition: composition used to create the stitched object
        """
        if not isinstance(tomo_obj_id, (BaseIdentifier, str)):
            raise TypeError(
                f"stitched_scan is expected to be an instance of {TomoScanBase}"
            )
        scan = None
        volume = None
        try:
            scan = ScanFactory.create_tomo_object_from_identifier(tomo_obj_id)
        except Exception:
            try:
                volume = VolumeFactory.create_tomo_object_from_identifier(tomo_obj_id)
            except Exception:
                pass
            else:
                pass

        if scan is not None:
            if len(scan.projections) == 0:
                _logger.error(
                    f"stitched scan {tomo_obj_id} doesn't contains any projections"
                )
                return

            if not len(scan.projections) == 1:
                _logger.warning(
                    f"stitched scan preview is expected to have a single project. Get {len(scan.projections)}. Will display the first one"
                )

            first_proj_url = next(iter(scan.projections.items()))[1]
            self._stitched_image = get_data(first_proj_url)
        elif volume is not None:
            volume.load_data()
            assert volume.data.ndim == 3
            self._stitched_image = volume.data[:, 0, :]
        else:
            _logger.error(f"Fail to load stitched object {tomo_obj_id}")

        assert self._stitched_image.ndim == 2
        self._composition_background = self.buildCompositionBackground(
            composition=composition, frame_width=self._stitched_image.shape[1]
        )
        self._update()

    @property
    def composition_background(self):
        return self._composition_background

    @property
    def stitched_image(self):
        return self._stitched_image

    # expose API
    def getImage(self, *args, **kwargs):
        return self.getPlotWidget().getImage(*args, **kwargs)

    def addImage(self, *args, **kwargs):
        self.getPlotWidget().addImage(*args, **kwargs)

    def removeImage(self, *args, **kwargs):
        self.getPlotWidget().removeImage(*args, **kwargs)

    def toolBar(self, *args, **kwargs):
        return self.getPlotWidget().toolBar(*args, **kwargs)

    def setKeepDataAspectRatio(self, *args, **kwargs):
        return self.getPlotWidget().setKeepDataAspectRatio(*args, **kwargs)

    def getColorBarWidget(self, *args, **kwargs):
        return self.getPlotWidget().getColorBarWidget(*args, **kwargs)

    def getMaskAction(self, *args, **kwargs):
        return self.getPlotWidget().getMaskAction(*args, **kwargs)

    def getCopyAction(self, *args, **kwargs):
        return self.getPlotWidget().getCopyAction(*args, **kwargs)

    def addToolBar(self, *args, **kwargs):
        return self.getPlotWidget().addToolBar(*args, **kwargs)

    def setActiveImage(self, *args, **kwargs):
        return self.getPlotWidget().setActiveImage(*args, **kwargs)

    def setAxesDisplayed(self, *args, **kwargs):
        plotWidget = self.getPlotWidget()
        if hasattr(plotWidget, "setAxesDisplayed"):
            plotWidget.setAxesDisplayed(*args, **kwargs)

    def getDefaultColormap(self, *args, **kwargs):
        return self.getPlotWidget().getDefaultColormap()

    def setDefaultColormap(self, *args, **kwargs):
        return self.getPlotWidget().setDefaultColormap(*args, **kwargs)
