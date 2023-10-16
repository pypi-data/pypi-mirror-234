from django.apps import AppConfig
from . import models

class AGLBaseDBConfig(AppConfig):
    name = 'agl_base_db'
    verbose_name = "AGL Base DB"

default_app_config = 'agl_base_db.AGLBaseDBConfig'
