Django Minio Storage
====================
Django app to use `Minio Server <https://github.com/minio/minio>` as file storage.

Intallation
-----------
At first, you need to have working minio server. How to do that you can found at `Minio Quickstart Guide <https://docs.minio.io/docs/minio>`.

Install Django Minio Storage from pip:
```
pip install django-minio
```
And include django-minio to your installed apps.

Add following keys to your projects settings file:
```
MINIO_SERVER = 'your_minio_server_address'
MINIO_ACCESSKEY = 'your_minio_server_access_key'
MINIO_SECRET = 'your_minio_server_secret_key'
MINIO_BUCKET = 'my_bucket'
```
Demo minio server and it's credentials can be found at `Python Client Quickstart Guide <https://docs.minio.io/docs/python-client-api-reference>`.

Usage
-----
Add `storage` attribute to your ImageField:
```
from django_minio.storage import MinioStorage

photo = models.ImageField(upload_to='photos/', storage=MinioStorage())
```
So the uploaded file will be loaded the `photos` directory in your project's MEDIA directory. Then in your Minio
server's bucket will be created same directory `photos` and the file will be loaded there.