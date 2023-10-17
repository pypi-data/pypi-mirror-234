"""Workflows for trial runs (i.e., not Production)."""
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TrialTeardown
from dkist_processing_core import ResourceQueue
from dkist_processing_core import Workflow

from dkist_processing_cryonirsp.tasks.bad_pixel_map import BadPixelMapCalibration
from dkist_processing_cryonirsp.tasks.ci_beam_boundaries import CIBeamBoundariesCalibration
from dkist_processing_cryonirsp.tasks.ci_science import CIScienceCalibration
from dkist_processing_cryonirsp.tasks.dark import DarkCalibration
from dkist_processing_cryonirsp.tasks.gain import CISolarGainCalibration
from dkist_processing_cryonirsp.tasks.gain import LampGainCalibration
from dkist_processing_cryonirsp.tasks.instrument_polarization import (
    CIInstrumentPolarizationCalibration,
)
from dkist_processing_cryonirsp.tasks.instrument_polarization import (
    SPInstrumentPolarizationCalibration,
)
from dkist_processing_cryonirsp.tasks.linearity_correction import LinearityCorrection
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspLinearizedData
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspRampData
from dkist_processing_cryonirsp.tasks.sp_beam_boundaries import SPBeamBoundariesCalibration
from dkist_processing_cryonirsp.tasks.sp_geometric import SPGeometricCalibration
from dkist_processing_cryonirsp.tasks.sp_science import SPScienceCalibration
from dkist_processing_cryonirsp.tasks.sp_solar_gain import SPSolarGainCalibration
from dkist_processing_cryonirsp.tasks.trial_output_data import TransferCryoTrialData
from dkist_processing_cryonirsp.tasks.write_l1 import CIWriteL1Frame
from dkist_processing_cryonirsp.tasks.write_l1 import SPWriteL1Frame

full_trial_ci_pipeline = Workflow(
    category="cryonirsp_ci",
    input_data="l0",
    output_data="l1",
    detail="full-trial",
    workflow_package=__package__,
)
full_trial_ci_pipeline.add_node(task=TransferL0Data, upstreams=None)
full_trial_ci_pipeline.add_node(task=ParseL0CryonirspRampData, upstreams=TransferL0Data)
full_trial_ci_pipeline.add_node(
    task=LinearityCorrection,
    resource_queue=ResourceQueue.HIGH_MEMORY,
    upstreams=ParseL0CryonirspRampData,
)
full_trial_ci_pipeline.add_node(task=ParseL0CryonirspLinearizedData, upstreams=LinearityCorrection)
full_trial_ci_pipeline.add_node(
    task=BadPixelMapCalibration, upstreams=ParseL0CryonirspLinearizedData
)
full_trial_ci_pipeline.add_node(task=CIBeamBoundariesCalibration, upstreams=BadPixelMapCalibration)
full_trial_ci_pipeline.add_node(task=DarkCalibration, upstreams=CIBeamBoundariesCalibration)
full_trial_ci_pipeline.add_node(task=LampGainCalibration, upstreams=DarkCalibration)
full_trial_ci_pipeline.add_node(task=CISolarGainCalibration, upstreams=LampGainCalibration)
full_trial_ci_pipeline.add_node(
    task=CIInstrumentPolarizationCalibration, upstreams=CISolarGainCalibration
)
full_trial_ci_pipeline.add_node(
    task=CIScienceCalibration, upstreams=CIInstrumentPolarizationCalibration
)
full_trial_ci_pipeline.add_node(task=CIWriteL1Frame, upstreams=CIScienceCalibration)
full_trial_ci_pipeline.add_node(task=TransferCryoTrialData, upstreams=CIWriteL1Frame)
full_trial_ci_pipeline.add_node(task=TrialTeardown, upstreams=TransferCryoTrialData)

non_science_ci_pipeline = Workflow(
    category="cryonirsp_ci",
    input_data="l0",
    output_data="l1",
    detail="non-science-trial",
    workflow_package=__package__,
)
non_science_ci_pipeline.add_node(task=TransferL0Data, upstreams=None)
non_science_ci_pipeline.add_node(task=ParseL0CryonirspRampData, upstreams=TransferL0Data)
non_science_ci_pipeline.add_node(
    task=LinearityCorrection,
    resource_queue=ResourceQueue.HIGH_MEMORY,
    upstreams=ParseL0CryonirspRampData,
)
non_science_ci_pipeline.add_node(task=ParseL0CryonirspLinearizedData, upstreams=LinearityCorrection)
non_science_ci_pipeline.add_node(
    task=BadPixelMapCalibration, upstreams=ParseL0CryonirspLinearizedData
)
non_science_ci_pipeline.add_node(task=CIBeamBoundariesCalibration, upstreams=BadPixelMapCalibration)
non_science_ci_pipeline.add_node(task=DarkCalibration, upstreams=CIBeamBoundariesCalibration)
non_science_ci_pipeline.add_node(task=LampGainCalibration, upstreams=DarkCalibration)
non_science_ci_pipeline.add_node(task=CISolarGainCalibration, upstreams=LampGainCalibration)
non_science_ci_pipeline.add_node(
    task=CIInstrumentPolarizationCalibration, upstreams=CISolarGainCalibration
)
non_science_ci_pipeline.add_node(
    task=TransferCryoTrialData, upstreams=CIInstrumentPolarizationCalibration
)
non_science_ci_pipeline.add_node(task=TrialTeardown, upstreams=TransferCryoTrialData)

full_trial_sp_pipeline = Workflow(
    category="cryonirsp_sp",
    input_data="l0",
    output_data="l1",
    detail="full-trial",
    workflow_package=__package__,
)
full_trial_sp_pipeline.add_node(task=TransferL0Data, upstreams=None)
full_trial_sp_pipeline.add_node(task=ParseL0CryonirspRampData, upstreams=TransferL0Data)
full_trial_sp_pipeline.add_node(
    task=LinearityCorrection,
    resource_queue=ResourceQueue.HIGH_MEMORY,
    upstreams=ParseL0CryonirspRampData,
)
full_trial_sp_pipeline.add_node(task=ParseL0CryonirspLinearizedData, upstreams=LinearityCorrection)
full_trial_sp_pipeline.add_node(
    task=BadPixelMapCalibration, upstreams=ParseL0CryonirspLinearizedData
)
full_trial_sp_pipeline.add_node(task=SPBeamBoundariesCalibration, upstreams=BadPixelMapCalibration)
full_trial_sp_pipeline.add_node(task=DarkCalibration, upstreams=SPBeamBoundariesCalibration)
full_trial_sp_pipeline.add_node(task=LampGainCalibration, upstreams=DarkCalibration)
full_trial_sp_pipeline.add_node(task=SPGeometricCalibration, upstreams=LampGainCalibration)
full_trial_sp_pipeline.add_node(task=SPSolarGainCalibration, upstreams=SPGeometricCalibration)
full_trial_sp_pipeline.add_node(
    task=SPInstrumentPolarizationCalibration, upstreams=SPSolarGainCalibration
)
full_trial_sp_pipeline.add_node(
    task=SPScienceCalibration, upstreams=SPInstrumentPolarizationCalibration
)
full_trial_sp_pipeline.add_node(task=SPWriteL1Frame, upstreams=SPScienceCalibration)
full_trial_sp_pipeline.add_node(task=TransferCryoTrialData, upstreams=SPWriteL1Frame)
full_trial_sp_pipeline.add_node(task=TrialTeardown, upstreams=TransferCryoTrialData)

non_science_sp_pipeline = Workflow(
    category="cryonirsp_sp",
    input_data="l0",
    output_data="l1",
    detail="non-science-trial",
    workflow_package=__package__,
)
non_science_sp_pipeline.add_node(task=TransferL0Data, upstreams=None)
non_science_sp_pipeline.add_node(task=ParseL0CryonirspRampData, upstreams=TransferL0Data)
non_science_sp_pipeline.add_node(
    task=LinearityCorrection,
    resource_queue=ResourceQueue.HIGH_MEMORY,
    upstreams=ParseL0CryonirspRampData,
)
non_science_sp_pipeline.add_node(task=ParseL0CryonirspLinearizedData, upstreams=LinearityCorrection)
non_science_sp_pipeline.add_node(
    task=BadPixelMapCalibration, upstreams=ParseL0CryonirspLinearizedData
)
non_science_sp_pipeline.add_node(task=SPBeamBoundariesCalibration, upstreams=BadPixelMapCalibration)
non_science_sp_pipeline.add_node(task=DarkCalibration, upstreams=SPBeamBoundariesCalibration)
non_science_sp_pipeline.add_node(task=LampGainCalibration, upstreams=DarkCalibration)
non_science_sp_pipeline.add_node(task=SPGeometricCalibration, upstreams=LampGainCalibration)
non_science_sp_pipeline.add_node(task=SPSolarGainCalibration, upstreams=SPGeometricCalibration)
non_science_sp_pipeline.add_node(
    task=SPInstrumentPolarizationCalibration, upstreams=SPSolarGainCalibration
)
non_science_sp_pipeline.add_node(
    task=TransferCryoTrialData, upstreams=SPInstrumentPolarizationCalibration
)
non_science_sp_pipeline.add_node(task=TrialTeardown, upstreams=TransferCryoTrialData)
