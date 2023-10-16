import boto3

from rastless.core.cog import get_s3_cog_info_from_s3_path
from rastless.db.models import LayerStepModel


class S3Bucket:
    def __init__(self, bucket_name, region="eu-central-1"):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3', region_name=region)
        self.s3_client = boto3.client('s3')
        self.bucket = self.s3.Bucket(bucket_name)

    def list_bucket_entries(self, prefix=None):
        bucket = self.s3.Bucket(self.bucket_name)
        if prefix:
            files = bucket.objects.filter(Prefix=prefix)
        else:
            files = bucket.objects.all()

        return list(files)


def delete_object_by_s3_path(s3_path, region="eu-central-1"):
    s3 = boto3.resource('s3', region_name=region)

    s3_cog_info = get_s3_cog_info_from_s3_path(s3_path)
    s3.Object(s3_cog_info.bucket_name, s3_cog_info.s3_object_name).delete()


def delete_layer_step_files(layer_step: LayerStepModel, cfg):
    if layer_step.cog_filepath and cfg.bucket_name in layer_step.cog_filepath:
        delete_object_by_s3_path(layer_step.cog_filepath)

    if layer_step.cog_layers:
        for _, value in layer_step.cog_layers.items():
            if cfg.bucket_name in value.s3_filepath:
                delete_object_by_s3_path(value.s3_filepath)
