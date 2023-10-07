"""CryoNIRSP-specific assemble movie task subclass."""
from dkist_processing_common.tasks import AssembleMovie
from logging42 import logger
from PIL import ImageDraw

from dkist_processing_cryonirsp.models.constants import CryonirspConstants
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess
from dkist_processing_cryonirsp.parsers.cryonirsp_l1_fits_access import CryonirspL1FitsAccess


class AssembleCryonirspMovieBase(AssembleMovie):
    """
    Assemble all CryoNIRSP movie frames (tagged with CryonirspTag.movie_frame()) into an mp4 movie file.

    Subclassed from the AssembleMovie task in dkist_processing_common to add CryoNIRSP specific text overlays.


    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs


    """

    @property
    def constants_model_class(self):
        """Get CryoNIRSP constants."""
        return CryonirspConstants

    @property
    def fits_parsing_class(self):
        """Cryonirsp specific subclass of L1FitsAccess to use for reading images."""
        return CryonirspL1FitsAccess

    def write_overlay(self, draw: ImageDraw, fits_obj: CryonirspL0FitsAccess) -> None:
        """
        Mark each image with it's instrument, observed wavelength, and observation time.

        Parameters
        ----------
        draw
            A PIL.ImageDraw object

        fits_obj
            A single movie "image", i.e., a single array tagged with CryonirspTag.movie_frame
        """
        self.write_line(
            draw=draw,
            text=f"INSTRUMENT: {self.constants.instrument}",
            line=3,
            column="right",
            font=self.font_36,
        )
        self.write_line(
            draw=draw,
            text=f"WAVELENGTH: {fits_obj.wavelength} nm",
            line=2,
            column="right",
            font=self.font_36,
        )
        self.write_line(
            draw=draw,
            text=f"OBS TIME: {fits_obj.time_obs}",
            line=1,
            column="right",
            font=self.font_36,
        )

        if self.constants.correct_for_polarization:
            # The `line` on which an item is drawn is a multiple of the height of that line.
            # The "Q" character is slightly taller than the rest and so n units of the "I   Q"
            # line are taller than n units of the "U   V" line.
            self.write_line(draw=draw, text="I   Q", line=17, column="middle", font=self.font_36)
            self.write_line(draw=draw, text="U   V", line=17, column="middle", font=self.font_36)


class CIAssembleCryonirspMovie(AssembleCryonirspMovieBase):
    """
    Assemble all CryoNIRSP CI movie frames (tagged with CryonirspTag.movie_frame()) into an mp4 movie file.

    Subclassed from the AssembleMovie task in dkist_processing_common to add CryoNIRSP specific text overlays.


    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs


    """

    @property
    def num_images(self) -> int:
        """Total number of images in final movie.

        Overloaded from `dkist-processing-common` because DSPS repeat does not correspond to map scan in CryoNIRSP
        """
        return self.constants.num_map_scans * self.constants.num_scan_steps

    def tags_for_image_n(self, n: int) -> list[str]:
        """Return tags that grab the n'th movie image.

        Overloaded from `dkist-processing-common` because DSPS repeat does not correspond to map scan in CryoNIRSP
        """
        map_scan_num = n // self.constants.num_scan_steps + 1
        scan_step = n % self.constants.num_scan_steps + 1

        tags = [
            CryonirspTag.map_scan(map_scan_num),
            CryonirspTag.scan_step(scan_step),
        ]
        logger.info(f"AssembleMovie.tags_for_image_n: {tags =}")
        return tags


class SPAssembleCryonirspMovie(AssembleCryonirspMovieBase):
    """
    Assemble all CryoNIRSP SP movie frames (tagged with CryonirspTag.movie_frame()) into an mp4 movie file.

    Subclassed from the AssembleMovie task in dkist_processing_common to add CryoNIRSP specific text overlays.


    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs


    """

    @property
    def num_images(self) -> int:
        """Total number of images in final movie.

        Overloaded from `dkist-processing-common` because DSPS repeat does not correspond to map scan in CryoNIRSP
        """
        return self.constants.num_map_scans

    def tags_for_image_n(self, n: int) -> list[str]:
        """Return tags that grab the n'th movie image.

        Overloaded from `dkist-processing-common` because DSPS repeat does not correspond to map scan in CryoNIRSP
        """
        return [CryonirspTag.map_scan(n + 1)]
