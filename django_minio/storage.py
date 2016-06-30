import sys
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from minio import Minio
from django.conf import settings
import mimetypes


def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(settings, name, default)


@deconstructible
class MinioStorage(Storage):
    server = setting('MINIO_SERVER')
    access_key = setting('MINIO_ACCESSKEY')
    secret_key = setting('MINIO_SECRET')
    bucket = setting('MINIO_BUCKET')
    secure = True

    def __init__(self, *args, **kwargs):
        super(MinioStorage, self).__init__(*args, **kwargs)
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            self._connection = Minio(
                self.server, self.access_key, self.secret_key, self.secure)
        self._connection.trace_on(sys.stdout)
        return self._connection

    def _bucket_has_object(self, name):
        # temporary returning always False
        return False

    def _save(self, name, content):

        print('SAVE BEGIN', name, content)
        print('name: ', name)
        print('content:', content)
        if hasattr(content.file, 'content_type'):
            content_type = content.file.content_type
        else:
            content_type = mimetypes.guess_type(name)[0]

        # if hasattr(content, 'chunks'):
        #     content_data = b''.join(chunk for chunk in content.chunks())
        # else:
        #     content_data = content.read()
        print('content.file.size: ', content.file.size)
        self.connection.put_object(self.bucket, name, content, content.file.size, content_type=content_type)
        return name

    def url(self, name):
        if self.connection.bucket_exists(self.bucket):
            return self.connection.presigned_get_object(self.bucket, name)
        else:
            return "{}/{}".format(setting('MEDIA_URL'), name)

    def exists(self, name):
        return self._bucket_has_object(name)
