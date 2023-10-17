"""
Workflow which exercises the common tasks in an end to end scenario
"""
from dkist_processing_common.tasks import AddDatasetReceiptAccount
from dkist_processing_common.tasks import PublishCatalogAndQualityMessages
from dkist_processing_common.tasks import QualityL1Metrics
from dkist_processing_common.tasks import Teardown
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TransferL1Data
from dkist_processing_common.tasks import TrialTeardown
from dkist_processing_core import Workflow

from dkist_processing_test.tasks.fake_science import GenerateCalibratedData
from dkist_processing_test.tasks.movie import AssembleTestMovie
from dkist_processing_test.tasks.movie import MakeTestMovieFrames
from dkist_processing_test.tasks.parse import ParseL0TestInputData
from dkist_processing_test.tasks.quality import TestQualityL0Metrics
from dkist_processing_test.tasks.quality import TestSubmitQuality
from dkist_processing_test.tasks.trial_output_data import TransferTestTrialData
from dkist_processing_test.tasks.write_l1 import WriteL1Data

# TransferInputData Task
transfer_input_data = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="transfer-input-data",
    workflow_package=__package__,
)
transfer_input_data.add_node(task=TransferL0Data, upstreams=None)

# ParseInputData Task
parse_input_data = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="parse-input-data",
    workflow_package=__package__,
)
parse_input_data.add_node(task=ParseL0TestInputData, upstreams=None)

# L0Quality Task
quality_l0_metrics = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="quality-l0-metrics",
    workflow_package=__package__,
)
quality_l0_metrics.add_node(task=TestQualityL0Metrics, upstreams=None)

# L1Quality Task
quality_l1_metrics = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="quality-l1-metrics",
    workflow_package=__package__,
)
quality_l1_metrics.add_node(task=QualityL1Metrics, upstreams=None)

# SubmitQuality Task
quality_submit_metrics = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="quality-submit-metrics",
    workflow_package=__package__,
)
quality_submit_metrics.add_node(task=TestSubmitQuality, upstreams=None)

# GenerateL1CalibratedData Task
generate_calibrated_data = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="generate-calibrated-data",
    workflow_package=__package__,
)
generate_calibrated_data.add_node(task=GenerateCalibratedData, upstreams=None)

# MakeTestMovieFrames task
make_test_movie_frames = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="make-test-movie-frames",
    workflow_package=__package__,
)
make_test_movie_frames.add_node(task=MakeTestMovieFrames, upstreams=None)

# AssembleTestMovie Task
assemble_test_movie = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="assemble-test-movie",
    workflow_package=__package__,
)
assemble_test_movie.add_node(task=AssembleTestMovie, upstreams=None)

# WriteL1 Task
write_l1 = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="write-l1",
    workflow_package=__package__,
)
write_l1.add_node(task=WriteL1Data, upstreams=None)

# TransferOutputData Task
transfer_output_data = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="transfer-output-data",
    workflow_package=__package__,
)
transfer_output_data.add_node(task=TransferL1Data, upstreams=None)

# TransferTrialData Task
transfer_trial_data = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="transfer-trial-data",
    workflow_package=__package__,
)
transfer_trial_data.add_node(task=TransferTestTrialData, upstreams=None)

# AddDatasetReceiptAccount Task
add_dataset_receipt_account = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="add-dataset-receipt-account",
    workflow_package=__package__,
)
add_dataset_receipt_account.add_node(task=AddDatasetReceiptAccount, upstreams=None)

# PublishCatalogMessages Task
publish_catalog_messages = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="publish-messages",
    workflow_package=__package__,
)
publish_catalog_messages.add_node(task=PublishCatalogAndQualityMessages, upstreams=None)

# Teardown Task
teardown = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="teardown",
    workflow_package=__package__,
)
teardown.add_node(task=Teardown, upstreams=None)

# Trial Teardown Task
trial_teardown = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="trial-teardown",
    workflow_package=__package__,
)
trial_teardown.add_node(task=TrialTeardown, upstreams=None)
