"""Repackage VBI data already calibrated before receipt at the Data Center."""
from astropy.io import fits
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin

from dkist_processing_vbi.models.tags import VbiTag
from dkist_processing_vbi.tasks.vbi_base import VbiTaskBase


class GenerateL1SummitData(VbiTaskBase, FitsDataMixin):
    """
    Task class for updating the headers of on-summit processed VBI data.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    record_provenance = True

    def run(self) -> None:
        """
        For all input frames.

            - Add data-dependent SPEC-0214 headers
            - Write out
        """
        # This loop is how we ensure that only completed mosaics get processed.
        with self.apm_task_step("Re-tagging INPUT observe frames as CALIBRATED"):
            for mosaic in range(1, self.constants.num_mosaic_repeats + 1):
                for file_name in self.read(
                    tags=[
                        VbiTag.input(),
                        VbiTag.frame(),
                        VbiTag.task("Observe"),
                        VbiTag.mosaic(mosaic),
                    ]
                ):
                    old_tags = self.tags(file_name)
                    old_tags.remove(VbiTag.input())

                    # We use `fits` directly because opening the file with VbiL0FitsAccess would require re-compressing
                    # the CompImageHDU on write. Doing it this way allows us to modify the header only.
                    hdul = fits.open(file_name)
                    hdul[1].header["VBINMOSC"] = self.constants.num_mosaic_repeats
                    hdul[1].header["VBICMOSC"] = mosaic

                    new_tags = old_tags + [VbiTag.calibrated(), VbiTag.stokes("I")]
                    self.fits_data_write(hdu_list=hdul, tags=new_tags)
