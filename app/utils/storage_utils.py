from core.config import settings
import pandas as pd
import os
from pandas import DataFrame
from utils import aws_utils
from boto3.session import Session
import awswrangler as wr
from utils import import_tool_utils
from models.import_tool import ImportedFile
from typing import Tuple

my_aws_session: Session = aws_utils.get_aws_session()


def review_local_dirs():
    LOCAL_IMPORT_TOOL_PATH: str = settings.LOCAL_IMPORT_TOOL_PATH
    LOCAL_IMPORT_TOOL_PENDING_PATH: str = os.path.join(LOCAL_IMPORT_TOOL_PATH, 'pending')
    LOCAL_IMPORT_TOOL_PENDING_BASE_PATH: str = os.path.join(LOCAL_IMPORT_TOOL_PENDING_PATH, 'base')
    LOCAL_IMPORT_TOOL_TEMP_PATH: str = os.path.join(LOCAL_IMPORT_TOOL_PATH, 'temp')

    if not os.path.isdir(LOCAL_IMPORT_TOOL_PATH):
        os.mkdir(LOCAL_IMPORT_TOOL_PATH)

    if not os.path.isdir(LOCAL_IMPORT_TOOL_PENDING_PATH):
        os.mkdir(LOCAL_IMPORT_TOOL_PENDING_PATH)

    if not os.path.isdir(LOCAL_IMPORT_TOOL_PENDING_BASE_PATH):
        os.mkdir(LOCAL_IMPORT_TOOL_PENDING_BASE_PATH)

    if not os.path.isdir(LOCAL_IMPORT_TOOL_TEMP_PATH):
        os.mkdir(LOCAL_IMPORT_TOOL_TEMP_PATH)


def join_path(main_path: str, path: str):
    if settings.REMOTE_STORAGE:
        return f'{main_path}/{path}'
    else:
        return os.path.join(main_path, path)


# Paths
def IMPORT_TOOL_PENDING_PATH() -> str:
    if settings.REMOTE_STORAGE:
        return join_path(settings.STORAGE_S3_PATH, 'pending')
    else:
        return join_path(settings.LOCAL_IMPORT_TOOL_PATH, 'pending')


def IMPORT_TOOL_BASE_PENDING_PATH() -> str:
    return join_path(IMPORT_TOOL_PENDING_PATH(), 'base')


def complete_pending_path_file(file_name: str, file_directory_name: str) -> Tuple[str,str]:
    directory_path = join_path(IMPORT_TOOL_PENDING_PATH(), file_directory_name)
    file_path = join_path(directory_path, file_name)
    return directory_path, file_path


def complete_pending_base_path_file(file_name: str) -> str:
    return join_path(IMPORT_TOOL_BASE_PENDING_PATH(), file_name)


def temp_write_path(file_name: str) -> str:
    return join_path(settings.LOCAL_IMPORT_TOOL_TEMP_PATH, file_name)


def send_file_path(file_name: str, target_folder_name: str) -> Tuple[str,str]:
    target_dir = f'{settings.STORAGE_S3_PATH}/input/{target_folder_name}'
    target_path = f'{target_dir}/{file_name}'
    return target_dir, target_path


def tag_file_path(file_name: str, target_folder_name: str, target_tag_folder_name: str) -> Tuple[str,str]:
    target_dir, _ = send_file_path(file_name, target_folder_name)
    target_dir = f'{target_dir}/tags/{target_tag_folder_name}'
    target_path = f'{target_dir}/{file_name}'
    return target_dir, target_path


# Actions
# -Pandas
def read_df_csv(file_path: str,every_thing_as_str = True) -> DataFrame:
    if settings.REMOTE_STORAGE:
        if every_thing_as_str:
            df = wr.s3.read_csv(file_path, sep='|', index_col='row_id', dtype=str, boto3_session=my_aws_session)
        else:
            df = wr.s3.read_csv(file_path, sep='|', index_col='row_id', boto3_session=my_aws_session)
    else:
        if every_thing_as_str:
            df = pd.read_csv(file_path, sep='|', index_col='row_id', dtype=str)
        else:
            df = pd.read_csv(file_path, sep='|', index_col='row_id')
    return df


def save_df(df: DataFrame, file_path: str):
    if settings.REMOTE_STORAGE:
        wr.s3.to_csv(df, file_path, sep='|', index_label='row_id', boto3_session=my_aws_session)
    else:
        df.to_csv(file_path, sep='|', index_label='row_id')


# remove
def remove_file(file_path: str):
    if settings.REMOTE_STORAGE:
        wr.s3.delete_objects(file_path, boto3_session=my_aws_session)
    else:
        os.remove(file_path)


def exist_file(file_path: str) -> bool:
    if settings.REMOTE_STORAGE:
        return wr.s3.does_object_exist(file_path, boto3_session=my_aws_session)
    else:
        return os.path.exists(file_path)


# send file
def send_file(source_path: str, file_name: str, target_folder_name: str):
    target_dir, target_path = send_file_path(file_name, target_folder_name)
    if settings.REMOTE_STORAGE:
        source_dir = IMPORT_TOOL_PENDING_PATH()
        wr.s3.copy_objects(paths=[source_path], source_path=source_dir, target_path=target_dir,
                           boto3_session=my_aws_session)
    else:
        wr.s3.upload(local_file=source_path, path=target_path, boto3_session=my_aws_session)
    remove_file(source_path)


def send_filter_file(df_file: DataFrame, source_path: str, file_name: str, target_folder_name: str):
    df_file_final = df_file.copy(deep=True)
    for flag_category, filters in import_tool_utils.meta_columns_filter_dictionary.items():
        _, target_path = tag_file_path(file_name, target_folder_name, flag_category)
        df_filtered, df_filter = import_tool_utils.filter_by_action_rows_or(df_file, filters)
        save_df(df_filtered, target_path)
        df_file_final = df_file_final[~df_filter]

    _, target_path = send_file_path(file_name, target_folder_name)
    save_df(df_file_final, target_path)
    remove_file(source_path)


def send(imported_file: ImportedFile):
    s3 = aws_utils.get_aws_s3_resource()
    county_name = imported_file.file_schema.county.name
    file_type_folder_name = imported_file.file_schema.file_type.folder_name
    directory_name = imported_file.directory_name
    target_folder = f'{county_name}/{file_type_folder_name}/{directory_name}'
    _, new_prefix = send_file_path('', target_folder)
    _, old_prefix = complete_pending_path_file('', imported_file.directory_name)

    new_prefix = new_prefix[len(settings.STORAGE_S3_PATH)+1:]
    old_prefix = old_prefix[len(settings.STORAGE_S3_PATH)+1:]
    bucket = s3.Bucket(settings.IMPORT_TOOL_BUCKET_NAME)

    for obj in bucket.objects.filter(Prefix=old_prefix):
        old_source = {'Bucket': settings.IMPORT_TOOL_BUCKET_NAME,
                      'Key': obj.key}
        # replace the prefix
        new_key = new_prefix + obj.key[len(old_prefix):]
        new_obj = bucket.Object(new_key)
        new_obj.copy(old_source)
