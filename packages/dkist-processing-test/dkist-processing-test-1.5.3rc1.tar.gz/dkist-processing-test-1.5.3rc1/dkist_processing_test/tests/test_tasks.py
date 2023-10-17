"""
Tests for the tasks defined in this repo
"""
import json
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from random import randint
from uuid import uuid4

import numpy as np
import pytest
from astropy.io import fits
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tests.conftest import FakeGQLClient
from dkist_service_configuration import logger

from dkist_processing_test.models.parameters import TestParameters
from dkist_processing_test.tasks.exercise_numba import ExerciseNumba
from dkist_processing_test.tasks.fail import FailTask
from dkist_processing_test.tasks.fake_science import GenerateCalibratedData
from dkist_processing_test.tasks.movie import AssembleTestMovie
from dkist_processing_test.tasks.movie import MakeTestMovieFrames
from dkist_processing_test.tasks.noop import NoOpTask
from dkist_processing_test.tasks.trial_output_data import TransferTestTrialData
from dkist_processing_test.tasks.write_l1 import WriteL1Data
from dkist_processing_test.tests.conftest import generate_214_l0_fits_frame
from dkist_processing_test.tests.conftest import S122Headers


@dataclass
class FakeConstantDb:
    NUM_DSPS_REPEATS: int = 2
    INSTRUMENT: str = "TEST"
    AVERAGE_CADENCE: float = 10.0
    MINIMUM_CADENCE: float = 10.0
    MAXIMUM_CADENCE: float = 10.0
    VARIANCE_CADENCE: float = 0.0
    STOKES_PARAMS: tuple[str] = (
        "I",
        "Q",
        "U",
        "V",
    )  # A tuple because lists aren't allowed on dataclasses
    CONTRIBUTING_PROPOSAL_IDS: tuple[str] = ("abc", "def")
    CONTRIBUTING_EXPERIMENT_IDS: tuple[str] = ("ghi", "jkl")


@pytest.fixture()
def noop_task():
    return NoOpTask(recipe_run_id=1, workflow_name="noop", workflow_version="VX.Y")


def test_noop_task(noop_task):
    """
    Given: A NoOpTask
    When: Calling the task instance
    Then: No errors raised
    """
    noop_task()


@pytest.fixture()
def fail_task():
    return FailTask(recipe_run_id=1, workflow_name="fail", workflow_version="VX.Y")


def test_fail_task(fail_task):
    """
    Given: A FailTask
    When: Calling the task instance
    Then: Runtime Error raised
    """
    with pytest.raises(RuntimeError):
        fail_task()


@pytest.fixture()
def generate_calibrated_data_task(
    tmp_path,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
    parameter_file_object_key,
    random_parameter_hdulist,
):
    number_of_frames = 10
    with GenerateCalibratedData(
        recipe_run_id=recipe_run_id, workflow_name="GenerateCalibratedData", workflow_version="VX.Y"
    ) as task:
        # configure input data
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        input_frame_set = Spec122Dataset(
            instrument="vbi",
            dataset_shape=(number_of_frames, 512, 512),
            array_shape=(1, 512, 512),
            time_delta=10,
        )
        # load input data
        for idx, input_frame in enumerate(input_frame_set):
            hdu = input_frame.hdu()
            hdu.data = (
                np.ones(hdu.data.shape, dtype=int) * 10
            )  # Because input data will be ints in test system
            hdu.header["DSPSNUM"] = 1
            hdul = fits.HDUList([hdu])
            file_name = f"input_{idx}.fits"
            task.fits_data_write(hdu_list=hdul, tags=Tag.input(), relative_path=file_name)

        # Write parameter file
        hdul = random_parameter_hdulist[0]
        task.fits_data_write(hdu_list=hdul, tags=Tag.parameter(parameter_file_object_key))

        # This needs to be after we've tagged the parameter file
        assign_input_dataset_doc_to_task(task)

        # result
        yield task, number_of_frames
        # teardown
        task._purge()
    # disconnect


@pytest.fixture(scope="session")
def input_dataset_document_parameters_part_with_file(parameter_file_object_key):
    param_name = "test_random_data"
    value = {
        "__file__": {"bucket": "foo", "objectKey": parameter_file_object_key},
    }
    value_id = randint(1000, 2000)
    values = [
        {
            "parameterValueId": value_id,
            "parameterValue": json.dumps(value),
            "parameterValueStartDate": "1946-11-20",
        }
    ]
    parameter = {"parameterName": param_name, "parameterValues": values}
    parameters_list = [parameter]

    return parameters_list


@pytest.fixture(scope="session")
def assign_input_dataset_doc_to_task(input_dataset_document_parameters_part_with_file):
    def update_task(task):
        doc_path = task.scratch.workflow_base_path / "dataset_parameters.json"
        with open(doc_path, "w") as f:
            f.write(json.dumps(input_dataset_document_parameters_part_with_file))
        task.tag(doc_path, Tag.input_dataset_parameters())
        task.parameters = TestParameters(task.input_dataset_parameters)

    return update_task


def test_generate_calibrated_data(generate_calibrated_data_task, mocker):
    """
    Given: A GenerateCalibratedData task
    When: Calling the task instance
    Then: Output files are generated for each input file with appropriate tags
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, number_of_frames = generate_calibrated_data_task
    task()
    # Then
    calibrated_frame_paths = list(task.read(tags=[Tag.calibrated(), Tag.frame()]))

    # Verify frames
    assert len(calibrated_frame_paths) == number_of_frames
    for filepath in calibrated_frame_paths:
        assert filepath.exists()

    # Verify debug frame was written
    debug_frame_paths = list(task.read(tags=[Tag.debug(), Tag.frame()]))
    assert len(debug_frame_paths) == 1
    assert debug_frame_paths[0].exists()


class CommonDataset(Spec122Dataset):
    def __init__(self):
        super().__init__(
            array_shape=(1, 10, 10),
            time_delta=1,
            dataset_shape=(2, 10, 10),
            instrument="visp",
            start_time=datetime(2020, 1, 1, 0, 0, 0),
        )

        self.add_constant_key("TELEVATN", 6.28)
        self.add_constant_key("TAZIMUTH", 3.14)
        self.add_constant_key("TTBLANGL", 1.23)
        self.add_constant_key("INST_FOO", "bar")
        self.add_constant_key("DKIST004", "observe")
        self.add_constant_key("ID___005", "ip id")
        self.add_constant_key("PAC__004", "Sapphire Polarizer")
        self.add_constant_key("PAC__005", "31.2")
        self.add_constant_key("PAC__006", "clear")
        self.add_constant_key("PAC__007", "6.66")
        self.add_constant_key("PAC__008", "DarkShutter")
        self.add_constant_key("INSTRUME", "VISP")
        self.add_constant_key("WAVELNTH", 1080.0)
        self.add_constant_key("DATE-OBS", "2020-01-02T00:00:00.000")
        self.add_constant_key("DATE-END", "2020-01-03T00:00:00.000")
        self.add_constant_key("ID___013", "PROPOSAL_ID1")
        self.add_constant_key("PAC__002", "clear")
        self.add_constant_key("PAC__003", "on")
        self.add_constant_key("TELSCAN", "Raster")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)
        self.add_constant_key("BZERO", 0)
        self.add_constant_key("BSCALE", 1)


@pytest.fixture()
def complete_common_header():
    """
    A header with some common by-frame keywords
    """
    # Taken from dkist-processing-common
    ds = CommonDataset()
    header_list = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]

    return header_list[0]


@pytest.fixture(scope="function", params=[1, 4])
def write_l1_task(complete_common_header, request):
    with WriteL1Data(
        recipe_run_id=randint(0, 99999),
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        num_of_stokes_params = request.param
        stokes_params = ["I", "Q", "U", "V"]
        hdu = fits.PrimaryHDU(
            data=np.random.random(size=(1, 128, 128)) * 10, header=complete_common_header
        )
        logger.info(f"{num_of_stokes_params=}")
        hdul = fits.HDUList([hdu])
        for i in range(num_of_stokes_params):
            task.fits_data_write(
                hdu_list=hdul,
                tags=[Tag.calibrated(), Tag.frame(), Tag.stokes(stokes_params[i])],
            )
        task.constants._update(
            asdict(
                FakeConstantDb(
                    AVERAGE_CADENCE=10,
                    MINIMUM_CADENCE=10,
                    MAXIMUM_CADENCE=10,
                    VARIANCE_CADENCE=0,
                    INSTRUMENT="TEST",
                )
            )
        )
        yield task, num_of_stokes_params
        task._purge()


def test_write_l1_task(write_l1_task, mocker):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, num_of_stokes_params = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    logger.info(f"{files=}")
    assert len(files) == num_of_stokes_params
    for file in files:
        logger.info(f"Checking file {file}")
        assert file.exists


@pytest.fixture()
def make_movie_frames_task(tmp_path, recipe_run_id):
    with MakeTestMovieFrames(
        recipe_run_id=recipe_run_id, workflow_name="MakeMovieFrames", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path, recipe_run_id=recipe_run_id)
        task.testing_num_dsps_repeats = 10
        task.num_steps = 1
        task.num_exp_per_step = 1
        task.constants._update(
            asdict(FakeConstantDb(NUM_DSPS_REPEATS=task.testing_num_dsps_repeats))
        )
        ds = S122Headers(
            array_shape=(1, 10, 10),
            num_steps=task.num_steps,
            num_exp_per_step=task.num_exp_per_step,
            num_dsps_repeats=task.testing_num_dsps_repeats,
        )
        header_generator = (d.header() for d in ds)
        for d, header in enumerate(header_generator):
            data = np.ones((10, 10))
            data[: d * 10, :] = 0.0
            hdl = generate_214_l0_fits_frame(data=data, s122_header=header)
            task.fits_data_write(
                hdu_list=hdl,
                tags=[
                    Tag.output(),
                    Tag.dsps_repeat(d + 1),
                ],
            )
        yield task
        task._purge()


def test_make_movie_frames_task(make_movie_frames_task, mocker):
    """
    :Given: a make_movie_frames_task task
    :When: running the task
    :Then: no errors are raised and a movie file is created
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = make_movie_frames_task
    task()
    movie_frames = list(task.read(tags=[Tag.movie_frame()]))
    logger.info(f"{movie_frames=}")
    assert len(movie_frames) == task.testing_num_dsps_repeats
    for frame in movie_frames:
        assert frame.exists()


@pytest.fixture()
def assemble_test_movie_task(tmp_path, recipe_run_id):
    with AssembleTestMovie(
        recipe_run_id=recipe_run_id, workflow_name="AssembleTestMovie", workflow_version="VX.Y"
    ) as task:
        task.scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        task.testing_num_dsps_repeats = 10
        task.num_steps = 1
        task.num_exp_per_step = 1
        task.constants._update(
            asdict(FakeConstantDb(NUM_DSPS_REPEATS=task.testing_num_dsps_repeats))
        )
        ds = S122Headers(
            array_shape=(1, 10, 10),
            num_steps=task.num_steps,
            num_exp_per_step=task.num_exp_per_step,
            num_dsps_repeats=task.testing_num_dsps_repeats,
        )
        header_generator = (d.header() for d in ds)
        for d, header in enumerate(header_generator):
            data = np.ones((10, 10))
            data[: d * 10, :] = 0.0
            hdl = generate_214_l0_fits_frame(data=data, s122_header=header)
            task.fits_data_write(
                hdu_list=hdl,
                tags=[
                    Tag.movie_frame(),
                    Tag.dsps_repeat(d + 1),
                ],
            )
        yield task
        task._purge()


def test_assemble_test_movie_task(assemble_test_movie_task, mocker):
    """
    :Given: an assemble_test_movie task
    :When: running the task
    :Then: no errors are raised and a movie file is created
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = assemble_test_movie_task
    task()
    movie_file = list(task.read(tags=[Tag.movie()]))
    logger.info(f"{movie_file=}")
    assert len(movie_file) == 1
    assert movie_file[0].exists()


@pytest.fixture
def trial_output_task(recipe_run_id, tmp_path, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=FakeGQLClient,
    )
    proposal_id = "test_proposal_id"
    with TransferTestTrialData(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})

        file_count = 0
        # Write a debug frame
        debug_file_obj = uuid4().hex.encode("utf8")
        task.write(debug_file_obj, tags=[Tag.debug(), Tag.frame()])
        file_count += 1

        # Write an intermediate frame that we want to transfer
        intermediate_keep_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_keep_file_obj,
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("DUMMY")],
        )
        file_count += 1

        # Write an intermediate frame that we don't want to transfer
        intermediate_discard_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_discard_file_obj,
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("WHO_CARES")],
        )

        # An output frame
        output_file_obj = uuid4().hex.encode("utf8")
        task.write(output_file_obj, tags=[Tag.output(), Tag.frame()])
        file_count += 1

        # Specifically tagged files
        task.write(uuid4().hex.encode("utf8"), tags=[Tag.frame(), "FOO", "BAR"])
        file_count += 1
        task.write(uuid4().hex.encode("utf8"), tags=[Tag.frame(), "BAZ"])
        file_count += 1

        # This one won't get transferred
        task.write(uuid4().hex.encode("utf8"), tags=[Tag.frame(), "FOO"])

        yield task, file_count
        task._purge()


def test_transfer_test_trial_data(trial_output_task, mocker):
    """
    Given: A TransferTestTrialData task with associated frames
    When: Running the task and building the transfer list
    Then: No errors occur and the transfer list has the correct number of items
    """
    task, expected_num_items = trial_output_task

    mocker.patch(
        "dkist_processing_common.tasks.mixin.globus.GlobusMixin.globus_transfer_scratch_to_object_store"
    )
    mocker.patch(
        "dkist_processing_test.tasks.trial_output_data.TransferTestTrialData.remove_folder_objects"
    )

    # Just make sure the thing runs with no errors
    task()

    transfer_list = task.build_transfer_list()
    assert len(transfer_list) == expected_num_items


@pytest.fixture()
def exercise_numba_task(recipe_run_id):
    with ExerciseNumba(
        recipe_run_id=recipe_run_id, workflow_name="ExerciseNumba", workflow_version="VX.Y"
    ) as task:
        yield task


def test_exercise_numba_task(exercise_numba_task):
    """
    :Given: an exercise_numba task
    :When: running the task
    :Then: the numba module can be loaded and simple method using numba is executed
    """
    original = np.linspace(0.0, 10.0, 1001)
    task = exercise_numba_task
    task()
    assert task.speedup > 1.0
    assert np.all(np.equal(original, task.sorted_array))
