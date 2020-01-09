from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


class OverwriteStorage(FileSystemStorage):
    '''Remove file if already exists and save new one'''
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
