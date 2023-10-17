"""
Fake science task
"""
import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_array_encoder
from dkist_processing_common.codecs.json import json_encoder
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin

from dkist_processing_test.models.parameters import TestParameters


class GenerateCalibratedData(WorkflowTaskBase, FitsDataMixin, InputDatasetMixin):

    record_provenance = True

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        self.parameters = TestParameters(self.input_dataset_parameters)

    def run(self):
        rng = np.random.default_rng()
        with self.apm_task_step("Create debug frame"):
            self.write(
                data=np.arange(10), tags=[Tag.frame(), Tag.debug()], encoder=fits_array_encoder
            )

        with self.apm_task_step("Creating intermediate frame"):
            self.write(
                data=np.arange(5),
                tags=[Tag.frame(), Tag.intermediate(), Tag.task("DUMMY")],
                encoder=fits_array_encoder,
            )

        with self.apm_task_step("Creating unique frames"):
            for _ in range(2):
                self.write(data=np.arange(3), tags=["FOO", "BAR"], encoder=fits_array_encoder)

            self.write(data={"test": "dictionary"}, tags=["BAZ"], encoder=json_encoder)

        with self.apm_task_step("Creating frames that won't be used"):
            self.write(data=b"123", tags=[Tag.intermediate(), Tag.task("NOT_USED"), Tag.frame()])
            self.write(data=b"123", tags=["FOO"])

        with self.apm_task_step("Loop over inputs"):
            count = 1  # keep a running count to increment the dsps repeat number
            for hdu in self.fits_data_read_hdu(tags=Tag.input()):
                header = hdu.header
                with self.apm_processing_step("Doing some calculations"):
                    header["DSPSNUM"] = count
                    data = hdu.data

                    # Just do some weird crap. We don't use the loaded random array directly so that we
                    # don't have to care that the shapes are the same as the "real" data.
                    random_signal = rng.normal(*self.parameters.randomness, size=data.shape)
                    data = (
                        data + random_signal
                    )  # Needs to be like this because data will start as int-type
                    data += self.parameters.constant
                    output_hdu = fits.PrimaryHDU(data=data, header=header)

                with self.apm_writing_step("Writing data"):
                    output_hdul = fits.HDUList([output_hdu])
                    self.fits_data_write(
                        hdu_list=output_hdul,
                        tags=[
                            Tag.calibrated(),
                            Tag.frame(),
                            Tag.stokes("I"),
                            Tag.dsps_repeat(count),
                        ],
                    )
                count += 1
