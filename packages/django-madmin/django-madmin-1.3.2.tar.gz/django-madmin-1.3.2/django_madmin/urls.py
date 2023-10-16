from django.conf import settings
from django.urls import path
from . import views


if settings.DEBUG:
    from django.utils.autoreload import file_changed
    file_changed.disconnect(dispatch_uid='template_loaders_file_changed')


prefix = getattr(settings, 'MADMIN', {}).get('upload_path_prefix', 'madmin')


madmin_urls = [
    path('{}/upload/'.format(prefix), views.upload, name="upload"),
    path('{}/check_upload/'.format(prefix), views.check_upload, name="check_upload"),
]
