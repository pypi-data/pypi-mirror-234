from typing import Tuple

from sqlalchemy import Table

from .conversion_common_json import JsonRecordExtractorDict, get_json_column_extractor
from .conversion_common_tsv import get_tsv_column_extractor


def create_upsert_converters(table_def: Table) -> JsonRecordExtractorDict:
    # create a tuple of converter objects for each column for UPSERT records
    return {col.name: get_json_column_extractor(col) for col in table_def.columns}


def create_delete_converters(table_def: Table) -> JsonRecordExtractorDict:
    # create a tuple of converter objects for each column for DELETE records
    return {col.name: get_json_column_extractor(col) for col in table_def.primary_key}


# TODO: this function is to be used when full TSV support is enabled on the backend.
def disabled_create_copy_converters(table_def: Table) -> Tuple:
    all_columns = [col.name for col in table_def.columns]
    key_indices = [all_columns.index(col.name) for col in table_def.primary_key]

    return tuple(
        get_tsv_column_extractor(key_indices, column_index, column)
        for column_index, column in enumerate(table_def.columns)
    )


def create_copy_converters(table_def: Table) -> Tuple:
    return tuple(get_json_column_extractor(col) for col in table_def.columns)
