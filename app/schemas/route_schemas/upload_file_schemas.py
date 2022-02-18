from pydantic import BaseModel, Json
from typing import List, Dict, Optional
from fastapi import UploadFile, File

from sqlalchemy.sql.expression import false
from schemas.message_schemas import DefaultMessageSchema
from schemas.model_schemas import file_column_schema


# upload_file

    
class MappingData(BaseModel):
    file_columns_names: List[str]
    file_schema_columns: List[file_column_schema.FileColumnSchema]
    match_columns: Dict[str, file_column_schema.FileColumnSchema]


class UploadOutData(BaseModel):
    mapping_data: MappingData
    imported_file_id: int
    sample: Json


class UploadOut(DefaultMessageSchema):
    data: UploadOutData


# map_columns
class MapColumnsSchema(BaseModel):
    file_column_name: str
    file_schema_column_id: int
    default_value: Optional[str] = ''


class FileExtraColumnsSchema(BaseModel):
    file_column_name: str
    default_value: Optional[str] = ''


class SchemaExtraColumnsSchema(BaseModel):
    schema_column_id: int
    default_value: Optional[str] = ''


class MapColumnsIn(BaseModel):
    map_columns: List[MapColumnsSchema]
    file_extra_columns: List[FileExtraColumnsSchema]
    schema_extra_columns: List[SchemaExtraColumnsSchema]


class MapColumnsOutData(BaseModel):
    meta_insights: Dict[str, int]


class MapColumnsOut(DefaultMessageSchema):
    data: MapColumnsOutData


# abort_upload
class AbortUploadIn(BaseModel):
    pass


# commit_upload
class CommitUploadIn(BaseModel):
    pass


# Tags
class TagsOut(BaseModel):
    message: str
    tags: List[str]