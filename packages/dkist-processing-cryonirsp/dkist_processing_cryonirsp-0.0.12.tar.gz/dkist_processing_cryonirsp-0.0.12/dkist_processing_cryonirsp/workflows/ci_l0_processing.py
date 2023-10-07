"""Cryo CI raw data processing workflow."""
from dkist_processing_common.tasks import AddDatasetReceiptAccount
from dkist_processing_common.tasks import PublishCatalogAndQualityMessages
from dkist_processing_common.tasks import QualityL1Metrics
from dkist_processing_common.tasks import SubmitQuality
from dkist_processing_common.tasks import Teardown
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TransferL1Data
from dkist_processing_core import ResourceQueue
from dkist_processing_core import Workflow

from dkist_processing_cryonirsp.tasks.assemble_movie import CIAssembleCryonirspMovie
from dkist_processing_cryonirsp.tasks.bad_pixel_map import BadPixelMapCalibration
from dkist_processing_cryonirsp.tasks.ci_beam_boundaries import CIBeamBoundariesCalibration
from dkist_processing_cryonirsp.tasks.ci_science import CIScienceCalibration
from dkist_processing_cryonirsp.tasks.dark import DarkCalibration
from dkist_processing_cryonirsp.tasks.gain import CISolarGainCalibration
from dkist_processing_cryonirsp.tasks.gain import LampGainCalibration
from dkist_processing_cryonirsp.tasks.instrument_polarization import (
    CIInstrumentPolarizationCalibration,
)
from dkist_processing_cryonirsp.tasks.linearity_correction import LinearityCorrection
from dkist_processing_cryonirsp.tasks.make_movie_frames import CIMakeCryonirspMovieFrames
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspLinearizedData
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspRampData
from dkist_processing_cryonirsp.tasks.quality_metrics import CryonirspL0QualityMetrics
from dkist_processing_cryonirsp.tasks.quality_metrics import CryonirspL1QualityMetrics
from dkist_processing_cryonirsp.tasks.write_l1 import CIWriteL1Frame

l0_pipeline = Workflow(
    category="cryonirsp_ci",
    input_data="l0",
    output_data="l1",
    workflow_package=__package__,
)
l0_pipeline.add_node(task=TransferL0Data, upstreams=None)
l0_pipeline.add_node(task=ParseL0CryonirspRampData, upstreams=TransferL0Data)
l0_pipeline.add_node(
    task=LinearityCorrection,
    resource_queue=ResourceQueue.HIGH_MEMORY,
    upstreams=ParseL0CryonirspRampData,
)
l0_pipeline.add_node(task=ParseL0CryonirspLinearizedData, upstreams=LinearityCorrection)
l0_pipeline.add_node(task=CryonirspL0QualityMetrics, upstreams=ParseL0CryonirspLinearizedData)
l0_pipeline.add_node(task=BadPixelMapCalibration, upstreams=ParseL0CryonirspLinearizedData)
l0_pipeline.add_node(task=CIBeamBoundariesCalibration, upstreams=BadPixelMapCalibration)
l0_pipeline.add_node(task=DarkCalibration, upstreams=CIBeamBoundariesCalibration)
l0_pipeline.add_node(task=LampGainCalibration, upstreams=DarkCalibration)
l0_pipeline.add_node(task=CISolarGainCalibration, upstreams=LampGainCalibration)
l0_pipeline.add_node(task=CIInstrumentPolarizationCalibration, upstreams=CISolarGainCalibration)
l0_pipeline.add_node(task=CIScienceCalibration, upstreams=CIInstrumentPolarizationCalibration)
l0_pipeline.add_node(task=CIWriteL1Frame, upstreams=CIScienceCalibration)
l0_pipeline.add_node(task=QualityL1Metrics, upstreams=CIWriteL1Frame)
l0_pipeline.add_node(task=CryonirspL1QualityMetrics, upstreams=CIWriteL1Frame)
l0_pipeline.add_node(
    task=SubmitQuality,
    upstreams=[CryonirspL0QualityMetrics, QualityL1Metrics, CryonirspL1QualityMetrics],
)
l0_pipeline.add_node(task=CIMakeCryonirspMovieFrames, upstreams=CIWriteL1Frame)
l0_pipeline.add_node(task=CIAssembleCryonirspMovie, upstreams=CIMakeCryonirspMovieFrames)
l0_pipeline.add_node(
    task=AddDatasetReceiptAccount, upstreams=[CIAssembleCryonirspMovie, SubmitQuality]
)
l0_pipeline.add_node(task=TransferL1Data, upstreams=AddDatasetReceiptAccount)
l0_pipeline.add_node(
    task=PublishCatalogAndQualityMessages,
    upstreams=TransferL1Data,
)
l0_pipeline.add_node(task=Teardown, upstreams=PublishCatalogAndQualityMessages)
