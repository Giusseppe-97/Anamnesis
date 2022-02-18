from core.config import settings
import boto3


def get_aws_session() -> boto3.session.Session:
    session = boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    return session


def get_aws_s3_resource():
    resource = get_aws_session().resource('s3')
    return resource
