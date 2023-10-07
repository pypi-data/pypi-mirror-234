from logging import Logger
from typing import ClassVar, List, Type

from great_expectations.datasource.fluent.file_path_data_asset import _FilePathDataAsset
from great_expectations.datasource.fluent.interfaces import DataAsset as DataAsset
from great_expectations.datasource.fluent.pandas_datasource import _PandasDatasource

logger: Logger

class CSVAsset(_FilePathDataAsset): ...
class ExcelAsset(_FilePathDataAsset): ...
class JSONAsset(_FilePathDataAsset): ...
class ORCAsset(_FilePathDataAsset): ...
class ParquetAsset(_FilePathDataAsset): ...
class FeatherAsset(_FilePathDataAsset): ...
class FWFAsset(_FilePathDataAsset): ...
class HDFAsset(_FilePathDataAsset): ...
class HTMLAsset(_FilePathDataAsset): ...
class PickleAsset(_FilePathDataAsset): ...
class SASAsset(_FilePathDataAsset): ...
class SPSSAsset(_FilePathDataAsset): ...
class StataAsset(_FilePathDataAsset): ...
class XMLAsset(_FilePathDataAsset): ...

class _PandasFilePathDatasource(_PandasDatasource):
    asset_types: ClassVar[List[Type[DataAsset]]]
    assets: List[_FilePathDataAsset]
