import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from random import randint

from dkist_processing_common.manual import ManualProcessing
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_service_configuration import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.linearity_correction import LinearityCorrection
from dkist_processing_cryonirsp.tasks.parse import ParseL0CryonirspRampData
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory


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
                param_path=Path(param_path), create_files=False
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


def main(
    scratch_path: str,
    suffix: str = "dat",
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
    with ManualProcessing(
        workflow_path=Path(scratch_path),
        recipe_run_id=recipe_run_id,
        testing=True,
        workflow_name="cryonirsp-l0-pipeline",  # need sperate workflows for CI and SP?
        workflow_version="GROGU",
    ) as manual_processing_run:
        manual_processing_run.run_task(
            task=create_input_dataset_parameter_document(param_path=param_path)
        )
        manual_processing_run.run_task(task=tag_inputs_task(suffix))
        manual_processing_run.run_task(task=ParseL0CryonirspRampData)
        manual_processing_run.run_task(task=LinearityCorrection)


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
