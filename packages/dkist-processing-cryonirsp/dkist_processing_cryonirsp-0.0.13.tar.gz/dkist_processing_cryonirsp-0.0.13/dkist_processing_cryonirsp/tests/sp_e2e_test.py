import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from random import randint

from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_header_validator import spec214_validator
from dkist_processing_common.manual import ManualProcessing
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.tasks import QualityL1Metrics
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_service_configuration import logger

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.assemble_movie import SPAssembleCryonirspMovie
from dkist_processing_cryonirsp.tasks.bad_pixel_map import BadPixelMapCalibration
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase
from dkist_processing_cryonirsp.tasks.dark import DarkCalibration
from dkist_processing_cryonirsp.tasks.gain import LampGainCalibration
from dkist_processing_cryonirsp.tasks.instrument_polarization import (
    SPInstrumentPolarizationCalibration,
)
from dkist_processing_cryonirsp.tasks.l1_output_data import SPSubmitQuality
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
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory

# from dkist_processing_cryonirsp.tests.e2e_helpers import LoadDarkCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import LoadGeometricCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import LoadInstPolCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import LoadLampCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import LoadSolarCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import SaveDarkCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import SaveGeometricCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import SaveInstPolCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import SaveLampCal
# from dkist_processing_cryonirsp.tests.e2e_helpers import SaveSolarCal

INV = False
try:
    from dkist_inventory.asdf_generator import dataset_from_fits

    INV = True
# Temp hack to work around import error caused by Stuart code updates...
except (ModuleNotFoundError, ImportError):
    # Bitbucket pipelines won't have dkist-inventory installed
    pass

QRM = False
try:
    from quality_report_maker.libraries import report
    from quality_report_maker.libraries.json_encoder import datetime_json_object_hook
    from quality_report_maker.libraries.json_encoder import DatetimeEncoder

    QRM = True
except ModuleNotFoundError:
    logger.warning("Could not find quality_report_maker (must be installed manually)")
if QRM:
    import matplotlib.pyplot as plt

    plt.ioff()


def translate_122_to_214_task(suffix: str):
    class Translate122To214L0(WorkflowTaskBase):
        def run(self) -> None:
            raw_dir = Path(self.scratch.scratch_base_path) / f"CRYONIRSP{self.recipe_run_id:03n}"
            if not os.path.exists(self.scratch.workflow_base_path):
                os.makedirs(self.scratch.workflow_base_path)

            if not raw_dir.exists():
                raise FileNotFoundError(
                    f"Expected to find a raw CRYONIRSP{self.recipe_run_id:03n} folder in {self.scratch.scratch_base_path}"
                )

            for file in raw_dir.glob(f"*.{suffix}"):
                translated_file_name = Path(self.scratch.workflow_base_path) / os.path.basename(
                    file
                )
                logger.info(f"Translating {file} -> {translated_file_name}")
                hdl = fits.open(file)
                # Handle both compressed and uncompressed files...
                if len(hdl) > 1:
                    hdl_header = hdl[1].header
                    hdl_data = hdl[1].data
                else:
                    hdl_header = hdl[0].header
                    hdl_data = hdl[0].data
                header = spec122_validator.validate_and_translate_to_214_l0(
                    hdl_header, return_type=fits.HDUList
                )[0].header

                comp_hdu = fits.CompImageHDU(header=header, data=hdl_data)
                comp_hdl = fits.HDUList([fits.PrimaryHDU(), comp_hdu])
                comp_hdl.writeto(translated_file_name, overwrite=True)

                hdl.close()
                del hdl
                comp_hdl.close()
                del comp_hdl

    return Translate122To214L0


def create_input_dataset_parameter_document(param_path: Path):
    class CreateInputDatasetParameterDocument(WorkflowTaskBase):
        def run(self) -> None:
            doc_path = self.scratch.workflow_base_path / "input_dataset_parameters.json"
            with open(doc_path, "w") as f:
                f.write(json.dumps(self.input_dataset_document_simple_parameters_part))
            self.tag(doc_path, CryonirspTag.input_dataset_parameters())
            logger.info(f"Wrote input dataset doc to {doc_path}")

        @property
        def input_dataset_document_simple_parameters_part(self):
            parameters_list = []
            value_id = randint(1000, 2000)
            param_class = cryonirsp_testing_parameters_factory(
                param_path=param_path, create_files=False
            )
            for pn, pv in asdict(param_class()).items():
                values = [
                    {
                        "parameterValueId": value_id,
                        "parameterValue": json.dumps(pv),
                        "parameterValueStartDate": "1946-11-20",
                    }
                ]
                parameter = {"parameterName": pn, "parameterValues": values}
                parameters_list.append(parameter)

            return parameters_list

    return CreateInputDatasetParameterDocument


def tag_inputs_task(suffix: str):
    class TagInputs(WorkflowTaskBase):
        def run(self) -> None:
            logger.info(f"Looking in {os.path.abspath(self.scratch.workflow_base_path)}")
            input_file_list = list(self.scratch.workflow_base_path.glob(f"*.{suffix}"))
            if len(input_file_list) == 0:
                raise FileNotFoundError(
                    f"Did not find any files matching '*.{suffix}' in {self.scratch.workflow_base_path}"
                )
            for file in input_file_list:
                logger.info(f"Found {file}")
                self.tag(path=file, tags=[CryonirspTag.input(), CryonirspTag.frame()])

    return TagInputs


def tag_linearized_inputs_task(suffix: str):
    class TagLinearizedInputs(WorkflowTaskBase):
        def run(self) -> None:
            logger.info(f"Looking in {os.path.abspath(self.scratch.workflow_base_path)}")
            input_file_list = list(self.scratch.workflow_base_path.glob(f"*.{suffix}"))
            if len(input_file_list) == 0:
                raise FileNotFoundError(
                    f"Did not find any files matching '*.{suffix}' in {self.scratch.workflow_base_path}"
                )
            for file in input_file_list:
                logger.info(f"Found {file}")
                self.tag(path=file, tags=[CryonirspTag.linearized(), CryonirspTag.frame()])
            # Update the arm_id constant, as it is derived in linearity processing
            with fits.open(file) as hdul:
                if len(hdul) == 1:
                    hdu = hdul[0]
                else:
                    hdu = hdul[1]
                arm_id = hdu.header["CNARMID"]
            self.constants._update({CryonirspBudName.arm_id.value: arm_id})

    return TagLinearizedInputs


def tag_output_frames_task(suffix: str):
    class TagOutputFrames(WorkflowTaskBase):
        def run(self) -> None:
            logger.info(f"Looking in {os.path.abspath(self.scratch.workflow_base_path)}")
            input_file_list = list(self.scratch.workflow_base_path.glob(f"*L1.{suffix}"))
            if len(input_file_list) == 0:
                raise FileNotFoundError(
                    f"Did not find any files matching '*.{suffix}' in {self.scratch.workflow_base_path}"
                )
            for file in input_file_list:
                logger.info(f"Found {file}")
                stokes_tag = CryonirspTag.stokes("I")
                for stokes in ["Q", "U", "V"]:
                    if f"_{stokes}_" in str(file):
                        stokes_tag = CryonirspTag.stokes(stokes)
                hdl = fits.open(file)
                hdr = hdl[1].header
                self.tag(
                    path=file,
                    tags=[
                        CryonirspTag.output(),
                        CryonirspTag.frame(),
                        stokes_tag,
                        CryonirspTag.meas_num(hdr["CNCMEAS"]),
                        CryonirspTag.scan_step(hdr["CNCURSCN"]),
                        CryonirspTag.map_scan(hdr["DSPSNUM"]),
                    ],
                )

    return TagOutputFrames


class MoviePrep(WorkflowTaskBase):
    def run(self):
        # Set the constants for map_scan and num_scans:
        self.constants._update({BudName.num_map_scans: 1})
        self.constants._update({"NUM_SCAN_STEPS": 101})
        self.constants._update({"INSTRUMENT": "CRYO-NIRSP"})
        self.constants._update({"NUM_MODSTATES": 8})


class ShowPolMode(CryonirspTaskBase):
    def run(self) -> None:
        logger.info(f"{self.constants.correct_for_polarization = }")


class ShowExposureTimes(CryonirspTaskBase):
    def run(self) -> None:
        logger.info(f"{self.constants.dark_exposure_times = }")
        logger.info(f"{self.constants.lamp_gain_exposure_times = }")
        logger.info(f"{self.constants.solar_gain_exposure_times = }")
        if self.constants.correct_for_polarization:
            try:
                getattr(self.constants, "polcal_exposure_times")
            except KeyError:
                logger.info(f"polcal_exposure_times is not defined, initializing it to []")
                self.constants._update({CryonirspBudName.polcal_exposure_times.value: []})
            finally:
                logger.info(f"{self.constants.polcal_exposure_times = }")
        logger.info(f"{self.constants.observe_exposure_times = }")


class SpoofDarkExposureTimes(CryonirspTaskBase):
    # We have only dark frames, so spoof the existence of gain1 frames for which darks must be computed
    def run(self) -> None:
        self.constants._update(
            {CryonirspBudName.lamp_gain_exposure_times.value: self.constants.dark_exposure_times}
        )
        logger.info(f"{self.constants.lamp_gain_exposure_times = }")


class SpoofExposureTimeLists(CryonirspTaskBase):
    # Create empty exposure time lists for those that are not defined, to facilitate testing
    def run(self) -> None:
        # try:
        #     temp = self.constants.dark_exposure_times
        # except KeyError:
        #     self.constants._update({CryonirspBudName.dark_exposure_times.value: []})
        try:
            temp = self.constants.lamp_gain_exposure_times
        except KeyError:
            self.constants._update({CryonirspBudName.lamp_gain_exposure_times.value: []})
        try:
            temp = self.constants.solar_gain_exposure_times
        except KeyError:
            self.constants._update({CryonirspBudName.solar_gain_exposure_times.value: []})
        try:
            temp = self.constants.polcal_exposure_times
        except KeyError:
            self.constants._update({CryonirspBudName.polcal_exposure_times.value: []})
        try:
            temp = self.constants.observe_exposure_times
        except KeyError:
            self.constants._update({CryonirspBudName.observe_exposure_times.value: []})


class SetWavelengthForTesting(WorkflowTaskBase):
    def run(self):
        self.constants._update({CryonirspBudName.wavelength.value: 123.456})


class SubmitAndExposeQuality(SPSubmitQuality):
    """A direct copy paste of SumbitQuality with an additional step of writing the report to disk"""

    def run(self):
        # To make sure the subclassing worked
        super().run()

        # Now regenerate the report str and save it
        if QRM:
            logger.info("Building quality report for save to disk")
            report_str = self.quality_build_report(polcal_label_list=self.polcal_label_list)

            doc_path = self.scratch.workflow_base_path / "quality_report.json"
            report_container = {
                "datasetId": self.constants.dataset_id,
                "qualityReport": json.dumps(report_str, cls=DatetimeEncoder),
            }
            json_str = json.dumps(report_container)
            with open(doc_path, "w") as f:
                f.write(json_str)
            logger.info(f"Wrote report to {doc_path}")


class ValidateL1Output(CryonirspTaskBase):
    def run(self) -> None:
        files = self.read(tags=[CryonirspTag.output(), CryonirspTag.frame()])
        for f in files:
            logger.info(f"Validating {f}")
            spec214_validator.validate(f, extra=False)


def setup_APM_config() -> None:
    mesh_config = {
        "system-monitoring-log-apm": {
            "mesh_address": "system-monitoring-log-apm.service.sim.consul",
            "mesh_port": 8200,
        },
        "automated-processing-scratch-inventory": {"mesh_address": "localhost", "mesh_port": 6379},
        "internal-api-gateway": {"mesh_address": "localhost", "mesh_port": 80},
    }
    apm_options = {"TRANSACTION_MAX_SPANS": 10000}
    os.environ["MESH_CONFIG"] = json.dumps(mesh_config)
    os.environ["ELASTIC_APM_ENABLED"] = "true"
    os.environ["ELASTIC_APM_OTHER_OPTIONS"] = json.dumps(apm_options)


def make_pdf_report(scratch_path: str, recipe_run_id: int) -> None:
    if not QRM:
        logger.info("Did NOT make quality report pdf because quality_report_maker is not installed")
        return

    json_file = os.path.join(scratch_path, str(recipe_run_id), "quality_report.json")
    pdf_file = os.path.join(scratch_path, str(recipe_run_id), "quality_report.pdf")
    with open(json_file, "r") as f:
        report_container = json.load(f)
        dataset_id = report_container["datasetId"]
        report_str = json.loads(
            report_container["qualityReport"], object_hook=datetime_json_object_hook
        )

    pdf_bytes = report.format_report(report_str, f"GROGU_TEST_{dataset_id}")
    with open(pdf_file, "wb") as f:
        f.write(pdf_bytes)

    logger.info(f"Wrote quality report PDF to {pdf_file}")


def make_dataset_asdf(recipe_run_id, scratch_path):
    if not INV:
        logger.warning("Did NOT make dataset asdf file because dkist_inventory is not installed")
        return

    output_dir = os.path.join(scratch_path, str(recipe_run_id))
    asdf_name = f"dataset_{recipe_run_id:03n}.asdf"
    logger.info(f"Creating ASDF file from {output_dir} and saving to {asdf_name}")
    dataset_from_fits(output_dir, asdf_name, hdu=1)


def main(
    scratch_path: str,
    suffix: str = "FITS",
    recipe_run_id: int = 2,
    skip_translation: bool = False,
    only_translate: bool = False,
    load_dark: bool = False,
    load_lamp: bool = False,
    load_geometric: bool = False,
    load_solar: bool = False,
    load_inst_pol: bool = False,
    use_apm: bool = False,
    param_path: Path = None,
):
    if use_apm:
        setup_APM_config()
    with ManualProcessing(
        workflow_path=Path(scratch_path),
        recipe_run_id=recipe_run_id,
        testing=True,
        workflow_name="sp_l0_to_l1_cryonirsp",
        workflow_version="GROGU",
    ) as manual_processing_run:
        if not skip_translation:
            manual_processing_run.run_task(task=translate_122_to_214_task(suffix))
        if only_translate:
            return
        manual_processing_run.run_task(
            task=create_input_dataset_parameter_document(param_path=param_path)
        )

        manual_processing_run.run_task(task=tag_inputs_task(suffix))
        manual_processing_run.run_task(task=ParseL0CryonirspRampData)
        manual_processing_run.run_task(task=LinearityCorrection)

        # manual_processing_run.run_task(task=tag_linearized_inputs_task(suffix))
        manual_processing_run.run_task(task=ParseL0CryonirspLinearizedData)
        # manual_processing_run.run_task(task=SetWavelengthForTesting)
        # manual_processing_run.run_task(task=SpoofExposureTimeLists)
        manual_processing_run.run_task(task=CryonirspL0QualityMetrics)
        manual_processing_run.run_task(task=ShowPolMode)
        manual_processing_run.run_task(task=ShowExposureTimes)
        manual_processing_run.run_task(task=BadPixelMapCalibration)
        manual_processing_run.run_task(task=SPBeamBoundariesCalibration)
        # manual_processing_run.run_task(task=SpoofDarkExposureTimes)
        manual_processing_run.run_task(task=DarkCalibration)
        manual_processing_run.run_task(task=LampGainCalibration)
        manual_processing_run.run_task(task=SPGeometricCalibration)
        manual_processing_run.run_task(task=SPSolarGainCalibration)
        manual_processing_run.run_task(task=SPInstrumentPolarizationCalibration)
        # if load_dark:
        #    manual_processing_run.run_task(task=LoadDarkCal)
        # else:
        #    manual_processing_run.run_task(task=DarkCalibration)
        #    manual_processing_run.run_task(task=SaveDarkCal)
        #
        # if load_lamp:
        #     manual_processing_run.run_task(task=LoadLampCal)
        # else:
        #     manual_processing_run.run_task(task=LampCalibration)
        #     manual_processing_run.run_task(task=SaveLampCal)
        #
        # if load_geometric:
        #     manual_processing_run.run_task(task=LoadGeometricCal)
        # else:
        #     manual_processing_run.run_task(task=GeometricCalibration)
        #     manual_processing_run.run_task(task=SaveGeometricCal)
        #
        # if load_solar:
        #     manual_processing_run.run_task(task=LoadSolarCal)
        # else:
        #     manual_processing_run.run_task(task=SolarCalibration)
        #     manual_processing_run.run_task(task=SaveSolarCal)
        #
        # if load_inst_pol:
        #     manual_processing_run.run_task(task=LoadInstPolCal)
        # else:
        #     manual_processing_run.run_task(task=InstrumentPolarizationCalibration)
        #     manual_processing_run.run_task(task=SaveInstPolCal)

        manual_processing_run.run_task(task=SPScienceCalibration)
        manual_processing_run.run_task(task=SPWriteL1Frame)
        # manual_processing_run.run_task(task=tag_output_frames_task(suffix=suffix))
        # manual_processing_run.run_task(task=MoviePrep)
        manual_processing_run.run_task(task=QualityL1Metrics)
        manual_processing_run.run_task(task=CryonirspL1QualityMetrics)
        manual_processing_run.run_task(task=SubmitAndExposeQuality)
        manual_processing_run.run_task(task=ValidateL1Output)

        manual_processing_run.run_task(task=SPMakeCryonirspMovieFrames)
        manual_processing_run.run_task(task=SPAssembleCryonirspMovie)

        # Test some downstream services
        make_dataset_asdf(recipe_run_id, scratch_path)
        make_pdf_report(scratch_path, recipe_run_id)

        if any([load_dark, load_lamp, load_geometric, load_solar, load_inst_pol]):
            logger.info("NOT counting provenance records because some tasks were skipped")
        else:
            manual_processing_run.count_provenance()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run an end-to-end test of the Cryonirsp DC Science pipeline"
    )
    parser.add_argument("scratch_path", help="Location to use as the DC 'scratch' disk")
    parser.add_argument(
        "-i",
        "--run-id",
        help="Which subdir to use. This will become the recipe run id",
        type=int,
        default=4,
    )
    parser.add_argument("--suffix", help="File suffix to treat as INPUT frames", default="FITS")
    parser.add_argument(
        "-T",
        "--skip-translation",
        help="Skip the translation of raw 122 l0 frames to 214 l0",
        action="store_true",
    )
    parser.add_argument(
        "-t", "--only-translate", help="Do ONLY the translation step", action="store_true"
    )
    parser.add_argument(
        "-D",
        "--load-dark",
        help="Load dark calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-L",
        "--load-lamp",
        help="Load lamp calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-G",
        "--load-geometric",
        help="Load geometric calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-S",
        "--load-solar",
        help="Load solar calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-P",
        "--load-inst-pol",
        help="Load instrument polarization calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument("-A", "--use-apm", help="Send APM spans to SIM", action="store_true")
    parser.add_argument(
        "-p",
        "--param-path",
        help="Path to parameter directory",
        type=str,
        default=None,
    )

    args = parser.parse_args()
    sys.exit(
        main(
            scratch_path=args.scratch_path,
            suffix=args.suffix,
            recipe_run_id=args.run_id,
            skip_translation=args.skip_translation,
            only_translate=args.only_translate,
            load_dark=args.load_dark,
            load_lamp=args.load_lamp,
            load_geometric=args.load_geometric,
            load_solar=args.load_solar,
            load_inst_pol=args.load_inst_pol,
            use_apm=args.use_apm,
            param_path=Path(args.param_path),
        )
    )
