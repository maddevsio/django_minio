from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
from minio import Minio
from minio.error import ResponseError
from django.conf import settings

# # Initialize minioClient with an endpoint and access/secret keys.
# minioClient = Minio('play.minio.io:9000',
#                     access_key='Q3AM3UQ867SPQQA43P2F',
#                     secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
#                     secure=True)

minioClient = Minio(settings.MINIO_SERVER,
                    access_key=settings.MINIO_ACCESSKEY,
                    secret_key=settings.MINIO_SECRET,
                    secure=True)

bucket = settings.MINIO_BUCKET


@deconstructible
class MinioStorage(FileSystemStorage):

    def _save(self, name, content):
        """"
        Override _save() method to load file object to Minio server.
        """
        obj = super(MinioStorage, self)._save(name, content)
        try:
            minioClient.make_bucket(bucket)
        except ResponseError:
            try:
                file_path = settings.MEDIA_ROOT + '/' + obj
                minioClient.fput_object(bucket, obj, file_path)
            except ResponseError:
                pass
        return obj

    def url(self, name):
        """"
        Override url() method to get the url of a file from Minio server.
        """
        file_url = ''
        try:
            file_url = minioClient.presigned_get_object(bucket, name)
        except ResponseError:
            pass
        return file_url

    def exists(self, name):
        return super(MinioStorage, self).exists(name)
