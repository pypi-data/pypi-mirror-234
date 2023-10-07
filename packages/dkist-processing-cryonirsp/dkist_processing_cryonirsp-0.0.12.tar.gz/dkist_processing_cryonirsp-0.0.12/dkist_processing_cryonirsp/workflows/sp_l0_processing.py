"""Cryo SP raw data processing workflow."""
from dkist_processing_common.tasks import AddDatasetReceiptAccount
from dkist_processing_common.tasks import PublishCatalogAndQualityMessages
from dkist_processing_common.tasks import QualityL1Metrics
from dkist_processing_common.tasks import SubmitQuality
from dkist_processing_common.tasks import Teardown
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TransferL1Data
from dkist_processing_core import ResourceQueue
from dkist_processing_core import Workflow

from dkist_processing_cryonirsp.tasks.assemble_movie import SPAssembleCryonirspMovie
from dkist_processing_cryonirsp.tasks.bad_pixel_map import BadPixelMapCalibration
from dkist_processing_cryonirsp.tasks.dark import DarkCalibration
from dkist_processing_cryonirsp.tasks.gain import LampGainCalibration
from dkist_processing_cryonirsp.tasks.instrument_polarization import (
    SPInstrumentPolarizationCalibration,
)
from dkist_processing_cryonirsp.tasks.linearity_correction import LinearityCorrection
from dkist_processing_cryonirsp.tasks.make_movie_frames import SPMakeCryonirspMovieFrames
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspLinearizedData
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspRampData
from dkist_processing_cryonirsp.tasks.quality_metrics import CryonirspL0QualityMetrics
from dkist_processing_cryonirsp.tasks.quality_metrics import CryonirspL1QualityMetrics
from dkist_processing_cryonirsp.tasks.sp_beam_boundaries import SPBeamBoundariesCalibration
from dkist_processing_cryonirsp.tasks.sp_geometric import SPGeometricCalibration
from dkist_processing_cryonirsp.tasks.sp_science import SPScienceCalibration
from dkist_processing_cryonirsp.tasks.sp_solar_gain import SPSolarGainCalibration
from dkist_processing_cryonirsp.tasks.write_l1 import SPWriteL1Frame

l0_pipeline = Workflow(
    category="cryonirsp_sp",
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
l0_pipeline.add_node(task=SPBeamBoundariesCalibration, upstreams=BadPixelMapCalibration)
l0_pipeline.add_node(task=DarkCalibration, upstreams=SPBeamBoundariesCalibration)
l0_pipeline.add_node(task=LampGainCalibration, upstreams=DarkCalibration)
l0_pipeline.add_node(task=SPGeometricCalibration, upstreams=LampGainCalibration)
l0_pipeline.add_node(task=SPSolarGainCalibration, upstreams=SPGeometricCalibration)
l0_pipeline.add_node(task=SPInstrumentPolarizationCalibration, upstreams=SPSolarGainCalibration)
l0_pipeline.add_node(task=SPScienceCalibration, upstreams=SPInstrumentPolarizationCalibration)
l0_pipeline.add_node(task=SPWriteL1Frame, upstreams=SPScienceCalibration)
l0_pipeline.add_node(task=QualityL1Metrics, upstreams=SPWriteL1Frame)
l0_pipeline.add_node(task=CryonirspL1QualityMetrics, upstreams=SPWriteL1Frame)
l0_pipeline.add_node(
    task=SubmitQuality,
    upstreams=[CryonirspL0QualityMetrics, QualityL1Metrics, CryonirspL1QualityMetrics],
)
l0_pipeline.add_node(task=SPMakeCryonirspMovieFrames, upstreams=SPWriteL1Frame)
l0_pipeline.add_node(task=SPAssembleCryonirspMovie, upstreams=SPMakeCryonirspMovieFrames)
l0_pipeline.add_node(
    task=AddDatasetReceiptAccount, upstreams=[SPAssembleCryonirspMovie, SubmitQuality]
)
l0_pipeline.add_node(task=TransferL1Data, upstreams=AddDatasetReceiptAccount)
l0_pipeline.add_node(
    task=PublishCatalogAndQualityMessages,
    upstreams=TransferL1Data,
)
l0_pipeline.add_node(task=Teardown, upstreams=PublishCatalogAndQualityMessages)
