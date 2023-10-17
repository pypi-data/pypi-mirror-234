from enum import Enum
from typing import Dict, List, Literal, Optional, Union

import pydantic
from pydantic import BaseModel


class EntityInfo(BaseModel):
    owner: str
    contact_ids: List[str]
    links: List[str]


class CreateElement(BaseModel):
    name: str


class CreateEntity(CreateElement):
    label: str
    description: str


class CreateOutput(CreateEntity):
    output_type: str


class CreateEntityRequest(BaseModel):
    entity: CreateEntity
    entity_info: Optional[EntityInfo]


class UpdateEntityRequest(BaseModel):
    entity: CreateEntity


class FieldMetadata(BaseModel):
    tags: Optional[List[str]]
    description: Optional[str]


class UpdateEntityMetadataRequest(BaseModel):
    fields: Dict[str, FieldMetadata]
    tags: List[str]


class DeleteEntityMetadataRequest(BaseModel):
    fields: Dict[str, FieldMetadata]
    tags: List[str]


class FieldDataType(pydantic.BaseModel):
    meta: Dict[str, str]
    column_type: str


class CreateFieldDefinition(pydantic.BaseModel):
    name: str
    description: Optional[str] = None
    primary: bool = False
    optional: bool = False
    data_type: FieldDataType


class IcebergTableProperties(pydantic.BaseModel):
    table_format: str
    partitioning: Optional[List[str]] = None
    location: Optional[str] = None
    format_version: Optional[int] = None


class StreamingDataProductSchema(pydantic.BaseModel):
    product_type: Literal["streaming"]
    iceberg_table_properties: Optional[IcebergTableProperties] = None

    fields: List[CreateFieldDefinition]


class StoredDataProductSchema(pydantic.BaseModel):
    product_type: Literal["stored"]
    iceberg_table_properties: Optional[IcebergTableProperties] = None

    fields: List[CreateFieldDefinition]


class UpdateDataProductSchema(pydantic.BaseModel):
    details: Union[
        StreamingDataProductSchema,
        StoredDataProductSchema,
    ] = pydantic.Field(discriminator="product_type")


class ExpectationItem(BaseModel):
    expectation_type: str
    kwargs: Dict
    meta: Dict


class ExpectationColumnThresholds(BaseModel):
    accuracy: Optional[float]
    completeness: Optional[float]
    consistency: Optional[float]
    uniqueness: Optional[float]
    validity: Optional[float]


class ExpectationThresholds(BaseModel):
    table: float
    columns: Dict[str, ExpectationColumnThresholds]


class ExpectationWeights(BaseModel):
    accuracy: float
    completeness: float
    consistency: float
    uniqueness: float
    validity: float


class UpdateQualityExpectations(BaseModel):
    custom_details: List[ExpectationItem]
    weights: Optional[ExpectationWeights]
    thresholds: Optional[ExpectationThresholds]


class ClassificationRegexRecognizer(BaseModel):
    name: str
    description: str
    label: str
    patterns: List[str]


class ClassificationRule(BaseModel):
    model: str
    excluded_columns: List[str]
    regex_recognizers: List[ClassificationRegexRecognizer]


class UpdateClassificationResult(BaseModel):
    resolve: List[str]


class BuilderPipeline(BaseModel):
    config: Dict
    inputs: Dict[str, Dict]
    transformations: List
    finalisers: List
    preview: bool = False


class UpdateSparkState(BaseModel):
    state: Dict


class UpdateDataSourceConnection(BaseModel):
    connection: Dict  # TODO: add more details when input parameters will be stable


class UpdateDataSourceConnectionSecret(BaseModel):
    secrets: Dict  # TODO: this type is differ from the type in gateway


class UpdateDataUnitConfiguration(BaseModel):
    configuration: Dict  # TODO: add more details when input parameters will be stable


class UpdateSecret(BaseModel):
    name: str
    data: Dict


class UpdateJournalNote(BaseModel):
    note: str
    owner: str


class SecretKeys(BaseModel):
    keys: List[str]


class TagScope(Enum):
    schema = "SCHEMA"
    field = "FIELD"


class UpdateTag(BaseModel):
    tag: str
    scope: str
