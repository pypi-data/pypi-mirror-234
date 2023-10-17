from datetime import date, datetime
from typing import List, Optional
from pydantic import Field, StringConstraints
import logging
from uuid import UUID

from datadoc_model import Enums
from datadoc_model.BaseModel import DataDocBaseModel
from datadoc_model.LanguageStrings import LanguageStrings
from datadoc_model.LanguageStringsEnum import LanguageStringsEnum
from typing_extensions import Annotated

MODEL_VERSION = "1.0.0"

ALPHANUMERIC_HYPHEN_UNDERSCORE = "[-A-Za-z0-9_.*/]"
URL_FORMAT = "(https?:\/\/)?(www\.)?[a-zA-Z0-9]+([-a-zA-Z0-9.]{1,254}[A-Za-z0-9])?\.[a-zA-Z0-9()]{1,6}([\/][-a-zA-Z0-9_]+)*[\/]?"  # noqa: W605

logger = logging.getLogger(__name__)


class DataDocDataSet(DataDocBaseModel):
    """DataDoc data set. See documentation https://statistics-norway.atlassian.net/l/c/NgjE7yj1"""

    short_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=1, max_length=63, pattern=ALPHANUMERIC_HYPHEN_UNDERSCORE
            ),
        ]
    ] = None
    assessment: Optional[Enums.Assessment] = None
    dataset_status: Optional[Enums.DatasetStatus] = Enums.DatasetStatus.DRAFT
    dataset_state: Optional[Enums.DatasetState] = None
    name: Optional[LanguageStrings] = None
    data_source: Optional[LanguageStrings] = None
    population_description: Optional[LanguageStrings] = None
    version: Optional[str] = None
    version_description: Optional[str] = None
    unit_type: Optional[Enums.UnitType] = None
    temporality_type: Optional[Enums.TemporalityType] = None
    description: Optional[LanguageStrings] = None
    subject_field: Optional[LanguageStrings] = None
    keyword: Optional[List[str]] = None
    spatial_coverage_description: Optional[LanguageStrings] = None
    id: Optional[UUID] = None
    owner: Optional[LanguageStrings] = None
    data_source_path: Optional[str] = None
    metadata_created_date: Optional[datetime] = None
    metadata_created_by: Optional[str] = None
    metadata_last_updated_date: Optional[datetime] = None
    metadata_last_updated_by: Optional[str] = None
    contains_data_from: Optional[date] = None
    contains_data_until: Optional[date] = None


class DataDocVariable(DataDocBaseModel):
    """DataDoc instance variable. See documentation https://statistics-norway.atlassian.net/l/c/goyNhUPP"""

    short_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=1, max_length=63, pattern=ALPHANUMERIC_HYPHEN_UNDERSCORE
            ),
        ]
    ] = None
    name: Optional[LanguageStrings] = None
    data_type: Optional[Enums.Datatype] = None
    variable_role: Optional[Enums.VariableRole] = None
    definition_uri: Optional[
        Annotated[
            str, StringConstraints(min_length=1, max_length=63, pattern=URL_FORMAT)
        ]
    ] = None
    direct_person_identifying: Optional[bool] = None
    data_source: Optional[LanguageStrings] = None
    population_description: Optional[LanguageStrings] = None
    comment: Optional[LanguageStrings] = None
    temporality_type: Optional[Enums.TemporalityType] = None
    # TODO: measurement_unit implemented as string. In the future this should be implemente as a class? See https://www.ssb.no/klass/klassifikasjoner/303/koder
    measurement_unit: Optional[LanguageStrings] = None
    format: Optional[str] = None
    classification_uri: Optional[
        Annotated[
            str, StringConstraints(min_length=1, max_length=63, pattern=URL_FORMAT)
        ]
    ] = None
    sentinel_value_uri: Optional[
        Annotated[
            str, StringConstraints(min_length=1, max_length=63, pattern=URL_FORMAT)
        ]
    ] = None
    invalid_value_description: Optional[LanguageStrings] = None
    id: Optional[Annotated[str, StringConstraints(pattern=URL_FORMAT)]] = None
    contains_data_from: Optional[date] = None
    contains_data_until: Optional[date] = None


class MetadataDocument(DataDocBaseModel):
    """Represents the data structure on file. Includes the dataset metadata from the user as
    well as meta-metadata like the percentage of completed metadata fields and the document version
    """

    percentage_complete: Annotated[int, Field(ge=0, le=100)]
    document_version: str = MODEL_VERSION
    dataset: DataDocDataSet
    variables: List[DataDocVariable]
