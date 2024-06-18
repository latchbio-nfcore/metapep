from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: typing.Optional[LatchFile], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], ncbi_key: typing.Optional[str], ncbi_email: typing.Optional[str], show_supported_models: typing.Optional[bool], hide_pvalue: typing.Optional[bool], min_pep_len: typing.Optional[int], max_pep_len: typing.Optional[int], pred_method: typing.Optional[str], prodigal_mode: typing.Optional[str], prediction_chunk_size: typing.Optional[int], downstream_chunk_size: typing.Optional[int], max_task_num: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('multiqc_methods_description', multiqc_methods_description),
                *get_flag('ncbi_key', ncbi_key),
                *get_flag('ncbi_email', ncbi_email),
                *get_flag('min_pep_len', min_pep_len),
                *get_flag('max_pep_len', max_pep_len),
                *get_flag('pred_method', pred_method),
                *get_flag('show_supported_models', show_supported_models),
                *get_flag('prodigal_mode', prodigal_mode),
                *get_flag('prediction_chunk_size', prediction_chunk_size),
                *get_flag('downstream_chunk_size', downstream_chunk_size),
                *get_flag('max_task_num', max_task_num),
                *get_flag('hide_pvalue', hide_pvalue)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_metapep", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_metapep(input: typing.Optional[LatchFile], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], ncbi_key: typing.Optional[str], ncbi_email: typing.Optional[str], show_supported_models: typing.Optional[bool], hide_pvalue: typing.Optional[bool], min_pep_len: typing.Optional[int] = 9, max_pep_len: typing.Optional[int] = 11, pred_method: typing.Optional[str] = 'syfpeithi', prodigal_mode: typing.Optional[str] = 'meta', prediction_chunk_size: typing.Optional[int] = 4000000, downstream_chunk_size: typing.Optional[int] = 7500000, max_task_num: typing.Optional[int] = 1000) -> None:
    """
    nf-core/metapep

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, multiqc_methods_description=multiqc_methods_description, ncbi_key=ncbi_key, ncbi_email=ncbi_email, min_pep_len=min_pep_len, max_pep_len=max_pep_len, pred_method=pred_method, show_supported_models=show_supported_models, prodigal_mode=prodigal_mode, prediction_chunk_size=prediction_chunk_size, downstream_chunk_size=downstream_chunk_size, max_task_num=max_task_num, hide_pvalue=hide_pvalue)

