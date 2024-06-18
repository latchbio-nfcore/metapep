
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
    'ncbi_key': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Pipeline options',
        description='Required for downloading proteins from ncbi.',
    ),
    'ncbi_email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Required for downloading proteins from ncbi.',
    ),
    'min_pep_len': NextflowParameter(
        type=typing.Optional[int],
        default=9,
        section_title=None,
        description='Minimum length of produced peptides.',
    ),
    'max_pep_len': NextflowParameter(
        type=typing.Optional[int],
        default=11,
        section_title=None,
        description='Maximum length of produced peptides.',
    ),
    'pred_method': NextflowParameter(
        type=typing.Optional[str],
        default='syfpeithi',
        section_title=None,
        description='Epitope prediction method to use',
    ),
    'show_supported_models': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Display supported alleles of all prediction methods and exit.',
    ),
    'prodigal_mode': NextflowParameter(
        type=typing.Optional[str],
        default='meta',
        section_title=None,
        description="Prodigal mode, 'meta' or 'single'.",
    ),
    'prediction_chunk_size': NextflowParameter(
        type=typing.Optional[int],
        default=4000000,
        section_title=None,
        description='Maximum chunk size (#peptides) for epitope prediction jobs.',
    ),
    'downstream_chunk_size': NextflowParameter(
        type=typing.Optional[int],
        default=7500000,
        section_title=None,
        description='Maximum chunk size (#epitope predictions) for processing of downstream visualisations.',
    ),
    'max_task_num': NextflowParameter(
        type=typing.Optional[int],
        default=1000,
        section_title=None,
        description='Maximum number of tasks submitted by `PREDICT_EPITOPES` process',
    ),
    'hide_pvalue': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Do not display mean comparison p-values in boxplots.',
    ),
}

