import json

import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.assemble_movie import CIAssembleCryonirspMovie
from dkist_processing_cryonirsp.tasks.assemble_movie import SPAssembleCryonirspMovie
from dkist_processing_cryonirsp.tests.conftest import Cryonirsp122ObserveFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import generate_214_l1_fits_frame


@pytest.fixture(scope="function")
def assemble_ci_task_with_tagged_movie_frames(tmp_path, recipe_run_id, init_cryonirsp_constants_db):
    num_map_scans = 10
    num_scan_steps = 1
    init_cryonirsp_constants_db(recipe_run_id, CryonirspConstantsDb(NUM_MAP_SCANS=num_map_scans))
    with CIAssembleCryonirspMovie(
        recipe_run_id=recipe_run_id,
        workflow_name="ci_cryo_make_movie_frames",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            task.testing_num_map_scans = num_map_scans
            task.num_steps = num_scan_steps
            task.num_exp_per_step = 1
            ds = Cryonirsp122ObserveFrames(
                array_shape=(1, 100, 100),
                num_steps=task.num_steps,
                num_exp_per_step=task.num_exp_per_step,
                num_map_scans=task.testing_num_map_scans,
            )
            header_generator = (d.header() for d in ds)
            for d, header in enumerate(header_generator):
                for scan_step in range(num_scan_steps + 1):
                    hdl = generate_214_l1_fits_frame(s122_header=header)
                    task.write(
                        data=hdl,
                        tags=[
                            CryonirspTag.movie_frame(),
                            CryonirspTag.map_scan(d + 1),
                            CryonirspTag.scan_step(scan_step),
                        ],
                        encoder=fits_hdulist_encoder,
                    )
            yield task
        finally:
            task._purge()


def test_assemble_ci_movie(assemble_ci_task_with_tagged_movie_frames, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    assemble_ci_task_with_tagged_movie_frames()
    movie_file = list(assemble_ci_task_with_tagged_movie_frames.read(tags=[CryonirspTag.movie()]))
    assert len(movie_file) == 1
    assert movie_file[0].exists()


@pytest.fixture(scope="function")
def assemble_sp_task_with_tagged_movie_frames(tmp_path, recipe_run_id, init_cryonirsp_constants_db):
    num_map_scans = 10
    init_cryonirsp_constants_db(recipe_run_id, CryonirspConstantsDb(NUM_MAP_SCANS=num_map_scans))
    with SPAssembleCryonirspMovie(
        recipe_run_id=recipe_run_id,
        workflow_name="sp_cryo_make_movie_frames",
        workflow_version="VX.Y",
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            task.testing_num_map_scans = num_map_scans
            task.num_steps = 1  # do we need num_steps and num_exp_per_step for SP?
            task.num_exp_per_step = 1
            ds = Cryonirsp122ObserveFrames(
                array_shape=(1, 100, 100),
                num_steps=task.num_steps,
                num_exp_per_step=task.num_exp_per_step,
                num_map_scans=task.testing_num_map_scans,
            )
            header_generator = (d.header() for d in ds)
            for d, header in enumerate(header_generator):
                hdl = generate_214_l1_fits_frame(s122_header=header)
                task.write(
                    data=hdl,
                    tags=[
                        CryonirspTag.movie_frame(),
                        CryonirspTag.map_scan(d + 1),
                    ],
                    encoder=fits_hdulist_encoder,
                )
            yield task
        finally:
            task._purge()


def test_assemble_sp_movie(assemble_sp_task_with_tagged_movie_frames, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    assemble_sp_task_with_tagged_movie_frames()
    movie_file = list(assemble_sp_task_with_tagged_movie_frames.read(tags=[CryonirspTag.movie()]))
    assert len(movie_file) == 1
    assert movie_file[0].exists()
