"""CryoNIRSP FITS access for L0 data."""
from astropy.io import fits
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess


class CryonirspRampFitsAccess(L0FitsAccess):
    """
    Class to provide easy access to L0 headers for non-linearized (raw) CryoNIRSP data.

    i.e. instead of <CryonirspL0FitsAccess>.header['key'] this class lets us use <CryonirspL0FitsAccess>.key instead

    Parameters
    ----------
    hdu :
        Fits L0 header object

    name : str
        The name of the file that was loaded into this FitsAccess object

    auto_squeeze : bool
        When set to True, dimensions of length 1 will be removed from the array
    """

    def __init__(
        self,
        hdu: fits.ImageHDU | fits.PrimaryHDU | fits.CompImageHDU,
        name: str | None = None,
        auto_squeeze: bool = True,
    ):
        super().__init__(hdu=hdu, name=name, auto_squeeze=auto_squeeze)

        self.camera_readout_mode = self.header["CNCAMMD"]
        self.curr_frame_in_ramp: int = self.header["CNCNDR"]
        self.arm_id: str = self.header["CNARMID"]
        self.roi_1_origin_x = self.header["HWROI1OX"]
        self.roi_1_origin_y = self.header["HWROI1OY"]
        self.roi_1_size_x = self.header["HWROI1SX"]
        self.roi_1_size_y = self.header["HWROI1SY"]


class CryonirspL0FitsAccess(L0FitsAccess):
    """
    Class to provide easy access to L0 headers for linearized (ready for processing) CryoNIRSP data.

    i.e. instead of <CryonirspL0FitsAccess>.header['key'] this class lets us use <CryonirspL0FitsAccess>.key instead

    Parameters
    ----------
    hdu :
        Fits L0 header object

    name : str
        The name of the file that was loaded into this FitsAccess object

    auto_squeeze : bool
        When set to True, dimensions of length 1 will be removed from the array
    """

    def __init__(
        self,
        hdu: fits.ImageHDU | fits.PrimaryHDU | fits.CompImageHDU,
        name: str | None = None,
        auto_squeeze: bool = True,
    ):
        super().__init__(hdu=hdu, name=name, auto_squeeze=auto_squeeze)

        self.arm_id: str = self.header["CNARMID"]
        self.number_of_modulator_states: int = self.header["CNMODNST"]
        self.modulator_state: int = self.header["CNMODCST"]
        self.scan_step: int = self.header["CNCURSCN"]
        self.num_scan_steps: int = self.header["CNNUMSCN"]
        self.meas_num: int = self.header["CNCMEAS"]
        self.num_meas: int = self.header["CNNMEAS"]
        self.sub_repeat_num = self.header["CNCSREP"]
        self.num_sub_repeats: int = self.header["CNSUBREP"]
        self.modulator_spin_mode: str = self.header["CNSPINMD"]
        self.axis_1_type: str = self.header["CTYPE1"]
        self.axis_2_type: str = self.header["CTYPE2"]
        self.axis_3_type: str = self.header["CTYPE3"]
