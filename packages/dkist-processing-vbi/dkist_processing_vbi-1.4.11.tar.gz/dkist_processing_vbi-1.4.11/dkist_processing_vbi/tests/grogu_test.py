import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_header_validator import spec214_validator
from dkist_processing_common.manual import ManualProcessing
from dkist_processing_common.tasks import QualityL1Metrics
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from dkist_processing_common.tasks.mixin.metadata_store import MetadataStoreMixin
from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_service_configuration import logger

from dkist_processing_vbi.models.tags import VbiTag
from dkist_processing_vbi.parsers.vbi_l0_fits_access import VbiL0FitsAccess
from dkist_processing_vbi.tasks.assemble_movie import AssembleVbiMovie
from dkist_processing_vbi.tasks.dark import DarkCalibration
from dkist_processing_vbi.tasks.gain import GainCalibration
from dkist_processing_vbi.tasks.make_movie_frames import MakeVbiMovieFrames
from dkist_processing_vbi.tasks.parse import ParseL0VbiInputData
from dkist_processing_vbi.tasks.process_summit_processed import GenerateL1SummitData
from dkist_processing_vbi.tasks.quality_metrics import VbiQualityL0Metrics
from dkist_processing_vbi.tasks.quality_metrics import VbiQualityL1Metrics
from dkist_processing_vbi.tasks.science import ScienceCalibration
from dkist_processing_vbi.tasks.vbi_base import VbiTaskBase
from dkist_processing_vbi.tasks.write_l1 import VbiWriteL1Frame

INV = False
try:
    from dkist_inventory.asdf_generator import dataset_from_fits

    INV = True
except ModuleNotFoundError:
    # Bitbucket pipelines won't have dkist-inventory installed
    logger.warning("Could not load dkist-inventory. This is OK on Bitbucket.")
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


def tag_inputs_task(suffix: str):
    class TagInputs(WorkflowTaskBase):
        def run(self) -> None:
            logger.info(f"Looking in {os.path.abspath(self.scratch.workflow_base_path)}")
            for file in self.scratch.workflow_base_path.glob(f"*.{suffix}"):
                logger.info(f"Found {file}")
                self.tag(path=file, tags=[VbiTag.input(), VbiTag.frame()])

    return TagInputs


def translate_task(summit_processed: bool = False):
    class Translate122To214L0(WorkflowTaskBase):
        def run(self) -> None:
            raw_dir = Path(self.scratch.scratch_base_path) / f"VBI{self.recipe_run_id:03n}"
            if not os.path.exists(self.scratch.workflow_base_path):
                os.makedirs(self.scratch.workflow_base_path)
            for file in raw_dir.glob("*.FITS"):
                translated_file_name = Path(self.scratch.workflow_base_path) / os.path.basename(
                    file
                )
                logger.info(f"Translating and compressing {file} -> {translated_file_name}")
                hdl = fits.open(file)
                data = hdl[0].data
                if summit_processed:
                    data = data.astype(np.float32)
                header = spec122_validator.validate_and_translate_to_214_l0(
                    hdl[0].header, return_type=fits.HDUList
                )[0].header
                trans_hdl = fits.HDUList(
                    [fits.PrimaryHDU(), fits.CompImageHDU(data=data, header=header)]
                )

                trans_hdl.writeto(translated_file_name, overwrite=True)
                hdl.close()
                trans_hdl.close()
                del hdl, trans_hdl

    return Translate122To214L0


class ShowExposureTimes(VbiTaskBase):
    def run(self) -> None:
        logger.info(f"{self.constants.dark_exposure_times = }")
        logger.info(f"{self.constants.gain_exposure_times = }")
        logger.info(f"{self.constants.observe_exposure_times = }")


class ExposeOutputData(VbiTaskBase, FitsDataMixin):
    def run(self) -> None:
        for step in range(self.constants.num_spatial_steps):
            output_access_list = list(
                self.fits_data_read_fits_access(
                    tags=[VbiTag.output(), VbiTag.frame(), VbiTag.spatial_step(step)],
                    cls=VbiL0FitsAccess,
                )
            )
            logger.info(f"found {len(output_access_list)} outputs for step {step}")
            fits.PrimaryHDU(output_access_list[0].data).writeto(f"comp_{step}.FITS", overwrite=True)


class SubmitAndExposeQuality(WorkflowTaskBase, QualityMixin, MetadataStoreMixin):
    """A direct copy paste of SumbitQuality with an additional step of writing the report to disk"""

    def run(self):
        with self.apm_processing_step("Building quality report"):
            logger.info("Building quality report")
            report_str = self.quality_build_report()

        with self.apm_task_step("Submitting quality report"):
            logger.info("Submitting quality report")
            self.metadata_store_add_quality_report(
                dataset_id=self.constants.dataset_id, quality_report=report_str
            )

        if QRM:
            doc_path = self.scratch.workflow_base_path / "quality_report.json"
            report_container = {
                "datasetId": self.constants.dataset_id,
                "qualityReport": json.dumps(report_str, cls=DatetimeEncoder),
            }
            json_str = json.dumps(report_container)
            with open(doc_path, "w") as f:
                f.write(json_str)
            logger.info(f"Wrote report to {doc_path}")


class ValidateL1Output(VbiTaskBase):
    def run(self) -> None:
        files = self.read(tags=[VbiTag.output(), VbiTag.frame()])
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


def compare_to_sv_data(sv_file_name: str) -> bool:

    sv_hdl = fits.open(sv_file_name)
    for i, sv_h in enumerate(sv_hdl[1:]):
        dc_data = fits.open(f"comp_{i}.FITS")[0].data
        if not np.allclose(sv_h.data[0], dc_data, atol=1e-5, rtol=1e-5):
            return False

    return True


def l0_pipeline_workflow(manual_processing_run: ManualProcessing) -> None:
    manual_processing_run.run_task(task=ShowExposureTimes)
    manual_processing_run.run_task(task=VbiQualityL0Metrics)
    manual_processing_run.run_task(task=DarkCalibration)
    manual_processing_run.run_task(task=GainCalibration)
    manual_processing_run.run_task(task=ScienceCalibration)


def summit_data_processing_workflow(manual_processing_run: ManualProcessing) -> None:
    manual_processing_run.run_task(task=GenerateL1SummitData)


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


def make_dataset_asdf(scratch_path, recipe_run_id):
    if not INV:
        logger.warning("Did NOT make dataset asdf file because dkist_inventory is not installed")
        return

    output_dir = os.path.join(scratch_path, str(recipe_run_id))
    asdf_name = f"dataset_{recipe_run_id:03n}.asdf"
    logger.info(f"Creating ASDF file from {output_dir} and saving to {asdf_name}")
    dataset_from_fits(output_dir, asdf_name, hdu=1)


def main(
    scratch_path="/media/FastPipelin/vbi/scratch",
    recipe_run_id=4,
    suffix: str = "FITS",
    sv_file_to_test: str | None = None,
    skip_translation: bool = False,
    skip_movie: bool = False,
    only_translate: bool = False,
    science_workflow_name: str = "l0_processing",
    use_apm: bool = False,
):
    if use_apm:
        setup_APM_config()
    science_func_dict = {
        "l0_pipeline": l0_pipeline_workflow,
        "summit_data_processed": summit_data_processing_workflow,
    }
    science_workflow = science_func_dict[science_workflow_name]
    with ManualProcessing(
        workflow_path=scratch_path,
        recipe_run_id=recipe_run_id,
        testing=True,
        workflow_name=f"vbi-{science_workflow_name}",
        workflow_version="GROGU",
    ) as manual_processing_run:
        if not skip_translation:
            manual_processing_run.run_task(
                task=translate_task(
                    summit_processed=science_workflow_name == "summit_data_processed"
                )
            )
        if only_translate:
            return
        manual_processing_run.run_task(task=tag_inputs_task(suffix))
        manual_processing_run.run_task(task=ParseL0VbiInputData)
        science_workflow(manual_processing_run)
        manual_processing_run.run_task(task=VbiWriteL1Frame)
        manual_processing_run.run_task(task=QualityL1Metrics)
        manual_processing_run.run_task(task=VbiQualityL1Metrics)
        manual_processing_run.run_task(task=SubmitAndExposeQuality)
        manual_processing_run.run_task(task=ValidateL1Output)

        # Put this here because the movie stuff takes a long time
        make_dataset_asdf(scratch_path, recipe_run_id)
        make_pdf_report(scratch_path, recipe_run_id)

        if not skip_movie:
            manual_processing_run.run_task(task=MakeVbiMovieFrames)
            manual_processing_run.run_task(task=AssembleVbiMovie)

        manual_processing_run.count_provenance()

        if sv_file_to_test:
            manual_processing_run.run_task(task=ExposeOutputData)
            assert compare_to_sv_data(sv_file_to_test)
            logger.info("DC output matches SV output!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run an end-to-end test of the VBI DC Science pipeline"
    )
    parser.add_argument("scratch_path", help="Location to use as the DC 'scratch' disk")
    parser.add_argument("--suffix", help="File suffix to treat as INPUT frames", default="FITS")
    parser.add_argument(
        "-W",
        "--workflow_name",
        help="Name of VBI workflow to test",
        choices=["l0_pipeline", "summit_data_processed"],
        default="l0_pipeline",
    )
    parser.add_argument(
        "-i",
        "--run-id",
        help="Which subdir to use. This will become the recipe run id",
        type=int,
        default=4,
    )
    parser.add_argument(
        "-S",
        "--sv-file-to-test",
        help="If given, the result of the DC pipeline will be checked against this file on a pixel-by-pixel basis",
        type=str,
    )
    parser.add_argument(
        "-T",
        "--skip-translation",
        help="Skip the translation of raw 122 l0 frames to 214 l0",
        action="store_true",
    )
    parser.add_argument(
        "-t", "--only-translate", help="Do ONLY the translation step", action="store_true"
    )
    parser.add_argument("-M", "--skip-movie", help="Skip making output movie", action="store_true")
    parser.add_argument("-A", "--use-apm", help="Send APM spans to SIM", action="store_true")
    args = parser.parse_args()

    sys.exit(
        main(
            scratch_path=args.scratch_path,
            recipe_run_id=args.run_id,
            suffix=args.suffix,
            sv_file_to_test=args.sv_file_to_test,
            skip_translation=args.skip_translation,
            only_translate=args.only_translate,
            skip_movie=args.skip_movie,
            science_workflow_name=args.workflow_name,
            use_apm=args.use_apm,
        )
    )
