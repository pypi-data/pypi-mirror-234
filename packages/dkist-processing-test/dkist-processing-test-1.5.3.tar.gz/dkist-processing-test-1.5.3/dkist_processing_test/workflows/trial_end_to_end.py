"""
Workflow which exercises the common tasks end to end in a trial scenario
"""
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TrialTeardown
from dkist_processing_core import Workflow

from dkist_processing_test.tasks.fake_science import GenerateCalibratedData
from dkist_processing_test.tasks.parse import ParseL0TestInputData
from dkist_processing_test.tasks.quality import TestQualityL0Metrics
from dkist_processing_test.tasks.trial_output_data import TransferTestTrialData
from dkist_processing_test.tasks.write_l1 import WriteL1Data

trial = Workflow(
    input_data="input",
    output_data="output",
    category="test",
    detail="trial-e2e",
    workflow_package=__package__,
)
trial.add_node(task=TransferL0Data, upstreams=None)
trial.add_node(task=ParseL0TestInputData, upstreams=TransferL0Data)
trial.add_node(task=TestQualityL0Metrics, upstreams=ParseL0TestInputData)
trial.add_node(task=GenerateCalibratedData, upstreams=TestQualityL0Metrics)
trial.add_node(task=WriteL1Data, upstreams=GenerateCalibratedData)
trial.add_node(task=TransferTestTrialData, upstreams=WriteL1Data)
trial.add_node(task=TrialTeardown, upstreams=TransferTestTrialData)
