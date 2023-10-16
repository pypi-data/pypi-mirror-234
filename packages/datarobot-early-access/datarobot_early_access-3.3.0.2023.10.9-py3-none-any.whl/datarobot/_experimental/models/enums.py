#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from enum import Enum


class NotebookPermissions(str, Enum):
    CAN_READ = "CAN_READ"
    CAN_UPDATE = "CAN_UPDATE"
    CAN_DELETE = "CAN_DELETE"
    CAN_SHARE = "CAN_SHARE"
    CAN_COPY = "CAN_COPY"
    CAN_EXECUTE = "CAN_EXECUTE"


class NotebookStatus(str, Enum):
    STOPPING = "stopping"
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    RESTARTING = "restarting"
    DEAD = "dead"
    DELETED = "deleted"


class CategoricalStatsMethods(str, Enum):
    MOST_FREQUENT = "most-frequent"


class NumericStatsMethods(str, Enum):
    MAX = "max"
    MIN = "min"
    AVG = "avg"
    STDDEV = "stddev"
    MEDIAN = "median"


class DataWranglingDialect(str, Enum):
    SNOWFLAKE = "snowflake"


class RecipeInputType(str, Enum):
    DATASOURCE = "datasource"


class DatetimeSamplingStrategy(str, Enum):
    EARLIEST = "earliest"
    LATEST = "latest"


class WranglingOperations(str, Enum):
    """Supported data wrangling operations."""

    COMPUTE_NEW = "compute-new"
    DROP_COLUMNS = "drop-columns"
    RENAME_COLUMNS = "rename-columns"
    FILTER = "filter"

    LAGS = "lags"
    WINDOW_NUMERIC_STATS = "window-numeric-stats"
    TIME_SERIES = "time-series"


class SamplingOperations(str, Enum):
    """Supported data wrangling sampling operations."""

    RANDOM_SAMPLE = "random-sample"
    DATETIME_SAMPLE = "datetime-sample"


class DownsamplingOperations(str, Enum):
    """Supported data wrangling sampling operations."""

    RANDOM_SAMPLE = "random-sample"
    SMART_DOWNSAMPLING = "smart-downsampling"


class DataWranglingDataSourceTypes(str, Enum):
    JDBC = "jdbc"


class FilterOperationFunctions(str, Enum):
    """Operations, supported in FilterOperation."""

    EQUALS = "eq"
    NOT_EQUALS = "neq"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUALS = "lte"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUALS = "gte"
    IS_NULL = "null"
    IS_NOT_NULL = "notnull"
    BETWEEN = "between"
    CONTAINS = "contains"


class ListVectorDatabasesSortQueryParams(str, Enum):
    """supported Sort query params for the Vectordatabase.list method."""

    NAME_ASCENDING = "name"
    NAME_DESCENDING = "-name"
    CREATION_USER_DATE_ASCENDING = "creationUserId"
    CREATION_USER_DATE_DESCENDING = "-creationUserId"
    CREATION_DATE_ASCENDING = "creationDate"
    CREATION_DATE_DESCENDING = "-creationDate"
    EMBEDDING_MODEL_ASCENDING = "embeddingModel"
    EMBEDDING_MODEL_DESCENDING = "-embeddingModel"
    DATASET_ID_ASCENDING = "datasetId"
    DATASET_ID_DESCENDING = "-datasetId"
    CHUNKING_METHOD_ASCENDING = "chunkingMethod"
    CHUNKING_METHOD_DESCENDING = "-chunkingMethod"
    CHUNKS_COUNT_ASCENDING = "chunksCount"
    CHUNKS_COUNT_DESCENDING = "-chunksCount"
    SIZE_ASCENDING = "size"
    SIZE_DESCENDING = "-size"
    USER_NAME_ASCENDING = "userName"
    USER_NAME_DESCENDING = "-userName"
    DATASET_NAME_ASCENDING = "datasetName"
    DATASET_NAME_DESCENDING = "-datasetName"
    PLAYGROUNDS_COUNT_ASCENDING = "playgroundsCount"
    PLAYGROUNDS_COUNT_DESCENDING = "-playgroundsCount"
    SOURCE_ASCENDING = "source"
    SOURCE_DESCENDING = "-source"


class VectorDatabaseEmbeddingModel(str, Enum):
    """Text embedding model names for VectorDatabases."""

    E5_LARGE_V2 = "intfloat/e5-large-v2"
    E5_BASE_V2 = "intfloat/e5-base-v2"
    MULTILINGUAL_E5_BASE = "intfloat/multilingual-e5-base"
    ALL_MINILM_L6_V2 = "sentence-transformers/all-MiniLM-L6-v2"
    JINA_EMBEDDING_T_EN_V1 = "jinaai/jina-embedding-t-en-v1"


class VectorDatabaseChunkingMethod(str, Enum):
    """Text chunking method names for VectorDatabases."""

    RECURSIVE = "recursive"


class VectorDatabaseDatasetLanguages(str, Enum):
    """Dataset languages supported by VectorDatabases."""

    AFRIKAANS = "Afrikaans"
    AMHARIC = "Amharic"
    ARABIC = "Arabic"
    ASSAMESE = "Assamese"
    AZERBAIJANI = "Azerbaijani"
    BELARUSIAN = "Belarusian"
    BULGARIAN = "Bulgarian"
    BENGALI = "Bengali"
    BRETON = "Breton"
    BOSNIAN = "Bosnian"
    CATALAN = "Catalan"
    CZECH = "Czech"
    WELSH = "Welsh"
    DANISH = "Danish"
    GERMAN = "German"
    GREEK = "Greek"
    ENGLISH = "English"
    ESPERANTO = "Esperanto"
    SPANISH = "Spanish"
    ESTONIAN = "Estonian"
    BASQUE = "Basque"
    PERSIAN = "Persian"
    FINNISH = "Finnish"
    FRENCH = "French"
    WESTERN_FRISIAN = "Western Frisian"
    IRISH = "Irish"
    SCOTTISH_GAELIC = "Scottish Gaelic"
    GALICIAN = "Galician"
    GUJARATI = "Gujarati"
    HAUSA = "Hausa"
    HEBREW = "Hebrew"
    HINDI = "Hindi"
    CROATIAN = "Croatian"
    HUNGARIAN = "Hungarian"
    ARMENIAN = "Armenian"
    INDONESIAN = "Indonesian"
    ICELANDIC = "Icelandic"
    ITALIAN = "Italian"
    JAPANESE = "Japanese"
    JAVANESE = "Javanese"
    GEORGIAN = "Georgian"
    KAZAKH = "Kazakh"
    KHMER = "Khmer"
    KANNADA = "Kannada"
    KOREAN = "Korean"
    KURDISH = "Kurdish"
    KYRGYZ = "Kyrgyz"
    LATIN = "Latin"
    LAO = "Lao"
    LITHUANIAN = "Lithuanian"
    LATVIAN = "Latvian"
    MALAGASY = "Malagasy"
    MACEDONIAN = "Macedonian"
    MALAYALAM = "Malayalam"
    MONGOLIAN = "Mongolian"
    MARATHI = "Marathi"
    MALAY = "Malay"
    BURMESE = "Burmese"
    NEPALI = "Nepali"
    DUTCH = "Dutch"
    NORWEGIAN = "Norwegian"
    OROMO = "Oromo"
    ORIYA = "Oriya"
    PANJABI = "Panjabi"
    POLISH = "Polish"
    PASHTO = "Pashto"
    PORTUGUESE = "Portuguese"
    ROMANIAN = "Romanian"
    RUSSIAN = "Russian"
    SANSKRIT = "Sanskrit"
    SINDHI = "Sindhi"
    SINHALA = "Sinhala"
    SLOVAK = "Slovak"
    SLOVENIAN = "Slovenian"
    SOMALI = "Somali"
    ALBANIAN = "Albanian"
    SERBIAN = "Serbian"
    SUNDANESE = "Sundanese"
    SWEDISH = "Swedish"
    SWAHILI = "Swahili"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    THAI = "Thai"
    TAGALOG = "Tagalog"
    TURKISH = "Turkish"
    UYGHUR = "Uyghur"
    UKRAINIAN = "Ukrainian"
    URDU = "Urdu"
    UZBEK = "Uzbek"
    VIETNAMESE = "Vietnamese"
    XHOSA = "Xhosa"
    YIDDISH = "Yiddish"
    CHINESE = "Chinese"

    @classmethod
    def list_all_languages(cls):
        return list(map(lambda c: c.value, cls))  # type: ignore [attr-defined]


class VectorDatabaseChunkingParameterType(str, Enum):
    """Chunking parameter types supported by VectorDatabases."""

    INT = "int"
    LIST_STR = "list[str]"


class VectorDatabaseSource(str, Enum):
    """Supported source for VectorDatabases."""

    LOCAL = "Local"
    EXTERNAL = "External"


class VectorDatabaseExecutionStatus(str, Enum):
    """Execution Statuses VectorDatabases can be in."""

    NEW = "NEW"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class ListPlaygroundsSortQueryParams(str, Enum):
    """supported Sort query params for the Playground.list method."""

    NAME_ASCENDING = "name"
    NAME_DESCENDING = "-name"
    DESCRIPTION_ASCENDING = "description"
    DESCRIPTION_DESCENDING = "-description"
    CREATION_USER_DATE_ASCENDING = "creationUserId"
    CREATION_USER_DATE_DESCENDING = "-creationUserId"
    CREATION_DATE_ASCENDING = "creationDate"
    CREATION_DATE_DESCENDING = "-creationDate"
    LAST_UPDATE_USER_DATE_ASCENDING = "lastUpdateUserId"
    LAST_UPDATE_USER_DATE_DESCENDING = "-lastUpdateUserId"
    SAVED_LLM_BLUEPRINTS_COUNT_ASCENDING = "savedLLMBlueprintsCount"
    SAVED_LLM_BLUEPRINTS_COUNT_DESCENDING = "-savedLLMBlueprintsCount"
