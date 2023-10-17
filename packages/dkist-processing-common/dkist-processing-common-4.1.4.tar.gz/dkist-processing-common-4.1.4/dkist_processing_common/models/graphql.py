"""GraphQL Data models for the metadata store api."""
from dataclasses import dataclass


@dataclass
class RecipeRunMutation:
    """Recipe run mutation record."""

    recipeRunId: int
    recipeRunStatusId: int


@dataclass
class RecipeRunStatusQuery:
    """Recipe run status query for the recipeRunStatuses endpoint."""

    recipeRunStatusName: str


@dataclass
class RecipeRunStatusMutation:
    """Recipe run status mutation record."""

    recipeRunStatusName: str
    isComplete: bool
    recipeRunStatusDescription: str


@dataclass
class RecipeRunStatusResponse:
    """Response to a recipe run status query."""

    recipeRunStatusId: int


@dataclass
class InputDatasetPartTypeResponse:
    """Response class for the input dataset part type entity."""

    inputDatasetPartTypeName: str


@dataclass
class InputDatasetPartResponse:
    """Response class for the input dataset part entity."""

    inputDatasetPartId: int
    inputDatasetPartDocument: str
    inputDatasetPartType: InputDatasetPartTypeResponse


@dataclass
class InputDatasetInputDatasetPartResponse:
    """Response class for the join entity between input datasets and input dataset parts."""

    inputDatasetPart: InputDatasetPartResponse


@dataclass
class InputDatasetResponse:
    """Input dataset query response."""

    inputDatasetId: int
    isActive: bool
    inputDatasetInputDatasetParts: list[InputDatasetInputDatasetPartResponse]


@dataclass
class RecipeInstanceResponse:
    """Recipe instance query response."""

    inputDataset: InputDatasetResponse
    recipeId: int


@dataclass
class RecipeRunResponse:
    """Recipe run query response."""

    recipeInstance: RecipeInstanceResponse
    recipeInstanceId: int
    configuration: str = None


@dataclass
class RecipeRunMutationResponse:
    """Recipe run mutation response."""

    recipeRunId: int


@dataclass
class RecipeRunQuery:
    """Query parameters for the metadata store endpoint recipeRuns."""

    recipeRunId: int


@dataclass
class DatasetCatalogReceiptAccountMutation:
    """
    Dataset catalog receipt account mutation record.

    It sets an expected object count for a dataset so that dataset inventory creation
    doesn't happen until all objects are transferred and inventoried.
    """

    datasetId: str
    expectedObjectCount: int


@dataclass
class DatasetCatalogReceiptAccountResponse:
    """Dataset catalog receipt account response for query and mutation endpoints."""

    datasetCatalogReceiptAccountId: int


@dataclass
class RecipeRunProvenanceMutation:
    """Recipe run provenance mutation record."""

    inputDatasetId: int
    isTaskManual: bool
    recipeRunId: int
    taskName: str
    libraryVersions: str
    workflowVersion: str
    codeVersion: str = None


@dataclass
class RecipeRunProvenanceResponse:
    """Response for the metadata store recipeRunProvenances and mutations endpoints."""

    recipeRunProvenanceId: int


@dataclass
class QualityReportMutation:
    """Quality report mutation record."""

    datasetId: str
    qualityReport: str  # JSON


@dataclass
class QualityReportQuery:
    """Query parameters for the metadata store endpoint qualityReports."""

    datasetId: str


@dataclass
class QualityReportResponse:
    """Query Response for the metadata store endpoint qualityReports."""

    qualityReportId: int
