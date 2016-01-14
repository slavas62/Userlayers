from django.conf import settings
from mutant.contrib.geo.models import GeometryFieldDefinition

default_app_config = 'userlayers.apps.UserlayersConfig'

SETTINGS_DEFAULT_MD_GEOMETRY_FIELD_NAME = 'USERLAYERS_DEFAULT_MD_GEOMETRY_FIELD_NAME'
SETTINGS_DEFAULT_MD_GEOMETRY_FIELD_TYPE = 'USERLAYERS_DEFAULT_MD_GEOMETRY_FIELD_TYPE'
DEFAULT_MD_GEOMETRY_FIELD_NAME = getattr(settings, SETTINGS_DEFAULT_MD_GEOMETRY_FIELD_NAME, 'geometry')
DEFAULT_MD_GEOMETRY_FIELD_TYPE = getattr(settings, SETTINGS_DEFAULT_MD_GEOMETRY_FIELD_TYPE, GeometryFieldDefinition)
