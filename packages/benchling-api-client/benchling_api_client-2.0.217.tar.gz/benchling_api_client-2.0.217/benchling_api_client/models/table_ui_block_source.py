from typing import Union

from ..extensions import UnknownType
from ..models.table_ui_block_dataset_source import TableUiBlockDatasetSource

TableUiBlockSource = Union[TableUiBlockDatasetSource, UnknownType]
